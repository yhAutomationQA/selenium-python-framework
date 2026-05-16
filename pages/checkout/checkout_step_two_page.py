from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from pages.checkout.checkout_step_two_locators import CheckoutStepTwoLocators


class CheckoutStepTwoPage(BasePage):
    """Represents the SauceDemo checkout step two (Overview) page."""

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        super().__init__(driver, timeout)
        self._loc = CheckoutStepTwoLocators()

    def open(self, base_url: str = "") -> "CheckoutStepTwoPage":
        """Navigate directly to the checkout overview page.

        Args:
            base_url: The base URL of the application.
        """
        self.open_url(f"{base_url.rstrip('/')}/checkout-step-two.html")
        self.wait_until_visible(self._loc.TITLE)
        return self

    def get_cart_items(self) -> List[WebElement]:
        """Return all cart item row elements on the overview page."""
        return self.find_elements(self._loc.CART_ITEM)

    def get_item_names(self) -> List[str]:
        """Return the product names listed in the overview."""
        return [el.text.strip() for el in self.find_elements(self._loc.CART_ITEM_NAME) if el.text.strip()]

    def get_item_prices(self) -> List[float]:
        """Return the prices of each item as floats."""
        prices: List[float] = []
        for el in self.find_elements(self._loc.CART_ITEM_PRICE):
            raw = el.text.strip().replace("$", "")
            try:
                prices.append(float(raw))
            except ValueError:
                continue
        return prices

    def get_item_quantities(self) -> List[int]:
        """Return the quantities of each item as integers."""
        quantities: List[int] = []
        for el in self.find_elements(self._loc.CART_ITEM_QUANTITY):
            try:
                quantities.append(int(el.text.strip()))
            except ValueError:
                quantities.append(1)
        return quantities

    def get_item_count(self) -> int:
        """Return the number of items in the checkout overview."""
        return len(self.get_cart_items())

    def get_payment_info(self) -> str:
        """Return the payment information text (e.g. 'SauceCard #...')."""
        values = self.find_elements(self._loc.PAYMENT_INFO_VALUE)
        if values:
            return values[0].text.strip()
        return ""

    def get_shipping_info(self) -> str:
        """Return the shipping information text (e.g. 'Free Pony Express Delivery!')."""
        values = self.find_elements(self._loc.PAYMENT_INFO_VALUE)
        if len(values) > 1:
            return values[1].text.strip()
        return ""

    def get_subtotal(self) -> str:
        """Return the item subtotal text."""
        return self.get_text(self._loc.SUBTOTAL_LABEL)

    def get_tax(self) -> str:
        """Return the tax text."""
        return self.get_text(self._loc.TAX_LABEL)

    def get_total(self) -> str:
        """Return the total text."""
        return self.get_text(self._loc.TOTAL_LABEL)

    def click_finish(self) -> "CheckoutStepTwoPage":
        """Click the Finish button to complete the order."""
        self.click(self._loc.FINISH_BUTTON)
        return self

    def click_cancel(self) -> "CheckoutStepTwoPage":
        """Click the Cancel button to return to the inventory."""
        self.click(self._loc.CANCEL_BUTTON)
        return self

    def get_title_text(self) -> str:
        """Return the page title text."""
        return self.get_text(self._loc.TITLE)
