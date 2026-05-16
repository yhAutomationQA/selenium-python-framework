import logging
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from components.base_component import BaseComponent

logger = logging.getLogger(__name__)


class ModalComponent(BaseComponent):
    ROOT = (By.CSS_SELECTOR, ".modal, [role='dialog'], .dialog, .overlay")
    TITLE = (By.CSS_SELECTOR, ".modal-title, .dialog-title, h2, h3, [role='dialog'] h2")
    BODY = (By.CSS_SELECTOR, ".modal-body, .dialog-body, .modal-content > p, [role='dialog'] > p")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, ".modal-confirm, .confirm-btn, .btn-primary, button[type='submit'], [data-action='confirm']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, ".modal-cancel, .cancel-btn, .btn-secondary, [data-action='cancel']")
    CLOSE_BUTTON = (By.CSS_SELECTOR, ".modal-close, .close-btn, .dismiss, [data-dismiss='modal']")
    BACKDROP = (By.CSS_SELECTOR, ".modal-backdrop, .overlay-backdrop")
    INPUTS = (By.CSS_SELECTOR, ".modal-body input, .dialog-body input, [role='dialog'] input")
    ERROR_TEXT = (By.CSS_SELECTOR, ".modal-error, .error-message, .validation-error")

    CONFIRM = "CONFIRM"
    CANCEL = "CANCEL"
    CLOSE = "CLOSE"

    def __init__(self, driver: WebDriver, locator: Optional[tuple] = None, timeout: int = 10):
        super().__init__(driver, locator or self.ROOT, timeout)

    def wait_until_visible(self, timeout: Optional[int] = None) -> "ModalComponent":
        logger.info("Modal | wait_until_visible")
        self._actions.wait_for_visibility(self._root_locator, timeout)
        return self

    def wait_until_closed(self, timeout: Optional[int] = None) -> bool:
        logger.info("Modal | wait_until_closed")
        return self._actions.wait_for_invisibility(self._root_locator, timeout)

    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    def get_message(self) -> str:
        return self.get_text(self.BODY)

    def accept(self, timeout: Optional[int] = None) -> "ModalComponent":
        logger.info("Modal | accept")
        self._actions.click(self.CONFIRM_BUTTON, timeout)
        self.wait_until_closed(timeout)
        return self

    def dismiss(self, timeout: Optional[int] = None) -> "ModalComponent":
        logger.info("Modal | dismiss")
        self._actions.click(self.CANCEL_BUTTON, timeout)
        self.wait_until_closed(timeout)
        return self

    def close(self, timeout: Optional[int] = None) -> "ModalComponent":
        logger.info("Modal | close")
        self._actions.click(self.CLOSE_BUTTON, timeout)
        self.wait_until_closed(timeout)
        return self

    def interact(self, action: str, timeout: Optional[int] = None) -> "ModalComponent":
        if action == self.CONFIRM:
            return self.accept(timeout)
        elif action == self.CANCEL:
            return self.dismiss(timeout)
        elif action == self.CLOSE:
            return self.close(timeout)
        raise ValueError(f"Unknown modal action: {action}")

    def fill_input(self, index: int = 0, text: str = "", timeout: Optional[int] = None) -> "ModalComponent":
        inputs = self.find_elements(self.INPUTS)
        if index >= len(inputs):
            raise IndexError(f"Modal has {len(inputs)} inputs, cannot access index {index}")
        self.fill(self.INPUTS if index == 0 else (By.CSS_SELECTOR, f".modal-body input:nth-of-type({index + 1})"), text, timeout=timeout)
        return self

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_TEXT)

    def has_errors(self) -> bool:
        return self.is_displayed(self.ERROR_TEXT)
