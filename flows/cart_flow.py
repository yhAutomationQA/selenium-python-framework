from typing import List

from flows.base_flow import BaseFlow
from pages.cart.cart_page import CartPage
from pages.inventory.inventory_page import InventoryPage


class CartFlow(BaseFlow):
    """Business workflows for the SauceDemo shopping cart.

    Orchestrates InventoryPage (add/remove/badge) and CartPage
    (view/checkout) into cohesive cart operations.
    """

    def __init__(self, driver, base_url: str = "", timeout: int = 10):
        super().__init__(driver, base_url, timeout)
        self._inventory = InventoryPage(driver, timeout)
        self._cart = CartPage(driver, timeout)

    # ── Add Items ─────────────────────────────────────────────────

    def add_item(self, name: str) -> "CartFlow":
        self._inventory.add_item_to_cart(name)
        return self

    def add_items(self, *names: str) -> "CartFlow":
        for name in names:
            self._inventory.add_item_to_cart(name)
        return self

    def add_all_items(self) -> "CartFlow":
        self._inventory.add_all_items_to_cart()
        return self

    # ── Remove Items ──────────────────────────────────────────────

    def remove_item(self, name: str) -> "CartFlow":
        self._inventory.remove_item_from_cart(name)
        return self

    def remove_all_items(self) -> "CartFlow":
        self._cart.remove_all_items()
        return self

    # ── Navigation ────────────────────────────────────────────────

    def navigate_to_cart(self) -> "CartFlow":
        self._inventory.open_cart()
        return self

    def navigate_to_inventory(self) -> "CartFlow":
        self._cart.click_continue_shopping()
        return self

    def proceed_to_checkout(self) -> "CartFlow":
        self._cart.click_checkout()
        return self

    # ── Queries ───────────────────────────────────────────────────

    @property
    def badge_count(self) -> int:
        return self._inventory.get_cart_badge_count()

    @property
    def item_count(self) -> int:
        return self._cart.get_item_count()

    @property
    def item_names(self) -> List[str]:
        return self._cart.get_item_names()

    @property
    def item_prices(self) -> List[float]:
        return self._cart.get_item_prices()

    @property
    def item_quantities(self) -> List[int]:
        return self._cart.get_item_quantities()

    @property
    def is_empty(self) -> bool:
        return self._cart.is_empty()

    @property
    def inventory_page(self) -> InventoryPage:
        return self._inventory

    @property
    def cart_page(self) -> CartPage:
        return self._cart
