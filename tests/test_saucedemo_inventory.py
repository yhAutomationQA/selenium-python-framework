import pytest
from pages.login.login_page import LoginPage
from pages.inventory.inventory_page import InventoryPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

ITEM_1 = "Sauce Labs Backpack"
ITEM_2 = "Sauce Labs Bike Light"


@pytest.fixture(autouse=True)
def logged_in(driver, base_url):
    LoginPage(driver).open(base_url).login(VALID_USER, VALID_PASS)
    yield


class TestInventoryAddRemove:
    def test_page_load(self, driver):
        inventory = InventoryPage(driver)
        assert inventory.get_page_title() == "Products"
        assert len(inventory.get_item_elements()) == 6

    def test_add_single_item(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart(ITEM_1)
        assert inventory.get_cart_badge_count() == 1
        assert inventory.is_item_in_cart(ITEM_1)

    def test_add_all_items(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_all_items_to_cart()
        assert inventory.get_cart_badge_count() == 6

    def test_add_then_remove(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart(ITEM_1)
        assert inventory.get_cart_badge_count() == 1
        inventory.remove_item_from_cart(ITEM_1)
        assert inventory.get_cart_badge_count() == 0
        assert not inventory.is_item_in_cart(ITEM_1)

    def test_add_multiple_items_badge_count(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart(ITEM_1)
        inventory.add_item_to_cart(ITEM_2)
        assert inventory.get_cart_badge_count() == 2

    @pytest.mark.smoke
    def test_reset_app_state_clears_cart(self, driver):
        inventory = InventoryPage(driver)
        inventory.add_all_items_to_cart()
        assert inventory.get_cart_badge_count() == 6
        inventory.reset_app_state()
        assert inventory.get_cart_badge_count() == 0


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
        details = inventory.get_item_details(ITEM_1)
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
