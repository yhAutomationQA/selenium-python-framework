import pytest

from flows.flow_utils import (
    BACKPACK,
    BIKE_LIGHT,
    ALL_ITEMS,
    INVENTORY_TITLE,
)
from flows.login_flow import LoginFlow
from flows.cart_flow import CartFlow
from pages.inventory.inventory_page import InventoryPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.fixture(autouse=True)
def logged_in(driver, base_url):
    LoginFlow(driver, base_url).login_as_standard_user()
    yield


class TestInventoryAddRemove:
    def test_page_load(self, driver):
        inventory = InventoryPage(driver)
        assert inventory.get_page_title() == INVENTORY_TITLE
        assert len(inventory.get_item_elements()) == 6

    def test_add_single_item(self, driver):
        cart = CartFlow(driver)
        cart.add_item(BACKPACK)
        assert cart.badge_count == 1
        assert cart.inventory_page.is_item_in_cart(BACKPACK)

    def test_add_all_items(self, driver):
        cart = CartFlow(driver)
        cart.add_all_items()
        assert cart.badge_count == 6

    def test_add_then_remove(self, driver):
        cart = CartFlow(driver)
        cart.add_item(BACKPACK)
        assert cart.badge_count == 1
        cart.remove_item(BACKPACK)
        assert cart.badge_count == 0
        assert not cart.inventory_page.is_item_in_cart(BACKPACK)

    def test_add_multiple_items_badge_count(self, driver):
        cart = CartFlow(driver)
        cart.add_items(BACKPACK, BIKE_LIGHT)
        assert cart.badge_count == 2

    @pytest.mark.smoke
    def test_reset_app_state_clears_cart(self, driver):
        cart = CartFlow(driver)
        cart.add_all_items()
        assert cart.badge_count == 6
        cart.inventory_page.reset_app_state()
        assert cart.badge_count == 0


class TestInventorySorting:
    def test_sort_az(self, driver):
        inventory = InventoryPage(driver)
        inventory.sort_by("az")
        names = inventory.get_item_names()
        assert names == sorted(names)

    def test_sort_za(self, driver):
        inventory = InventoryPage(driver)
        inventory.sort_by("za")
        names = inventory.get_item_names()
        assert names == sorted(names, reverse=True)

    def test_sort_lohi(self, driver):
        inventory = InventoryPage(driver)
        inventory.sort_by("lohi")
        prices = inventory.get_item_prices()
        assert prices == sorted(prices)

    def test_sort_hilo(self, driver):
        inventory = InventoryPage(driver)
        inventory.sort_by("hilo")
        prices = inventory.get_item_prices()
        assert prices == sorted(prices, reverse=True)


class TestInventoryDetails:
    def test_get_item_details_returns_correct_data(self, driver):
        inventory = InventoryPage(driver)
        details = inventory.get_item_details(BACKPACK)
        assert details is not None
        assert "description" in details
        assert "price" in details
        assert float(details["price"].replace("$", "")) > 0

    def test_get_item_details_unknown_returns_none(self, driver):
        inventory = InventoryPage(driver)
        assert inventory.get_item_details("Non Existent Item") is None

    def test_item_names_are_not_empty(self, driver):
        inventory = InventoryPage(driver)
        names = inventory.get_item_names()
        assert len(names) == 6
        assert all(name for name in names)

    def test_item_prices_are_positive(self, driver):
        inventory = InventoryPage(driver)
        prices = inventory.get_item_prices()
        assert len(prices) == 6
        assert all(p > 0 for p in prices)
