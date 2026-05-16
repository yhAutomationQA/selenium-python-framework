import logging
import os
from typing import Callable, List, Optional, Tuple, Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotSelectableException,
    MoveTargetOutOfBoundsException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)

from core.wrappers.waits import ElementWaits
from core.wrappers.javascript_actions import JavaScriptActions
from config.constants import SelectBy

logger = logging.getLogger(__name__)

_RESOLVE_ERROR = Union[
    Tuple[str, str],
    WebElement,
]

MAX_RETRY_ATTEMPTS = 3


class ElementActionsError(Exception):
    pass


class ElementActions:
    def __init__(self, driver: WebDriver, default_timeout: int = 10):
        self._driver = driver
        self._default_timeout = default_timeout
        self._waits = ElementWaits(driver, default_timeout)
        self._js = JavaScriptActions(driver, default_timeout)

    @property
    def waits(self) -> ElementWaits:
        return self._waits

    @property
    def js(self) -> JavaScriptActions:
        return self._js

    def _resolve(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> WebElement:
        if isinstance(target, tuple):
            return self._waits.for_presence(target, timeout)
        return target

    def _resolve_visible(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> WebElement:
        if isinstance(target, tuple):
            return self._waits.for_visibility(target, timeout)
        return target

    def _resolve_clickable(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> WebElement:
        if isinstance(target, tuple):
            return self._waits.for_clickable(target, timeout)
        return target

    def _screenshot(self, label: str = "error") -> str:
        name = f"element_action_{label}"
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        path = f"{screenshot_dir}/{name}.png"
        try:
            self._driver.save_screenshot(path)
            logger.info("Screenshot saved: %s", path)
        except Exception as e:
            logger.warning("Screenshot failed: %s", e)
        return path

    def _log_action(self, action: str, target, detail: str = "") -> None:
        label = target if isinstance(target, str) else str(target)
        logger.info("%s | target=%s | %s", action.upper(), label, detail)

    def _intercept_handler(
        self,
        exc: Exception,
        action: str,
        target,
        attempt: int,
        timeout: Optional[int] = None,
    ) -> Optional[bool]:
        if isinstance(exc, StaleElementReferenceException):
            logger.warning(
                "Stale element [%s] on '%s' attempt %d/%d",
                target, action, attempt, MAX_RETRY_ATTEMPTS,
            )
            return True  # retry

        if isinstance(exc, ElementClickInterceptedException):
            logger.warning("Click intercepted [%s], trying JS fallback", target)
            try:
                self._js.click(target, timeout)
                self._log_action("click(js_fallback)", target, "intercepted")
                return False  # handled, don't retry
            except Exception:
                return True  # retry Selenium click

        if isinstance(exc, ElementNotInteractableException):
            logger.warning("Element not interactable [%s], scrolling into view", target)
            self._js.scroll_into_view(target, timeout=timeout)
            return True  # retry after scroll

        if isinstance(exc, MoveTargetOutOfBoundsException):
            logger.warning("Element out of bounds [%s], scrolling", target)
            self._js.scroll_into_view(target, timeout=timeout)
            return True

        return None  # not handled

    def _execute(
        self,
        action_fn: Callable[[], None],
        target,
        action_name: str,
        timeout: Optional[int] = None,
    ) -> None:
        last_exception = None
        for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
            try:
                action_fn()
                return
            except (
                StaleElementReferenceException,
                ElementClickInterceptedException,
                ElementNotInteractableException,
                MoveTargetOutOfBoundsException,
            ) as e:
                last_exception = e
                handled = self._intercept_handler(e, action_name, target, attempt, timeout)
                if handled is False:
                    return
                if handled is None or attempt == MAX_RETRY_ATTEMPTS:
                    break
            except (NoSuchElementException, TimeoutException) as e:
                last_exception = e
                logger.error("Element not found for '%s' [%s]: %s", action_name, target, e)
                self._screenshot(f"{action_name}_not_found")
                raise ElementActionsError(
                    f"Failed to {action_name}: element not found {target}"
                ) from e
            except WebDriverException as e:
                last_exception = e
                logger.error("WebDriver error on '%s' [%s]: %s", action_name, target, e)
                self._screenshot(f"{action_name}_error")
                raise ElementActionsError(
                    f"Failed to {action_name}: {e}" 
                ) from e

        self._screenshot(f"{action_name}_failed")
        raise ElementActionsError(
            f"Failed to {action_name} on {target} after {MAX_RETRY_ATTEMPTS} attempts: {last_exception}"
        ) from last_exception

    def click(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> "ElementActions":
        self._log_action("click", target)
        def _action():
            element = self._resolve_clickable(target, timeout)
            element.click()
        self._execute(_action, target, "click", timeout)
        return self

    def type(
        self,
        target: Union[Tuple[str, str], WebElement],
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None,
    ) -> "ElementActions":
        self._log_action("type", target, f"text='{text}' clear={clear_first}")
        def _action():
            element = self._resolve_visible(target, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
        self._execute(_action, target, "type", timeout)
        return self

    def clear(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> "ElementActions":
        self._log_action("clear", target)
        def _action():
            element = self._resolve_visible(target, timeout)
            element.clear()
        self._execute(_action, target, "clear", timeout)
        return self

    def hover(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> "ElementActions":
        self._log_action("hover", target)
        def _action():
            element = self._resolve_visible(target, timeout)
            ActionChains(self._driver).move_to_element(element).perform()
        self._execute(_action, target, "hover", timeout)
        return self

    def scroll_to(
        self,
        target: Union[Tuple[str, str], WebElement],
        block: str = "center",
        timeout: Optional[int] = None,
    ) -> "ElementActions":
        self._log_action("scroll_to", target, f"block={block}")
        self._js.scroll_into_view(target, block=block, timeout=timeout)
        return self

    def drag_and_drop(
        self,
        source: Union[Tuple[str, str], WebElement],
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> "ElementActions":
        self._log_action("drag_and_drop", source, f"target={target}")
        def _action():
            src_el = self._resolve_visible(source, timeout)
            tgt_el = self._resolve_visible(target, timeout)
            ActionChains(self._driver).drag_and_drop(src_el, tgt_el).perform()
        self._execute(_action, source, "drag_and_drop", timeout)
        return self

    def drag_and_drop_by_offset(
        self,
        source: Union[Tuple[str, str], WebElement],
        x_offset: int,
        y_offset: int,
        timeout: Optional[int] = None,
    ) -> "ElementActions":
        self._log_action("drag_and_drop_by_offset", source, f"x={x_offset} y={y_offset}")
        def _action():
            element = self._resolve_visible(source, timeout)
            ActionChains(self._driver).drag_and_drop_by_offset(element, x_offset, y_offset).perform()
        self._execute(_action, source, "drag_and_drop_by_offset", timeout)
        return self

    def select_dropdown(
        self,
        target: Union[Tuple[str, str], WebElement],
        value: Union[str, int],
        by: SelectBy = SelectBy.TEXT,
        timeout: Optional[int] = None,
    ) -> "ElementActions":
        self._log_action("select_dropdown", target, f"by={by} value={value}")
        def _action():
            element = self._resolve(target, timeout)
            select = Select(element)
            if by == SelectBy.TEXT:
                select.select_by_visible_text(str(value))
            elif by == SelectBy.VALUE:
                select.select_by_value(str(value))
            elif by == SelectBy.INDEX:
                select.select_by_index(int(value))
            else:
                raise ValueError(f"Unsupported SelectBy: {by}")
        self._execute(_action, target, "select_dropdown", timeout)
        return self

    def wait_for_visibility(
        self,
        target: Tuple[str, str],
        timeout: Optional[int] = None,
    ) -> WebElement:
        t = timeout or self._default_timeout
        self._log_action("wait_for_visibility", target, f"timeout={t}")
        try:
            return self._waits.for_visibility(target, t)
        except TimeoutException as e:
            self._screenshot("wait_visibility_timeout")
            raise ElementActionsError(
                f"Element not visible: {target} after {t}s"
            ) from e

    def wait_for_clickable(
        self,
        target: Tuple[str, str],
        timeout: Optional[int] = None,
    ) -> WebElement:
        t = timeout or self._default_timeout
        self._log_action("wait_for_clickable", target, f"timeout={t}")
        try:
            return self._waits.for_clickable(target, t)
        except TimeoutException as e:
            self._screenshot("wait_clickable_timeout")
            raise ElementActionsError(
                f"Element not clickable: {target} after {t}s"
            ) from e

    def wait_for_text(
        self,
        target: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None,
    ) -> bool:
        t = timeout or self._default_timeout
        self._log_action("wait_for_text", target, f"text='{text}' timeout={t}")
        return self._waits.for_text_to_be_present(target, text, t)

    def wait_for_invisibility(
        self,
        target: Tuple[str, str],
        timeout: Optional[int] = None,
    ) -> bool:
        t = timeout or self._default_timeout
        self._log_action("wait_for_invisibility", target, f"timeout={t}")
        return self._waits.for_invisibility(target, t)

    def get_text(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> str:
        self._log_action("get_text", target)
        element = self._resolve_visible(target, timeout)
        try:
            return element.text
        except StaleElementReferenceException:
            logger.warning("Stale element getting text [%s], re-resolving", target)
            element = self._resolve_visible(target, timeout)
            return element.text

    def get_attribute(
        self,
        target: Union[Tuple[str, str], WebElement],
        attribute: str,
        timeout: Optional[int] = None,
    ) -> Optional[str]:
        self._log_action("get_attribute", target, attribute)
        element = self._resolve(target, timeout)
        try:
            return element.get_attribute(attribute)
        except StaleElementReferenceException:
            element = self._resolve(target, timeout)
            return element.get_attribute(attribute)

    def get_value(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> str:
        return self.get_attribute(target, "value", timeout) or ""

    def is_displayed(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> bool:
        try:
            element = self._resolve(target, timeout)
            return element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_enabled(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> bool:
        try:
            element = self._resolve(target, timeout)
            return element.is_enabled()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_selected(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> bool:
        try:
            element = self._resolve(target, timeout)
            return element.is_selected()
        except (NoSuchElementException, TimeoutException):
            return False

    def get_elements(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None,
    ) -> List[WebElement]:
        self._log_action("get_elements", locator)
        return self._waits.for_all_visible(locator, timeout)

    def javascript_click(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> "ElementActions":
        self._log_action("javascript_click", target)
        self._js.click(target, timeout)
        return self
