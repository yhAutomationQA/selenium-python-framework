import pytest
import logging
import os
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver
from core.driver_factory import DriverFactory
from config.config_loader import load_settings, resolve_env
from config.settings import Settings


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


@pytest.fixture(scope="session")
def settings(request) -> Settings:
    env = resolve_env(request.config.getoption("--env"))
    settings = load_settings(env)

    cli_browser = request.config.getoption("--browser")
    cli_headless = request.config.getoption("--headless")

    if cli_browser is not None:
        settings.browser = cli_browser
    if cli_headless is not None:
        settings.headless = cli_headless

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
def base_url(settings: Settings) -> str:
    return settings.base_url


@pytest.fixture(scope="session")
def api_url(settings: Settings) -> str:
    return settings.api_url


@pytest.fixture(scope="function")
def driver(request, settings: Settings, browser_name: str, headless: bool) -> Generator[WebDriver, None, None]:
    driver_instance = DriverFactory.create_driver(
        browser=browser_name,
        headless=headless,
        page_load_timeout=settings.page_load_timeout,
        implicit_wait=settings.implicit_wait,
    )
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver: WebDriver):
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        test_name = request.node.name.replace("/", "_").replace(" ", "_")
        driver.save_screenshot(f"{screenshot_dir}/{test_name}_failed.png")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )
