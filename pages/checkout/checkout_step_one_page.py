from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.checkout.checkout_step_one_locators import CheckoutStepOneLocators


class CheckoutStepOnePage(BasePage):
    """Represents the SauceDemo checkout step one (Your Information) page."""

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        super().__init__(driver, timeout)
        self._loc = CheckoutStepOneLocators()

    def open(self, base_url: str = "") -> "CheckoutStepOnePage":
        """Navigate directly to the checkout step one page.

        Args:
            base_url: The base URL of the application.
        """
        self.open_url(f"{base_url.rstrip('/')}/checkout-step-one.html")
        self.wait_until_visible(self._loc.TITLE)
        return self

    def enter_first_name(self, first_name: str) -> "CheckoutStepOnePage":
        """Type the first name into the first name field."""
        self.fill(self._loc.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str) -> "CheckoutStepOnePage":
        """Type the last name into the last name field."""
        self.fill(self._loc.LAST_NAME_INPUT, last_name)
        return self

    def enter_postal_code(self, postal_code: str) -> "CheckoutStepOnePage":
        """Type the postal code into the postal code field."""
        self.fill(self._loc.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> "CheckoutStepOnePage":
        """Fill all required checkout fields and submit.

        Args:
            first_name: Customer first name.
            last_name: Customer last name.
            postal_code: Customer postal / zip code.
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self) -> "CheckoutStepOnePage":
        """Click the Continue button to proceed to checkout overview."""
        self.click(self._loc.CONTINUE_BUTTON)
        return self

    def click_cancel(self) -> "CheckoutStepOnePage":
        """Click the Cancel button to return to the cart."""
        self.click(self._loc.CANCEL_BUTTON)
        return self

    def get_error_message(self) -> str:
        """Return the visible error text, or empty string if none."""
        if self.is_displayed(self._loc.ERROR_TEXT):
            return self.get_text(self._loc.ERROR_TEXT)
        return ""

    def is_error_displayed(self) -> bool:
        """Check whether the error message container is visible."""
        return self.is_displayed(self._loc.ERROR_CONTAINER)

    def get_title_text(self) -> str:
        """Return the page title text."""
        return self.get_text(self._loc.TITLE)
