import pytest
from pages.login.login_page import LoginPage
from pages.inventory.inventory_page import InventoryPage
from pages.cart.cart_page import CartPage
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage

pytestmark = [pytest.mark.ui, pytest.mark.regression]

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

ITEM_1 = "Sauce Labs Backpack"


@pytest.fixture(autouse=True)
def logged_in(driver, base_url):
    LoginPage(driver).open(base_url).login(VALID_USER, VALID_PASS)
    yield


class TestCheckoutStepOne:
    def test_page_load(self, driver, base_url):
        page = CheckoutStepOnePage(driver)
        page.open(base_url)
        assert "checkout-step-one" in driver.current_url
        assert page.get_title_text() == "Checkout: Your Information"

    def test_cancel_returns_to_cart(self, driver, base_url):
        CartPage(driver).open(base_url).click_checkout()
        CheckoutStepOnePage(driver).click_cancel()
        assert "cart" in driver.current_url

    def test_continue_with_empty_fields_shows_error(self, driver, base_url):
        page = CheckoutStepOnePage(driver)
        page.open(base_url).click_continue()
        assert page.is_error_displayed()
        assert "First Name is required" in page.get_error_message()

    def test_continue_with_first_name_only(self, driver, base_url):
        page = CheckoutStepOnePage(driver)
        page.open(base_url).enter_first_name("Test").click_continue()
        assert page.is_error_displayed()
        assert "Last Name is required" in page.get_error_message()

    def test_continue_with_name_no_postal(self, driver, base_url):
        page = CheckoutStepOnePage(driver)
        page.open(base_url).fill_information("Test", "User", "").click_continue()
        assert page.is_error_displayed()
        assert "Postal Code is required" in page.get_error_message()

    @pytest.mark.smoke
    def test_valid_information_proceeds_to_overview(self, driver, base_url):
        InventoryPage(driver).add_item_to_cart(ITEM_1)
        CartPage(driver).open(base_url).click_checkout()
        CheckoutStepOnePage(driver).fill_information(
            "Test", "User", "12345"
        ).click_continue()
        overview = CheckoutStepTwoPage(driver)
        assert overview.get_title_text() == "Checkout: Overview"


class TestCheckoutStepTwo:
    @pytest.fixture(autouse=True)
    def reach_overview(self, driver, base_url):
        InventoryPage(driver).add_item_to_cart(ITEM_1)
        CartPage(driver).open(base_url).click_checkout()
        CheckoutStepOnePage(driver).fill_information(
            "Test", "User", "12345"
        ).click_continue()
        yield

    def test_overview_page_load(self, driver):
        overview = CheckoutStepTwoPage(driver)
        assert overview.get_title_text() == "Checkout: Overview"
        assert overview.get_item_count() == 1

    def test_overview_item_details(self, driver):
        overview = CheckoutStepTwoPage(driver)
        names = overview.get_item_names()
        assert ITEM_1 in names
        prices = overview.get_item_prices()
        assert len(prices) == 1
        assert prices[0] > 0
        qty = overview.get_item_quantities()
        assert qty == [1]

    def test_overview_totals(self, driver):
        overview = CheckoutStepTwoPage(driver)
        subtotal = overview.get_subtotal()
        tax = overview.get_tax()
        total = overview.get_total()
        assert "Item total" in subtotal or "$" in subtotal
        assert "Tax" in tax or "$" in tax
        assert "Total" in total or "$" in total

    def test_payment_and_shipping_info(self, driver):
        overview = CheckoutStepTwoPage(driver)
        payment = overview.get_payment_info()
        shipping = overview.get_shipping_info()
        assert payment != ""
        assert shipping != ""

    def test_cancel_from_overview(self, driver):
        CheckoutStepTwoPage(driver).click_cancel()
        assert "inventory" in driver.current_url

    @pytest.mark.smoke
    def test_finish_order(self, driver):
        CheckoutStepTwoPage(driver).click_finish()
        assert "checkout-complete" in driver.current_url
