import logging
import os
from typing import List, Optional, Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from config.constants import Directory, SelectBy
from core.wrappers.element_actions import ElementActions
from core.wrappers.javascript_actions import JavaScriptActions
from core.wrappers.waits import ElementWaits

logger = logging.getLogger(__name__)


class BaseComponent:
    def __init__(self, driver: WebDriver, locator: Tuple[str, str], timeout: int = 10):
        self.driver = driver
        self._root_locator = locator
        self._timeout = timeout
        self._name = self.__class__.__name__
        self._actions = ElementActions(driver, timeout)
        self._waits = ElementWaits(driver, timeout)
        self._js = JavaScriptActions(driver, timeout)

    @property
    def actions(self) -> ElementActions:
        return self._actions

    @property
    def waits(self) -> ElementWaits:
        return self._waits

    @property
    def js(self) -> JavaScriptActions:
        return self._js

    @property
    def root_locator(self) -> Tuple[str, str]:
        return self._root_locator

    @property
    def root(self) -> WebElement:
        return self._waits.for_presence(self._root_locator)

    def is_visible(self, timeout: Optional[int] = None) -> bool:
        return self._actions.is_displayed(self._root_locator, timeout)

    def wait_until_visible(self, timeout: Optional[int] = None) -> "BaseComponent":
        self._actions.wait_for_visibility(self._root_locator, timeout)
        return self

    def wait_until_hidden(self, timeout: Optional[int] = None) -> bool:
        return self._actions.wait_for_invisibility(self._root_locator, timeout)

    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BaseComponent":
        self._actions.click(locator, timeout)
        return self

    def fill(
        self,
        locator: Tuple[str, str],
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None,
    ) -> "BaseComponent":
        self._actions.type(locator, text, clear_first=clear_first, timeout=timeout)
        return self

    def clear(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BaseComponent":
        self._actions.clear(locator, timeout)
        return self

    def hover(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BaseComponent":
        self._actions.hover(locator, timeout)
        return self

    def scroll_to(
        self,
        locator: Tuple[str, str],
        block: str = "center",
        timeout: Optional[int] = None,
    ) -> "BaseComponent":
        self._actions.scroll_to(locator, block=block, timeout=timeout)
        return self

    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        return self._actions.get_text(locator, timeout)

    def get_attribute(self, locator: Tuple[str, str], attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        return self._actions.get_attribute(locator, attribute, timeout)

    def get_value(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        return self._actions.get_value(locator, timeout)

    def is_displayed(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        return self._actions.is_displayed(locator, timeout)

    def is_enabled(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        return self._actions.is_enabled(locator, timeout)

    def is_selected(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        return self._actions.is_selected(locator, timeout)

    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> List[WebElement]:
        return self._actions.get_elements(locator, timeout)

    def select_option_by_text(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None,
    ) -> "BaseComponent":
        self._actions.select_dropdown(locator, text, by=SelectBy.TEXT, timeout=timeout)
        return self

    def select_option_by_value(
        self,
        locator: Tuple[str, str],
        value: str,
        timeout: Optional[int] = None,
    ) -> "BaseComponent":
        self._actions.select_dropdown(locator, value, by=SelectBy.VALUE, timeout=timeout)
        return self

    def select_option_by_index(
        self,
        locator: Tuple[str, str],
        index: int,
        timeout: Optional[int] = None,
    ) -> "BaseComponent":
        self._actions.select_dropdown(locator, index, by=SelectBy.INDEX, timeout=timeout)
        return self

    def js_click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BaseComponent":
        self._actions.javascript_click(locator, timeout)
        return self

    def take_screenshot(self, name: Optional[str] = None) -> str:
        filename = name or f"{self._name}_{self._timeout}"
        os.makedirs(Directory.SCREENSHOTS, exist_ok=True)
        path = os.path.join(Directory.SCREENSHOTS, f"{filename}.png")
        self.driver.save_screenshot(path)
        logger.info("%s | screenshot | %s", self._name, path)
        return path
