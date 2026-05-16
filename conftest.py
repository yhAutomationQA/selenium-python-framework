import os
import logging
from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from config.config_loader import load_settings, resolve_env
from config.settings import Settings
from core.driver.browser_options import BrowserOptionsFactory
from core.driver.driver_factory import DriverFactory
from core.driver.driver_manager import DriverManager
from utils.logger import LoggerConfig, log
from utils.allure_manager import AllureManager
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


def pytest_sessionstart(session):
    config_ = session.config
    env = config_.getoption("--env") or os.getenv("ENV", "qa")
    settings = load_settings(env)

    cli_log = config_.getoption("--log-level-cli")
    log_level = cli_log or settings.log_level

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


def pytest_sessionfinish(session):
    log.info("=" * 60)
    log.info("Test session finished")
    log.info("=" * 60)

    config_ = session.config
    env = config_.getoption("--env") or os.getenv("ENV", "qa")
    settings = load_settings(env)
    AllureManager.set_environment_from_settings(settings)


# ── Test Lifecycle Hooks ─────────────────────────────────────────


def pytest_runtest_setup(item):
    log.info("TEST  │ {} │ setup", item.nodeid)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call":
        status = "PASSED" if rep.passed else "FAILED"
        duration = rep.duration
        log.info(
            "TEST  │ {} │ {} ({:.3f}s)",
            item.nodeid,
            status,
            duration,
        )


# ── Settings / Env Fixtures ──────────────────────────────────────


@pytest.fixture(scope="session")
def settings(request) -> Settings:
    env = resolve_env(request.config.getoption("--env"))
    settings = load_settings(env)

    cli_browser = request.config.getoption("--browser")
    cli_headless = request.config.getoption("--headless")
    cli_incognito = request.config.getoption("--incognito")

    if cli_browser is not None:
        settings.browser = cli_browser
    if cli_headless is not None:
        settings.headless = cli_headless
    if cli_incognito is not None:
        settings.incognito = cli_incognito

    return settings


@pytest.fixture(scope="session")
def env(settings: Settings) -> str:
    return settings.env


@pytest.fixture(scope="session")
def browser_name(settings: Settings) -> str:
    return settings.browser


@pytest.fixture(scope="session")
def headless(settings: Settings) -> bool:
    return settings.headless


@pytest.fixture(scope="session")
def incognito(settings: Settings) -> bool:
    return settings.incognito


@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    return settings.base_url


@pytest.fixture(scope="session")
def api_url(settings: Settings) -> str:
    return settings.api_url


# ── Driver Fixtures ──────────────────────────────────────────────


@pytest.fixture(scope="session")
def driver_manager() -> Generator[DriverManager, None, None]:
    manager = DriverManager()
    yield manager
    remaining = manager.active_count
    if remaining > 0:
        log.warning("Cleaning up {} remaining driver(s) at session end", remaining)
        manager.quit_all()


@pytest.fixture(scope="function")
def driver(
    settings: Settings,
    browser_name: str,
    headless: bool,
    incognito: bool,
    driver_manager: DriverManager,
) -> Generator[WebDriver, None, None]:
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

    log.debug("Driver started | session={}", driver_instance.session_id)

    yield driver_instance

    log.debug("Driver quitting | session={}", driver_instance.session_id)
    driver_manager.quit(driver_instance)


# ── Logging / Reporting Fixtures ─────────────────────────────────


@pytest.fixture(scope="session")
def logger():
    """Provide the Loguru logger for manual use in tests."""
    return log


@pytest.fixture(scope="session")
def screenshot_manager() -> ScreenshotManager:
    return ScreenshotManager()


@pytest.fixture(scope="function", autouse=True)
def attach_on_failure(
    request,
    driver: WebDriver,
    screenshot_manager: ScreenshotManager,
):
    """Autouse fixture: captures screenshot + page source on test failure
    and attaches them to Allure."""
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        test_name = request.node.name
        exc = None
        if hasattr(request.node, "rep_call") and request.node.rep_call.excinfo is not None:
            exc = request.node.rep_call.excinfo.value

        screenshot_manager.capture_on_failure(driver, test_name, exception=exc)
