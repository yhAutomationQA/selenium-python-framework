import logging
import time
from typing import Optional, Tuple, Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    JavascriptException,
    TimeoutException,
    WebDriverException,
)

from core.wrappers.waits import ElementWaits

logger = logging.getLogger(__name__)


class JavaScriptActions:
    def __init__(self, driver: WebDriver, default_timeout: int = 10):
        self._driver = driver
        self._waits = ElementWaits(driver, default_timeout)

    def _resolve(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> WebElement:
        if isinstance(target, tuple):
            return self._waits.for_presence(target, timeout)
        return target

    def _execute(self, script: str, *args) -> None:
        return self._driver.execute_script(script, *args)

    def click(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> None:
        element = self._resolve(target, timeout)
        try:
            self._execute("arguments[0].click();", element)
            logger.debug("JS click executed on %s", target)
        except JavascriptException as e:
            logger.error("JS click failed on %s: %s", target, e)
            raise

    def scroll_into_view(
        self,
        target: Union[Tuple[str, str], WebElement],
        block: str = "center",
        timeout: Optional[int] = None,
    ) -> WebElement:
        element = self._resolve(target, timeout)
        self._execute("arguments[0].scrollIntoView({block: arguments[1]});", element, block)
        logger.debug("Scrolled into view: %s (block=%s)", target, block)
        return element

    def scroll_to_bottom(self) -> None:
        self._execute("window.scrollTo(0, document.body.scrollHeight);")
        logger.debug("Scrolled to bottom")

    def scroll_to_top(self) -> None:
        self._execute("window.scrollTo(0, 0);")
        logger.debug("Scrolled to top")

    def scroll_by(self, x: int = 0, y: int = 500) -> None:
        self._execute(f"window.scrollBy({x}, {y});")
        logger.debug("Scrolled by (%d, %d)", x, y)

    def highlight(
        self,
        target: Union[Tuple[str, str], WebElement],
        duration: float = 0.3,
        timeout: Optional[int] = None,
    ) -> None:
        element = self._resolve(target, timeout)
        original_style = self._execute(
            "arguments[0].getAttribute('style');", element
        )
        self._execute(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 3px solid red; background: yellow;",
        )
        time.sleep(duration)
        self._execute(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            original_style or "",
        )
        logger.debug("Highlighted element: %s", target)

    def set_value(
        self,
        target: Union[Tuple[str, str], WebElement],
        value: str,
        timeout: Optional[int] = None,
    ) -> None:
        element = self._resolve(target, timeout)
        self._execute("arguments[0].value = arguments[1];", element, value)
        self._execute(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            element,
        )
        self._execute(
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            element,
        )
        logger.debug("JS set value on %s: '%s'", target, value)

    def get_text(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> str:
        element = self._resolve(target, timeout)
        text = self._execute("return arguments[0].textContent;", element)
        return (text or "").strip()

    def get_inner_html(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> str:
        element = self._resolve(target, timeout)
        html = self._execute("return arguments[0].innerHTML;", element)
        return (html or "").strip()

    def get_attribute(
        self,
        target: Union[Tuple[str, str], WebElement],
        attribute: str,
        timeout: Optional[int] = None,
    ) -> Optional[str]:
        element = self._resolve(target, timeout)
        return self._execute("return arguments[0].getAttribute(arguments[1]);", element, attribute)

    def set_attribute(
        self,
        target: Union[Tuple[str, str], WebElement],
        attribute: str,
        value: str,
        timeout: Optional[int] = None,
    ) -> None:
        element = self._resolve(target, timeout)
        self._execute(
            "arguments[0].setAttribute(arguments[1], arguments[2]);",
            element,
            attribute,
            value,
        )
        logger.debug("Set attribute %s=%s on %s", attribute, value, target)

    def remove_attribute(
        self,
        target: Union[Tuple[str, str], WebElement],
        attribute: str,
        timeout: Optional[int] = None,
    ) -> None:
        element = self._resolve(target, timeout)
        self._execute(
            "arguments[0].removeAttribute(arguments[1]);",
            element,
            attribute,
        )
        logger.debug("Removed attribute %s from %s", attribute, target)

    def is_checked(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> bool:
        element = self._resolve(target, timeout)
        return self._execute("return arguments[0].checked;", element)

    def is_disabled(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> bool:
        element = self._resolve(target, timeout)
        return self._execute("return arguments[0].disabled;", element)

    def get_bounding_rect(
        self,
        target: Union[Tuple[str, str], WebElement],
        timeout: Optional[int] = None,
    ) -> dict:
        element = self._resolve(target, timeout)
        return self._execute(
            "var r = arguments[0].getBoundingClientRect(); return {x: r.x, y: r.y, width: r.width, height: r.height, top: r.top, bottom: r.bottom};",
            element,
        )

    def focus(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> None:
        element = self._resolve(target, timeout)
        self._execute("arguments[0].focus();", element)
        logger.debug("Focused on %s", target)

    def blur(self, target: Union[Tuple[str, str], WebElement], timeout: Optional[int] = None) -> None:
        element = self._resolve(target, timeout)
        self._execute("arguments[0].blur();", element)
        logger.debug("Blurred %s", target)
