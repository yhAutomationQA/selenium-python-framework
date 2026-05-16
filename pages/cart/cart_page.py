from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from pages.cart.cart_locators import CartLocators


class CartPage(BasePage):
    """Represents the SauceDemo shopping cart page.

    Provides methods to inspect cart contents, remove items,
    and navigate to checkout or back to shopping.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        super().__init__(driver, timeout)
        self._loc = CartLocators()

    def open(self, base_url: str = "") -> "CartPage":
        """Navigate directly to the cart page.

        Args:
            base_url: The base URL of the application.
        """
        self.open_url(f"{base_url.rstrip('/')}/cart.html")
        self.wait_until_visible(self._loc.CART_TITLE)
        return self

    def get_cart_items(self) -> List[WebElement]:
        """Return all cart item row elements."""
        return self.find_elements(self._loc.CART_ITEM)

    def get_item_names(self) -> List[str]:
        """Return the product names currently in the cart."""
        return [el.text.strip() for el in self.find_elements(self._loc.CART_ITEM_NAME) if el.text.strip()]

    def get_item_quantities(self) -> List[int]:
        """Return the quantities of each cart item as integers."""
        quantities: List[int] = []
        for el in self.find_elements(self._loc.CART_ITEM_QUANTITY):
            try:
                quantities.append(int(el.text.strip()))
            except ValueError:
                quantities.append(1)
        return quantities

    def get_item_prices(self) -> List[float]:
        """Return the prices of each cart item as floats."""
        prices: List[float] = []
        for el in self.find_elements(self._loc.CART_ITEM_PRICE):
            raw = el.text.strip().replace("$", "")
            try:
                prices.append(float(raw))
            except ValueError:
                continue
        return prices

    def remove_item(self, name: str) -> "CartPage":
        """Click the remove button for the cart item matching the given name.

        Args:
            name: The exact product name to remove.
        """
        items = self.get_cart_items()
        for item in items:
            name_el = item.find_element(*self._loc.CART_ITEM_NAME)
            if name_el.text.strip() == name:
                remove_btn = item.find_element(*self._loc.REMOVE_BUTTON)
                remove_btn.click()
                return self
        raise ValueError(f"Item '{name}' not found in cart")

    def remove_all_items(self) -> "CartPage":
        """Remove every item currently in the cart."""
        for btn in self.find_elements(self._loc.REMOVE_BUTTON):
            btn.click()
        return self

    def click_continue_shopping(self) -> "CartPage":
        """Click the 'Continue Shopping' button to return to the inventory."""
        self.click(self._loc.CONTINUE_SHOPPING_BUTTON)
        return self

    def click_checkout(self) -> "CartPage":
        """Click the 'Checkout' button to proceed to checkout."""
        self.click(self._loc.CHECKOUT_BUTTON)
        return self

    def get_item_count(self) -> int:
        """Return the number of distinct items in the cart."""
        return len(self.get_cart_items())

    def is_empty(self) -> bool:
        """Check whether the cart has zero items (no cart item elements)."""
        return self.get_item_count() == 0
