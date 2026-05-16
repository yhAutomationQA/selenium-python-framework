from selenium.webdriver.remote.webdriver import WebDriver


class BaseFlow:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def refresh(self) -> None:
        self.driver.refresh()
