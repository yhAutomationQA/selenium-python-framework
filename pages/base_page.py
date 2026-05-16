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


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self._timeout = timeout
        self._actions = ElementActions(driver, timeout)
        self._waits = ElementWaits(driver, timeout)
        self._js = JavaScriptActions(driver, timeout)
        self._page_name = self.__class__.__name__

    @property
    def actions(self) -> ElementActions:
        return self._actions

    @property
    def waits(self) -> ElementWaits:
        return self._waits

    @property
    def js(self) -> JavaScriptActions:
        return self._js

    def locator(self, by: str, selector: str) -> Tuple[str, str]:
        return (by, selector)

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def open_url(self, url: str) -> "BasePage":
        logger.info("%s | navigate | %s", self._page_name, url)
        self.driver.get(url)
        return self

    def get_title(self) -> str:
        title = self.driver.title
        logger.debug("%s | title | %s", self._page_name, title)
        return title

    def get_current_url(self) -> str:
        url = self.driver.current_url
        logger.debug("%s | current_url | %s", self._page_name, url)
        return url

    def refresh_page(self) -> "BasePage":
        logger.info("%s | refresh", self._page_name)
        self.driver.refresh()
        return self

    def navigate_back(self) -> "BasePage":
        logger.info("%s | navigate_back", self._page_name)
        self.driver.back()
        return self

    def navigate_forward(self) -> "BasePage":
        logger.info("%s | navigate_forward", self._page_name)
        self.driver.forward()
        return self

    def take_screenshot(self, name: Optional[str] = None) -> str:
        filename = name or f"{self._page_name}_{self._timeout}"
        os.makedirs(Directory.SCREENSHOTS, exist_ok=True)
        path = os.path.join(Directory.SCREENSHOTS, f"{filename}.png")
        self.driver.save_screenshot(path)
        logger.info("%s | screenshot | %s", self._page_name, path)
        return path

    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BasePage":
        self._actions.click(locator, timeout)
        return self

    def fill(
        self, locator: Tuple[str, str], text: str, clear_first: bool = True,
        timeout: Optional[int] = None,
    ) -> "BasePage":
        self._actions.type(locator, text, clear_first=clear_first, timeout=timeout)
        return self

    def clear(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BasePage":
        self._actions.clear(locator, timeout)
        return self

    def hover(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BasePage":
        self._actions.hover(locator, timeout)
        return self

    def scroll_to(self, locator: Tuple[str, str], block: str = "center", timeout: Optional[int] = None) -> "BasePage":
        self._actions.scroll_to(locator, block=block, timeout=timeout)
        return self

    def drag_and_drop(
        self,
        source: Tuple[str, str],
        target: Tuple[str, str],
        timeout: Optional[int] = None,
    ) -> "BasePage":
        self._actions.drag_and_drop(source, target, timeout)
        return self

    def select_option_by_text(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> "BasePage":
        self._actions.select_dropdown(locator, text, by=SelectBy.TEXT, timeout=timeout)
        return self

    def select_option_by_value(self, locator: Tuple[str, str], value: str, timeout: Optional[int] = None) -> "BasePage":
        self._actions.select_dropdown(locator, value, by=SelectBy.VALUE, timeout=timeout)
        return self

    def select_option_by_index(self, locator: Tuple[str, str], index: int, timeout: Optional[int] = None) -> "BasePage":
        self._actions.select_dropdown(locator, index, by=SelectBy.INDEX, timeout=timeout)
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

    def wait_until_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._actions.wait_for_visibility(locator, timeout)

    def wait_until_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._actions.wait_for_clickable(locator, timeout)

    def wait_until_hidden(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        return self._actions.wait_for_invisibility(locator, timeout)

    def wait_for_text(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> bool:
        return self._actions.wait_for_text(locator, text, timeout)

    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> List[WebElement]:
        return self._actions.get_elements(locator, timeout)

    def js_click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BasePage":
        self._actions.javascript_click(locator, timeout)
        return self

    def js_set_value(self, locator: Tuple[str, str], value: str, timeout: Optional[int] = None) -> "BasePage":
        self._js.set_value(locator, value, timeout)
        return self

    def js_scroll_to(
        self, locator: Tuple[str, str], block: str = "center",
        timeout: Optional[int] = None,
    ) -> "BasePage":
        self._js.scroll_into_view(locator, block=block, timeout=timeout)
        return self

    def js_highlight(
        self, locator: Tuple[str, str], duration: float = 0.3,
        timeout: Optional[int] = None,
    ) -> "BasePage":
        self._js.highlight(locator, duration=duration, timeout=timeout)
        return self

    def js_get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        return self._js.get_text(locator, timeout)

    def switch_to_frame(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BasePage":
        element = self._waits.for_presence(locator, timeout)
        self.driver.switch_to.frame(element)
        logger.debug("%s | switch_to_frame | %s", self._page_name, locator)
        return self

    def switch_to_default_content(self) -> "BasePage":
        self.driver.switch_to.default_content()
        logger.debug("%s | switch_to_default_content", self._page_name)
        return self

    def accept_alert(self, timeout: Optional[int] = None) -> "BasePage":
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout or self._timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        logger.debug("%s | accept_alert", self._page_name)
        return self

    def dismiss_alert(self, timeout: Optional[int] = None) -> "BasePage":
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout or self._timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()
        logger.debug("%s | dismiss_alert", self._page_name)
        return self

    def get_alert_text(self, timeout: Optional[int] = None) -> str:
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout or self._timeout).until(EC.alert_is_present())
        text = self.driver.switch_to.alert.text
        logger.debug("%s | alert_text | %s", self._page_name, text)
        return text
