
from selenium.webdriver.remote.webdriver import WebDriver


class BaseFlow:
    def __init__(self, driver: WebDriver, base_url: str = "", timeout: int = 10):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

    def navigate_to(self, url: str) -> "BaseFlow":
        self.driver.get(url)
        return self

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def refresh(self) -> "BaseFlow":
        self.driver.refresh()
        return self
