import pytest

from flows.cart_flow import CartFlow
from flows.flow_utils import BACKPACK, BIKE_LIGHT
from flows.login_flow import LoginFlow
from pages.cart.cart_page import CartPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.fixture(autouse=True)
def logged_in(driver, base_url):
    LoginFlow(driver, base_url).login_as_standard_user()
    yield


class TestCartEmpty:
    def test_empty_cart_direct_access(self, driver, base_url):
        cart = CartPage(driver)
        cart.open(base_url)
        assert cart.is_empty()
        assert cart.get_item_count() == 0

    def test_cart_title_on_empty(self, driver, base_url):
        cart = CartPage(driver)
        cart.open(base_url)
        assert "cart" in driver.current_url


class TestCartWithItems:
    @pytest.fixture(autouse=True)
    def add_items(self, driver):
        CartFlow(driver).add_items(BACKPACK, BIKE_LIGHT)
        yield

    def test_cart_contains_added_items(self, driver):
        cart = CartFlow(driver)
        cart.navigate_to_cart()
        names = cart.item_names
        assert BACKPACK in names
        assert BIKE_LIGHT in names
        assert cart.item_count == 2

    def test_cart_item_quantities(self, driver):
        cart = CartFlow(driver)
        cart.navigate_to_cart()
        quantities = cart.item_quantities
        assert len(quantities) == 2
        assert all(q == 1 for q in quantities)

    def test_cart_item_prices(self, driver):
        cart = CartFlow(driver)
        cart.navigate_to_cart()
        prices = cart.item_prices
        assert len(prices) == 2
        assert all(p > 0 for p in prices)

    def test_remove_single_item(self, driver):
        cart = CartFlow(driver)
        cart.navigate_to_cart()
        cart.cart_page.remove_item(BACKPACK)
        names = cart.item_names
        assert BACKPACK not in names
        assert BIKE_LIGHT in names
        assert cart.item_count == 1

    def test_remove_all_items(self, driver):
        cart = CartFlow(driver)
        cart.navigate_to_cart()
        cart.remove_all_items()
        assert cart.is_empty
        assert cart.item_count == 0


class TestCartNavigation:
    def test_continue_shopping(self, driver):
        cart = CartFlow(driver)
        cart.navigate_to_cart().navigate_to_inventory()
        assert "inventory" in driver.current_url

    @pytest.mark.smoke
    def test_checkout_navigation(self, driver):
        cart = CartFlow(driver)
        cart.navigate_to_cart().proceed_to_checkout()
        assert "checkout-step-one" in driver.current_url

    def test_cart_badge_after_adding_via_inventory(self, driver):
        cart = CartFlow(driver)
        cart.add_item(BACKPACK)
        assert cart.badge_count == 1
        cart.navigate_to_cart()
        assert cart.item_count == 1
