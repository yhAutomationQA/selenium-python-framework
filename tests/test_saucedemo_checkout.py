import pytest

from flows.cart_flow import CartFlow
from flows.checkout_flow import CheckoutFlow
from flows.flow_utils import (
    BACKPACK,
    CHECKOUT_ERROR_FIRST_NAME,
    CHECKOUT_ERROR_LAST_NAME,
    CHECKOUT_ERROR_POSTAL_CODE,
    CHECKOUT_STEP_ONE_TITLE,
    CHECKOUT_STEP_TWO_TITLE,
)
from flows.login_flow import LoginFlow

pytestmark = [pytest.mark.ui, pytest.mark.regression]


@pytest.fixture(autouse=True)
def logged_in(driver, base_url):
    LoginFlow(driver, base_url).login_as_standard_user()
    yield


class TestCheckoutStepOne:
    def test_page_load(self, driver, base_url):
        checkout = CheckoutFlow(driver, base_url)
        checkout.navigate_to_step_one()
        assert "checkout-step-one" in driver.current_url
        assert checkout.step_one_page.get_title_text() == CHECKOUT_STEP_ONE_TITLE

    def test_cancel_returns_to_cart(self, driver, base_url):
        CartFlow(driver, base_url).navigate_to_cart().proceed_to_checkout()
        CheckoutFlow(driver, base_url).cancel_step_one()
        assert "cart" in driver.current_url

    def test_continue_with_empty_fields_shows_error(self, driver, base_url):
        checkout = CheckoutFlow(driver, base_url)
        checkout.navigate_to_step_one().continue_to_overview()
        assert checkout.is_error_displayed
        assert CHECKOUT_ERROR_FIRST_NAME in checkout.error_message

    def test_continue_with_first_name_only(self, driver, base_url):
        checkout = CheckoutFlow(driver, base_url)
        checkout.navigate_to_step_one().fill_shipping_information(
            "Test", "", ""
        ).continue_to_overview()
        assert checkout.is_error_displayed
        assert CHECKOUT_ERROR_LAST_NAME in checkout.error_message

    def test_continue_with_name_no_postal(self, driver, base_url):
        checkout = CheckoutFlow(driver, base_url)
        checkout.navigate_to_step_one().fill_shipping_information(
            "Test", "User", ""
        ).continue_to_overview()
        assert checkout.is_error_displayed
        assert CHECKOUT_ERROR_POSTAL_CODE in checkout.error_message

    @pytest.mark.smoke
    def test_valid_information_proceeds_to_overview(self, driver, base_url):
        CartFlow(driver, base_url).add_item(BACKPACK).navigate_to_cart().proceed_to_checkout()
        checkout = CheckoutFlow(driver, base_url)
        checkout.fill_shipping_with_defaults().continue_to_overview()
        assert checkout.step_two_page.get_title_text() == CHECKOUT_STEP_TWO_TITLE


class TestCheckoutStepTwo:
    @pytest.fixture(autouse=True)
    def reach_overview(self, driver, base_url):
        CartFlow(driver, base_url).add_item(
            BACKPACK
        ).navigate_to_cart().proceed_to_checkout()
        CheckoutFlow(driver, base_url).fill_shipping_with_defaults().continue_to_overview()
        yield

    def test_overview_page_load(self, driver):
        checkout = CheckoutFlow(driver)
        assert checkout.step_two_page.get_title_text() == CHECKOUT_STEP_TWO_TITLE
        assert checkout.item_count == 1

    def test_overview_item_details(self, driver):
        checkout = CheckoutFlow(driver)
        names = checkout.item_names
        assert BACKPACK in names
        prices = checkout.item_prices
        assert len(prices) == 1
        assert prices[0] > 0
        assert checkout.item_quantities == [1]

    def test_overview_totals(self, driver):
        checkout = CheckoutFlow(driver)
        assert "Item total" in checkout.subtotal or "$" in checkout.subtotal
        assert "Tax" in checkout.tax or "$" in checkout.tax
        assert "Total" in checkout.total or "$" in checkout.total

    def test_payment_and_shipping_info(self, driver):
        checkout = CheckoutFlow(driver)
        assert checkout.payment_info != ""
        assert checkout.shipping_info != ""

    def test_cancel_from_overview(self, driver):
        CheckoutFlow(driver).cancel_step_two()
        assert "inventory" in driver.current_url

    @pytest.mark.smoke
    def test_finish_order(self, driver):
        CheckoutFlow(driver).finish_order()
        assert "checkout-complete" in driver.current_url
