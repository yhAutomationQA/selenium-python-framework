import pytest
from selenium.webdriver.remote.webdriver import WebDriver


class BaseTest:
    driver: WebDriver

    @pytest.fixture(autouse=True)
    def setup(self, driver: WebDriver):
        self.driver = driver

    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    def refresh(self) -> None:
        self.driver.refresh()

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    def capture_screenshot(self, name: str) -> str:
        from pathlib import Path
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        filepath = screenshot_dir / f"{name}.png"
        self.driver.save_screenshot(str(filepath))
        return str(filepath)
