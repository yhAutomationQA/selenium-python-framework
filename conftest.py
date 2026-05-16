from __future__ import annotations

import os
from typing import TYPE_CHECKING, Generator

import pytest

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

    from core.driver.driver_manager import DriverManager
    from utils.screenshot_manager import ScreenshotManager


# ── CLI Options ──────────────────────────────────────────────────


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        choices=["chrome", "firefox", "edge", "safari"],
        help="Browser to run tests on (overrides .env file)",
    )
    parser.addoption(
        "--env",
        action="store",
        default=os.getenv("ENV", "qa"),
        choices=["dev", "qa", "staging", "prod"],
        help="Target test environment",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=None,
        help="Run browser in headless mode (overrides .env file)",
    )
    parser.addoption(
        "--incognito",
        action="store_true",
        default=None,
        help="Run browser in incognito/private mode (overrides .env file)",
    )
    parser.addoption(
        "--log-level-cli",
        action="store",
        default=None,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set Loguru log level (overrides .env file)",
    )


# ── Session Hooks ────────────────────────────────────────────────


def _try_load_settings(env: str | None = None):
    """Load settings with graceful fallback if dependencies are missing."""
    try:
        from config.config_loader import load_settings, resolve_env

        return load_settings(resolve_env(env))
    except ImportError:
        return None


def pytest_sessionstart(session):
    settings = _try_load_settings(session.config.getoption("--env"))
    if settings is None:
        return

    cli_log = session.config.getoption("--log-level-cli")
    log_level = cli_log or settings.log_level

    try:
        from utils.logger import LoggerConfig, log

        LoggerConfig.configure(
            log_level=log_level,
            context={
                "env": settings.env,
                "browser": settings.browser,
            },
        )

        log.info("=" * 60)
        log.info("Test session started | env={} | browser={}", settings.env, settings.browser)
        log.info("=" * 60)
    except ImportError:
        pass


def pytest_sessionfinish(session):
    try:
        from utils.logger import log
    except ImportError:
        return

    log.info("=" * 60)
    log.info("Test session finished")
    log.info("=" * 60)

    settings = _try_load_settings(session.config.getoption("--env"))
    if settings is None:
        return

    try:
        from utils.allure_manager import AllureManager

        AllureManager.set_environment_from_settings(settings)
    except ImportError:
        pass


# ── Test Lifecycle Hooks ─────────────────────────────────────────


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call":
        try:
            from utils.logger import log

            status = "PASSED" if rep.passed else "FAILED"
            log.info("TEST  │ {} │ {} ({:.3f}s)", item.nodeid, status, rep.duration)
        except ImportError:
            pass


# ── Settings / Env Fixtures ──────────────────────────────────────


@pytest.fixture(scope="session")
def settings(request):
    from config.config_loader import load_settings, resolve_env

    env = resolve_env(request.config.getoption("--env"))
    loaded = load_settings(env)

    cli_browser = request.config.getoption("--browser")
    cli_headless = request.config.getoption("--headless")
    cli_incognito = request.config.getoption("--incognito")

    if cli_browser is not None:
        loaded.browser = cli_browser
    if cli_headless is not None:
        loaded.headless = cli_headless
    if cli_incognito is not None:
        loaded.incognito = cli_incognito

    return loaded


@pytest.fixture(scope="session")
def env(settings) -> str:
    return settings.env


@pytest.fixture(scope="session")
def browser_name(settings) -> str:
    return settings.browser


@pytest.fixture(scope="session")
def headless(settings) -> bool:
    return settings.headless


@pytest.fixture(scope="session")
def incognito(settings) -> bool:
    return settings.incognito


@pytest.fixture(scope="session")
def base_url(settings) -> str:
    return settings.base_url


@pytest.fixture(scope="session")
def api_url(settings) -> str:
    return settings.api_url


# ── Driver Fixtures ──────────────────────────────────────────────


@pytest.fixture(scope="session")
def driver_manager() -> Generator["DriverManager", None, None]:
    from core.driver.driver_manager import DriverManager

    manager = DriverManager()
    yield manager
    remaining = manager.active_count
    if remaining > 0:
        try:
            from utils.logger import log

            log.warning("Cleaning up {} remaining driver(s) at session end", remaining)
        except ImportError:
            pass
        manager.quit_all()


@pytest.fixture(scope="function")
def driver(
    request,
    settings,
    browser_name: str,
    headless: bool,
    incognito: bool,
    driver_manager: "DriverManager",
) -> Generator["WebDriver", None, None]:
    from core.driver.browser_options import BrowserOptionsFactory
    from core.driver.driver_factory import DriverFactory
    from utils.logger import log

    options = BrowserOptionsFactory.create_options(
        browser=browser_name,
        headless=headless,
        incognito=incognito,
        download_dir=settings.webdriver_download_path,
    )
    driver_instance = DriverFactory.create_driver(
        browser=browser_name,
        options=options,
        remote_url=settings.webdriver_remote_url,
        page_load_timeout=settings.page_load_timeout,
        implicit_wait=settings.implicit_wait,
    )
    driver_instance.maximize_window()
    driver_manager.register(driver_instance)

    request.node._driver = driver_instance
    log.debug("Driver started | session={}", driver_instance.session_id)

    yield driver_instance

    log.debug("Driver quitting | session={}", driver_instance.session_id)
    driver_manager.quit(driver_instance)


# ── Logging / Reporting Fixtures ─────────────────────────────────


@pytest.fixture(scope="session")
def logger():
    """Provide the Loguru logger for manual use in tests."""
    try:
        from utils.logger import log

        return log
    except ImportError:
        return None


@pytest.fixture(scope="session")
def screenshot_manager() -> "ScreenshotManager":
    from utils.screenshot_manager import ScreenshotManager

    return ScreenshotManager()


@pytest.fixture(scope="function", autouse=True)
def attach_on_failure(request, screenshot_manager: "ScreenshotManager"):
    """Autouse fixture: captures screenshot + page source on test failure."""
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        test_name = request.node.name
        exc = None
        rep = getattr(request.node, "rep_call", None)
        exc_info = getattr(rep, "excinfo", None)
        if exc_info is not None:
            exc = exc_info.value

        driver = getattr(request.node, "_driver", None)
        if driver is not None:
            screenshot_manager.capture_on_failure(driver, test_name, exception=exc)
