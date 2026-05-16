from typing import Dict, List, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage
from pages.inventory.inventory_locators import InventoryLocators
from config.constants import SelectBy


class InventoryPage(BasePage):
    """Represents the SauceDocs inventory / products listing page.

    Provides methods to browse products, add or remove items from the cart,
    sort the product list, and access the cart or sidebar menu.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        super().__init__(driver, timeout)
        self._loc = InventoryLocators()

    def open(self, base_url: str = "") -> "InventoryPage":
        """Navigate directly to the inventory page.

        Args:
            base_url: The base URL of the application.
        """
        self.open_url(f"{base_url.rstrip('/')}/inventory.html")
        self.wait_until_visible(self._loc.ITEM)
        return self

    def get_item_elements(self) -> List[WebElement]:
        """Return all product card elements on the page."""
        return self.find_elements(self._loc.ITEM)

    def get_item_names(self) -> List[str]:
        """Return the display names of all visible products."""
        return [
            el.text.strip()
            for el in self.find_elements(self._loc.ITEM_NAME)
            if el.text.strip()
        ]

    def get_item_prices(self) -> List[float]:
        """Return all product prices as floats, stripped of currency symbols."""
        prices: List[float] = []
        for el in self.find_elements(self._loc.ITEM_PRICE):
            raw = el.text.strip().replace("$", "")
            try:
                prices.append(float(raw))
            except ValueError:
                continue
        return prices

    def get_item_details(self, name: str) -> Optional[Dict[str, str]]:
        """Return the description and price for a product by its display name.

        Args:
            name: The exact product name to look up.

        Returns:
            A dict with keys 'description' and 'price', or None if not found.
        """
        items = self.get_item_elements()
        for item in items:
            name_el = item.find_element(*self._loc.ITEM_NAME)
            if name_el.text.strip() == name:
                desc = item.find_element(*self._loc.ITEM_DESC).text.strip()
                price = item.find_element(*self._loc.ITEM_PRICE).text.strip()
                return {"description": desc, "price": price}
        return None

    def add_item_to_cart(self, name: str) -> "InventoryPage":
        """Click the 'Add to cart' button for the product matching the given name.

        Args:
            name: The exact product name.
        """
        items = self.get_item_elements()
        for item in items:
            name_el = item.find_element(*self._loc.ITEM_NAME)
            if name_el.text.strip() == name:
                btn = item.find_element(*self._loc.ADD_TO_CART_BUTTON)
                btn.click()
                return self
        raise ValueError(f"Product '{name}' not found on inventory page")

    def add_all_items_to_cart(self) -> "InventoryPage":
        """Click every available 'Add to cart' button on the page."""
        for btn in self.find_elements(self._loc.ADD_TO_CART_BUTTON):
            btn.click()
        return self

    def remove_item_from_cart(self, name: str) -> "InventoryPage":
        """Click the 'Remove' button for the product matching the given name.

        Args:
            name: The exact product name.
        """
        items = self.get_item_elements()
        for item in items:
            name_el = item.find_element(*self._loc.ITEM_NAME)
            if name_el.text.strip() == name:
                btn = item.find_element(*self._loc.REMOVE_BUTTON)
                btn.click()
                return self
        raise ValueError(f"Product '{name}' not found on inventory page")

    def get_cart_badge_count(self) -> int:
        """Return the number displayed on the shopping cart badge.

        Returns:
            0 if the badge is not visible (empty cart).
        """
        if self.is_displayed(self._loc.SHOPPING_CART_BADGE):
            text = self.get_text(self._loc.SHOPPING_CART_BADGE)
            try:
                return int(text.strip())
            except ValueError:
                return 0
        return 0

    def open_cart(self) -> "InventoryPage":
        """Click the shopping cart link to navigate to the cart page."""
        self.click(self._loc.SHOPPING_CART_LINK)
        return self

    def sort_by(self, value: str) -> "InventoryPage":
        """Select a sort option from the product sort dropdown.

        Args:
            value: The option value  (e.g. 'za', 'az', 'lohi', 'hilo').
        """
        self.select_option_by_value(self._loc.SORT_DROPDOWN, value)
        return self

    def open_burger_menu(self) -> "InventoryPage":
        """Open the sidebar burger menu."""
        self.click(self._loc.BURGER_MENU_BUTTON)
        self.wait_until_visible(self._loc.BURGER_MENU)
        return self

    def close_burger_menu(self) -> "InventoryPage":
        """Close the sidebar burger menu."""
        if self.is_displayed(self._loc.CLOSE_MENU_BUTTON):
            self.click(self._loc.CLOSE_MENU_BUTTON)
            self.wait_until_hidden(self._loc.BURGER_MENU)
        return self

    def logout(self) -> "InventoryPage":
        """Open the sidebar and click the logout link."""
        self.open_burger_menu()
        self.click(self._loc.LOGOUT_SIDEBAR_LINK)
        return self

    def reset_app_state(self) -> "InventoryPage":
        """Open the sidebar and click the reset app state link."""
        self.open_burger_menu()
        self.click(self._loc.RESET_SIDEBAR_LINK)
        return self

    def is_item_in_cart(self, name: str) -> bool:
        """Check whether a product already has a 'Remove' button visible.

        Args:
            name: The exact product name.
        """
        items = self.get_item_elements()
        for item in items:
            name_el = item.find_element(*self._loc.ITEM_NAME)
            if name_el.text.strip() == name:
                return item.find_elements(*self._loc.REMOVE_BUTTON) and True
        return False

    def get_page_title(self) -> str:
        """Return the inventory page header title."""
        return self.get_text(self._loc.TITLE)
