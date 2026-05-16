from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Optional, Tuple


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self._timeout = timeout

    def _find(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        wait_time = timeout or self._timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(locator)
        )

    def _find_all(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> List[WebElement]:
        wait_time = timeout or self._timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        wait_time = timeout or self._timeout
        WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def fill(self, locator: Tuple[str, str], text: str, clear: bool = True, timeout: Optional[int] = None) -> None:
        element = self._find(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        return self._find(locator, timeout).text

    def get_attribute(self, locator: Tuple[str, str], attribute: str, timeout: Optional[int] = None) -> str:
        return self._find(locator, timeout).get_attribute(attribute)

    def is_displayed(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        try:
            return self._find(locator, timeout).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_selected(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        return self._find(locator, timeout).is_selected()

    def wait_until_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        wait_time = timeout or self._timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until_hidden(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        wait_time = timeout or self._timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.invisibility_of_element_located(locator)
        )

    def select_option_by_text(self, locator: Tuple[str, str], text: str) -> None:
        Select(self._find(locator)).select_by_visible_text(text)

    def select_option_by_value(self, locator: Tuple[str, str], value: str) -> None:
        Select(self._find(locator)).select_by_value(value)

    def select_option_by_index(self, locator: Tuple[str, str], index: int) -> None:
        Select(self._find(locator)).select_by_index(index)

    def switch_to_frame(self, locator: Tuple[str, str]) -> None:
        frame = self._find(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()

    def accept_alert(self) -> None:
        WebDriverWait(self.driver, self._timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self) -> None:
        WebDriverWait(self.driver, self._timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self) -> str:
        WebDriverWait(self.driver, self._timeout).until(EC.alert_is_present())
        return self.driver.switch_to.alert.text

    def scroll_into_view(self, locator: Tuple[str, str]) -> None:
        element = self._find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def execute_js(self, script: str, *args) -> None:
        self.driver.execute_script(script, *args)

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

    def take_screenshot(self, name: str) -> str:
        from pathlib import Path
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        filepath = screenshot_dir / f"{name}.png"
        self.driver.save_screenshot(str(filepath))
        return str(filepath)

    def navigate(self, url: str) -> None:
        self.driver.get(url)

    def refresh(self) -> None:
        self.driver.refresh()

    def go_back(self) -> None:
        self.driver.back()

    def go_forward(self) -> None:
        self.driver.forward()
