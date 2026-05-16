import logging
from enum import Enum
from typing import Callable, List, Optional, Tuple, Type, Union

from selenium.common.exceptions import (
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class WaitCondition(str, Enum):
    VISIBILITY = "visibility"
    CLICKABLE = "clickable"
    PRESENCE = "presence"
    INVISIBILITY = "invisibility"
    TEXT = "text"
    VALUE = "value"
    ATTRIBUTE = "attribute"
    SELECTION = "selection"
    STALENESS = "staleness"
    FRAME = "frame"
    ALERT = "alert"


_CONDITION_MAP = {
    WaitCondition.VISIBILITY: EC.visibility_of_element_located,
    WaitCondition.CLICKABLE: EC.element_to_be_clickable,
    WaitCondition.PRESENCE: EC.presence_of_element_located,
    WaitCondition.INVISIBILITY: EC.invisibility_of_element_located,
    WaitCondition.STALENESS: EC.staleness_of,
    WaitCondition.FRAME: EC.frame_to_be_available_and_switch_to_it,
    WaitCondition.ALERT: EC.alert_is_present,
}


class ElementWaits:
    def __init__(
        self,
        driver: WebDriver,
        timeout: int = 10,
        poll_frequency: float = 0.5,
        ignored_exceptions: Optional[List[Type[Exception]]] = None,
    ):
        self._driver = driver
        self._timeout = timeout
        self._poll = poll_frequency
        self._ignored = ignored_exceptions or [StaleElementReferenceException]

    def copy_with(
        self,
        timeout: Optional[int] = None,
        poll: Optional[float] = None,
    ) -> "ElementWaits":
        return ElementWaits(
            driver=self._driver,
            timeout=timeout if timeout is not None else self._timeout,
            poll_frequency=poll if poll is not None else self._poll,
            ignored_exceptions=list(self._ignored),
        )

    def with_timeout(self, timeout: int) -> "ElementWaits":
        return self.copy_with(timeout=timeout)

    def with_poll(self, frequency: float) -> "ElementWaits":
        return self.copy_with(poll=frequency)

    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        t = timeout if timeout is not None else self._timeout
        return WebDriverWait(
            driver=self._driver,
            timeout=t,
            poll_frequency=self._poll,
            ignored_exceptions=self._ignored,
        )

    def _until(
        self,
        condition: Callable,
        locator: Tuple[str, str],
        timeout: Optional[int] = None,
        message: str = "",
    ) -> Union[WebElement, bool]:
        return self._wait(timeout).until(
            condition(locator),
            message or f"Timed out waiting for condition on {locator}",
        )

    def for_visibility(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._until(EC.visibility_of_element_located, locator, timeout)

    def for_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._until(EC.element_to_be_clickable, locator, timeout)

    def for_presence(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._until(EC.presence_of_element_located, locator, timeout)

    def for_invisibility(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        return self._until(EC.invisibility_of_element_located, locator, timeout)

    def for_text_to_be_present(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None,
    ) -> bool:
        return self._wait(timeout).until(
            EC.text_to_be_present_in_element(locator, text),
            f"Text '{text}' not found in {locator}",
        )

    def for_text_to_be_present_in_value(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None,
    ) -> bool:
        return self._wait(timeout).until(
            EC.text_to_be_present_in_element_value(locator, text),
            f"Value '{text}' not found in {locator}",
        )

    def for_attribute_to_contain(
        self,
        locator: Tuple[str, str],
        attribute: str,
        value: str,
        timeout: Optional[int] = None,
    ) -> bool:
        return self._wait(timeout).until(
            lambda d: (
                d.find_element(*locator).get_attribute(attribute)
                and value in d.find_element(*locator).get_attribute(attribute)
            ),
            f"Attribute '{attribute}' does not contain '{value}' in {locator}",
        )

    def for_staleness(self, element: WebElement, timeout: Optional[int] = None) -> bool:
        return self._wait(timeout).until(
            EC.staleness_of(element),
            "Element did not go stale",
        )

    def for_any(self, *locators: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        return self._wait(timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, " | ".join(f"({loc[1]})" for loc in locators)))
        )

    def for_all_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> List[WebElement]:
        return self._wait(timeout).until(
            EC.visibility_of_all_elements_located(locator),
            f"Not all elements visible for {locator}",
        )

    def for_count(
        self,
        locator: Tuple[str, str],
        expected_count: int,
        timeout: Optional[int] = None,
    ) -> List[WebElement]:
        def _count_condition(driver):
            elements = driver.find_elements(*locator)
            if len(elements) == expected_count:
                return elements
            return None

        return self._wait(timeout).until(
            _count_condition,
            f"Expected {expected_count} elements for {locator}",
        )
