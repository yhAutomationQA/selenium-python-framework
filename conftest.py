import pytest
import logging
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver
from core.driver_factory import DriverFactory
from config.environments import ENV_CONFIG


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge", "safari"],
        help="Browser to run tests on",
    )
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        choices=["dev", "qa", "staging", "prod"],
        help="Target test environment",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="session")
def env(request) -> str:
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def browser_name(request) -> str:
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request) -> bool:
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def base_url(env: str) -> str:
    return ENV_CONFIG[env]["base_url"]


@pytest.fixture(scope="session")
def api_url(env: str) -> str:
    return ENV_CONFIG[env]["api_url"]


@pytest.fixture(scope="function")
def driver(request, browser_name: str, headless: bool) -> Generator[WebDriver, None, None]:
    driver_instance = DriverFactory.create_driver(browser=browser_name, headless=headless)
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver: WebDriver):
    yield
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot_dir = "screenshots"
        import os
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
