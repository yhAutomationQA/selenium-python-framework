from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService


class DriverFactory:

    @staticmethod
    def create_driver(browser: str = "chrome", headless: bool = False) -> WebDriver:
        browser = browser.lower()
        drivers = {
            "chrome": DriverFactory._create_chrome_driver,
            "firefox": DriverFactory._create_firefox_driver,
            "edge": DriverFactory._create_edge_driver,
        }
        creator = drivers.get(browser)
        if not creator:
            raise ValueError(f"Unsupported browser: {browser}. Supported: {list(drivers.keys())}")
        return creator(headless)

    @staticmethod
    def _create_chrome_driver(headless: bool) -> WebDriver:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _create_firefox_driver(headless: bool) -> WebDriver:
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def _create_edge_driver(headless: bool) -> WebDriver:
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
