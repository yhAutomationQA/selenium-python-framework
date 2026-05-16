from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple


class BaseComponent:
    def __init__(self, driver: WebDriver, locator: Tuple[str, str]):
        self.driver = driver
        self.locator = locator
        self._root_element: WebElement = None

    @property
    def root_element(self) -> WebElement:
        if self._root_element is None:
            self._root_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.locator)
            )
        return self._root_element

    def is_displayed(self) -> bool:
        try:
            return self.root_element.is_displayed()
        except Exception:
            return False

    def get_text(self) -> str:
        return self.root_element.text

    def get_attribute(self, name: str) -> str:
        return self.root_element.get_attribute(name)

    def click(self) -> None:
        self.root_element.click()
