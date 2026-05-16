import logging
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from core.driver.browser_options import BrowserOptions, BrowserOptionsFactory

logger = logging.getLogger(__name__)


class DriverFactory:

    @staticmethod
    def create_driver(
        browser: str = "chrome",
        options: Optional[BrowserOptions] = None,
        remote_url: Optional[str] = None,
        page_load_timeout: int = 30,
        implicit_wait: int = 10,
        headless: bool = False,
        incognito: bool = False,
        download_dir: Optional[str] = None,
    ) -> WebDriver:
        if options is None:
            options = BrowserOptionsFactory.create_options(
                browser=browser,
                headless=headless,
                incognito=incognito,
                download_dir=download_dir,
            )

        if remote_url:
            logger.info("Creating remote WebDriver for %s at %s", browser, remote_url)
            return DriverFactory._create_remote_driver(browser, options, remote_url, page_load_timeout, implicit_wait)

        logger.info("Creating local WebDriver for %s", browser)
        return DriverFactory._create_local_driver(browser, options, page_load_timeout, implicit_wait)

    @staticmethod
    def _create_local_driver(
        browser: str,
        options: BrowserOptions,
        page_load_timeout: int,
        implicit_wait: int,
    ) -> WebDriver:
        creators = {
            "chrome": DriverFactory._create_local_chrome,
            "firefox": DriverFactory._create_local_firefox,
            "edge": DriverFactory._create_local_edge,
        }
        creator = creators.get(browser)
        if not creator:
            raise ValueError(f"Unsupported browser: {browser}")
        driver = creator(options)
        driver.set_page_load_timeout(page_load_timeout)
        driver.implicitly_wait(implicit_wait)
        logger.debug("Driver configured: page_load_timeout=%d, implicit_wait=%d", page_load_timeout, implicit_wait)
        return driver

    @staticmethod
    def _create_remote_driver(
        browser: str,
        options: BrowserOptions,
        remote_url: str,
        page_load_timeout: int,
        implicit_wait: int,
    ) -> WebDriver:
        driver = webdriver.Remote(command_executor=remote_url, options=options)
        driver.set_page_load_timeout(page_load_timeout)
        driver.implicitly_wait(implicit_wait)
        logger.info("Remote driver connected: browser=%s, grid=%s", browser, remote_url)
        return driver

    @staticmethod
    def _create_local_chrome(options: ChromeOptions) -> WebDriver:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logger.debug("Chrome driver created")
        return driver

    @staticmethod
    def _create_local_firefox(options: FirefoxOptions) -> WebDriver:
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        logger.debug("Firefox driver created")
        return driver

    @staticmethod
    def _create_local_edge(options: EdgeOptions) -> WebDriver:
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        logger.debug("Edge driver created")
        return driver
