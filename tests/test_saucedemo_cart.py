import pytest
from pages.login.login_page import LoginPage
from pages.inventory.inventory_page import InventoryPage
from pages.cart.cart_page import CartPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

ITEM_1 = "Sauce Labs Backpack"
ITEM_2 = "Sauce Labs Bike Light"


@pytest.fixture(autouse=True)
def logged_in(driver, base_url):
    LoginPage(driver).open(base_url).login(VALID_USER, VALID_PASS)
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
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart(ITEM_1)
        inventory.add_item_to_cart(ITEM_2)
        yield

    def test_cart_contains_added_items(self, driver):
        inventory = InventoryPage(driver)
        inventory.open_cart()
        cart = CartPage(driver)
        names = cart.get_item_names()
        assert ITEM_1 in names
        assert ITEM_2 in names
        assert cart.get_item_count() == 2

    def test_cart_item_quantities(self, driver):
        InventoryPage(driver).open_cart()
        cart = CartPage(driver)
        qty = cart.get_item_quantities()
        assert len(qty) == 2
        assert all(q == 1 for q in qty)

    def test_cart_item_prices(self, driver):
        InventoryPage(driver).open_cart()
        cart = CartPage(driver)
        prices = cart.get_item_prices()
        assert len(prices) == 2
        assert all(p > 0 for p in prices)

    def test_remove_single_item(self, driver):
        InventoryPage(driver).open_cart()
        cart = CartPage(driver)
        cart.remove_item(ITEM_1)
        names = cart.get_item_names()
        assert ITEM_1 not in names
        assert ITEM_2 in names
        assert cart.get_item_count() == 1

    def test_remove_all_items(self, driver):
        InventoryPage(driver).open_cart()
        cart = CartPage(driver)
        cart.remove_all_items()
        assert cart.is_empty()
        assert cart.get_item_count() == 0


class TestCartNavigation:
    def test_continue_shopping(self, driver):
        InventoryPage(driver).open_cart()
        cart = CartPage(driver)
        cart.click_continue_shopping()
        assert "inventory" in driver.current_url

    @pytest.mark.smoke
    def test_checkout_navigation(self, driver):
        InventoryPage(driver).open_cart()
        cart = CartPage(driver)
        cart.click_checkout()
        assert "checkout-step-one" in driver.current_url

    def test_cart_badge_after_adding_via_inventory(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart(ITEM_1)
        assert inventory.get_cart_badge_count() == 1
        inventory.open_cart()
        assert CartPage(driver).get_item_count() == 1
