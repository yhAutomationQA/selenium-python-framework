from typing import List, Optional

from selenium.webdriver.remote.webdriver import WebDriver

from flows.base_flow import BaseFlow
from pages.login.login_page import LoginPage
from pages.inventory.inventory_page import InventoryPage
from pages.cart.cart_page import CartPage
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


class CheckoutFlow(BaseFlow):
    """Orchestrates a complete SauceDemo purchase flow.

    Combines login, inventory selection, cart review, and checkout
    into reusable multi-step sequences for end-to-end tests.
    """

    def __init__(self, driver: WebDriver, base_url: str = "", timeout: int = 10):
        super().__init__(driver)
        self.base_url = base_url
        self.timeout = timeout

    def login_as(
        self, username: str = VALID_USER, password: str = VALID_PASS
    ) -> "CheckoutFlow":
        """Log in with the given credentials."""
        LoginPage(self.driver, self.timeout).open(
            self.base_url
        ).login(username, password)
        return self

    def add_items_to_cart(self, items: List[str]) -> "CheckoutFlow":
        """Add one or more product names to the shopping cart."""
        inventory = InventoryPage(self.driver, self.timeout)
        for item in items:
            inventory.add_item_to_cart(item)
        return self

    def add_all_items_to_cart(self) -> "CheckoutFlow":
        """Add every product on the inventory page to the cart."""
        InventoryPage(self.driver, self.timeout).add_all_items_to_cart()
        return self

    def go_to_cart(self) -> "CheckoutFlow":
        """Navigate to the shopping cart page."""
        InventoryPage(self.driver, self.timeout).open_cart()
        return self

    def proceed_to_checkout(self) -> "CheckoutFlow":
        """Click the checkout button from the cart page."""
        CartPage(self.driver, self.timeout).click_checkout()
        return self

    def enter_shipping_information(
        self,
        first_name: str = "Test",
        last_name: str = "User",
        postal_code: str = "12345",
    ) -> "CheckoutFlow":
        """Fill in the checkout step one form."""
        CheckoutStepOnePage(self.driver, self.timeout).fill_information(
            first_name, last_name, postal_code
        ).click_continue()
        return self

    def finish_purchase(self) -> "CheckoutFlow":
        """Complete the order on the checkout overview page."""
        CheckoutStepTwoPage(self.driver, self.timeout).click_finish()
        return self

    def full_checkout(
        self,
        items: Optional[List[str]] = None,
        first_name: str = "Test",
        last_name: str = "User",
        postal_code: str = "12345",
    ) -> "CheckoutFlow":
        """Run a complete purchase from login to order completion.

        Args:
            items: Product names to add. Defaults to ["Sauce Labs Backpack"].
            first_name: Checkout first name.
            last_name: Checkout last name.
            postal_code: Checkout postal code.
        """
        items = items or ["Sauce Labs Backpack"]
        return (
            self.login_as()
            .add_items_to_cart(items)
            .go_to_cart()
            .proceed_to_checkout()
            .enter_shipping_information(first_name, last_name, postal_code)
            .finish_purchase()
        )
