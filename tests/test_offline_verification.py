"""Static structure tests that run without a browser.

Marked with @pytest.mark.offline. Run with: pytest -m offline
Verifies page objects, locators, and flows are correctly defined.
"""
from unittest.mock import MagicMock, PropertyMock

import pytest

pytestmark = [pytest.mark.offline]


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    type(driver).title = PropertyMock(return_value="Swag Labs")
    type(driver).current_url = PropertyMock(
        return_value="https://www.saucedemo.com/"
    )
    element = MagicMock()
    element.is_displayed.return_value = True
    element.is_enabled.return_value = True
    element.text = "mock_text"
    element.get_attribute.return_value = "mock_attribute"
    element.tag_name = "div"
    driver.find_element.return_value = element
    driver.find_elements.return_value = [element]
    return driver


class TestLocatorStructure:
    def test_login_locators(self):
        from pages.login.login_locators import LoginLocators

        loc = LoginLocators()
        assert hasattr(loc, "USERNAME_INPUT")
        assert hasattr(loc, "PASSWORD_INPUT")
        assert hasattr(loc, "LOGIN_BUTTON")
        assert hasattr(loc, "ERROR_TEXT")
        assert hasattr(loc, "ERROR_CONTAINER")
        assert hasattr(loc, "ERROR_CLOSE_BUTTON")

    def test_inventory_locators(self):
        from pages.inventory.inventory_locators import InventoryLocators

        loc = InventoryLocators()
        assert hasattr(loc, "ITEM")
        assert hasattr(loc, "ITEM_NAME")
        assert hasattr(loc, "ITEM_PRICE")
        assert hasattr(loc, "ADD_TO_CART_BUTTON")
        assert hasattr(loc, "REMOVE_BUTTON")
        assert hasattr(loc, "SORT_DROPDOWN")
        assert hasattr(loc, "SHOPPING_CART_BADGE")
        assert hasattr(loc, "SHOPPING_CART_LINK")
        assert hasattr(loc, "BURGER_MENU_BUTTON")
        assert hasattr(loc, "LOGOUT_SIDEBAR_LINK")
        assert hasattr(loc, "TITLE")

    def test_cart_locators(self):
        from pages.cart.cart_locators import CartLocators

        loc = CartLocators()
        assert hasattr(loc, "CART_ITEM")
        assert hasattr(loc, "CART_ITEM_NAME")
        assert hasattr(loc, "CART_ITEM_PRICE")
        assert hasattr(loc, "CART_ITEM_QUANTITY")
        assert hasattr(loc, "REMOVE_BUTTON")
        assert hasattr(loc, "CONTINUE_SHOPPING_BUTTON")
        assert hasattr(loc, "CHECKOUT_BUTTON")
        assert hasattr(loc, "CART_TITLE")

    def test_checkout_step_one_locators(self):
        from pages.checkout.checkout_step_one_locators import (
            CheckoutStepOneLocators,
        )

        loc = CheckoutStepOneLocators()
        assert hasattr(loc, "TITLE")
        assert hasattr(loc, "FIRST_NAME_INPUT")
        assert hasattr(loc, "LAST_NAME_INPUT")
        assert hasattr(loc, "POSTAL_CODE_INPUT")
        assert hasattr(loc, "CONTINUE_BUTTON")
        assert hasattr(loc, "CANCEL_BUTTON")
        assert hasattr(loc, "ERROR_TEXT")

    def test_checkout_step_two_locators(self):
        from pages.checkout.checkout_step_two_locators import (
            CheckoutStepTwoLocators,
        )

        loc = CheckoutStepTwoLocators()
        assert hasattr(loc, "TITLE")
        assert hasattr(loc, "CART_ITEM")
        assert hasattr(loc, "CART_ITEM_NAME")
        assert hasattr(loc, "CART_ITEM_PRICE")
        assert hasattr(loc, "FINISH_BUTTON")
        assert hasattr(loc, "CANCEL_BUTTON")
        assert hasattr(loc, "SUBTOTAL_LABEL")
        assert hasattr(loc, "TAX_LABEL")
        assert hasattr(loc, "TOTAL_LABEL")

    def test_all_locators_are_tuples(self):
        from pages.login.login_locators import LoginLocators
        from pages.inventory.inventory_locators import InventoryLocators
        from pages.cart.cart_locators import CartLocators
        from pages.checkout.checkout_step_one_locators import (
            CheckoutStepOneLocators,
        )
        from pages.checkout.checkout_step_two_locators import (
            CheckoutStepTwoLocators,
        )

        for loc_cls in [
            LoginLocators,
            InventoryLocators,
            CartLocators,
            CheckoutStepOneLocators,
            CheckoutStepTwoLocators,
        ]:
            loc = loc_cls()
            for attr_name in dir(loc):
                if attr_name.startswith("_"):
                    continue
                val = getattr(loc, attr_name)
                assert isinstance(val, tuple), (
                    f"{loc_cls.__name__}.{attr_name} is not a tuple"
                )
                assert len(val) == 2
                assert isinstance(val[0], str)
                assert isinstance(val[1], str)


class TestPageInstantiation:
    def test_login_page(self, mock_driver):
        from pages.login.login_page import LoginPage

        page = LoginPage(mock_driver)
        assert page._actions is not None
        assert page._waits is not None
        assert page._js is not None

    def test_inventory_page(self, mock_driver):
        from pages.inventory.inventory_page import InventoryPage

        page = InventoryPage(mock_driver)
        assert page._loc is not None

    def test_cart_page(self, mock_driver):
        from pages.cart.cart_page import CartPage

        page = CartPage(mock_driver)
        assert page._loc is not None

    def test_checkout_step_one_page(self, mock_driver):
        from pages.checkout.checkout_step_one_page import CheckoutStepOnePage

        page = CheckoutStepOnePage(mock_driver)
        assert page._loc is not None

    def test_checkout_step_two_page(self, mock_driver):
        from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage

        page = CheckoutStepTwoPage(mock_driver)
        assert page._loc is not None


class TestPageExports:
    def test_pages_init_exports_all(self):
        from pages import (
            BasePage,
            LoginPage,
            InventoryPage,
            CartPage,
            CheckoutStepOnePage,
            CheckoutStepTwoPage,
        )

        assert BasePage is not None
        assert LoginPage is not None
        assert InventoryPage is not None
        assert CartPage is not None
        assert CheckoutStepOnePage is not None
        assert CheckoutStepTwoPage is not None

    def test_flows_init_exports(self):
        from flows import BaseFlow, LoginFlow, CartFlow, CheckoutFlow

        assert BaseFlow is not None
        assert LoginFlow is not None
        assert CartFlow is not None
        assert CheckoutFlow is not None
    
    def test_flow_utils_constants(self):
        from flows.flow_utils import (
            STANDARD_USER,
            LOCKED_OUT_USER,
            VALID_PASSWORD,
            BACKPACK,
            BIKE_LIGHT,
            ALL_ITEMS,
            DEFAULT_FIRST_NAME,
            INVENTORY_TITLE,
            LOGIN_ERROR_MISMATCH,
        )

        assert STANDARD_USER == "standard_user"
        assert LOCKED_OUT_USER == "locked_out_user"
        assert VALID_PASSWORD == "secret_sauce"
        assert BACKPACK == "Sauce Labs Backpack"
        assert BIKE_LIGHT == "Sauce Labs Bike Light"
        assert len(ALL_ITEMS) == 6
        assert DEFAULT_FIRST_NAME == "Test"
        assert INVENTORY_TITLE == "Products"
        assert LOGIN_ERROR_MISMATCH == "Username and password do not match"


class TestBasePageMethods:
    def test_all_core_methods_exist(self, mock_driver):
        from pages.base_page import BasePage

        page = BasePage(mock_driver)
        required = [
            "open_url",
            "get_title",
            "get_current_url",
            "click",
            "fill",
            "clear",
            "get_text",
            "is_displayed",
            "is_enabled",
            "wait_until_visible",
            "wait_until_clickable",
            "wait_until_hidden",
            "find_elements",
            "refresh_page",
            "navigate_back",
            "navigate_forward",
            "take_screenshot",
            "js_click",
            "js_scroll_to",
            "js_highlight",
            "switch_to_frame",
            "switch_to_default_content",
            "accept_alert",
            "dismiss_alert",
            "get_alert_text",
        ]
        for method in required:
            assert hasattr(page, method), f"BasePage missing method: {method}"


class TestPageMethodSignatures:
    def test_login_page_methods(self, mock_driver):
        from pages.login.login_page import LoginPage

        page = LoginPage(mock_driver)
        assert callable(page.open)
        assert callable(page.enter_username)
        assert callable(page.enter_password)
        assert callable(page.click_login)
        assert callable(page.login)
        assert callable(page.get_error_message)
        assert callable(page.close_error_message)
        assert callable(page.is_error_displayed)
        assert callable(page.get_title_text)
        result_open = page.open("https://example.com")
        assert result_open is page

    def test_inventory_page_methods(self, mock_driver):
        from pages.inventory.inventory_page import InventoryPage

        page = InventoryPage(mock_driver)
        assert callable(page.open)
        assert callable(page.get_item_elements)
        assert callable(page.get_item_names)
        assert callable(page.get_item_prices)
        assert callable(page.add_item_to_cart)
        assert callable(page.add_all_items_to_cart)
        assert callable(page.remove_item_from_cart)
        assert callable(page.get_cart_badge_count)
        assert callable(page.open_cart)
        assert callable(page.sort_by)
        assert callable(page.open_burger_menu)
        assert callable(page.close_burger_menu)
        assert callable(page.logout)
        assert callable(page.reset_app_state)
        assert callable(page.is_item_in_cart)
        assert callable(page.get_page_title)

    def test_cart_page_methods(self, mock_driver):
        from pages.cart.cart_page import CartPage

        page = CartPage(mock_driver)
        assert callable(page.open)
        assert callable(page.get_cart_items)
        assert callable(page.get_item_names)
        assert callable(page.get_item_prices)
        assert callable(page.get_item_quantities)
        assert callable(page.remove_item)
        assert callable(page.remove_all_items)
        assert callable(page.click_continue_shopping)
        assert callable(page.click_checkout)
        assert callable(page.get_item_count)
        assert callable(page.is_empty)

    def test_checkout_step_one_methods(self, mock_driver):
        from pages.checkout.checkout_step_one_page import CheckoutStepOnePage

        page = CheckoutStepOnePage(mock_driver)
        assert callable(page.open)
        assert callable(page.enter_first_name)
        assert callable(page.enter_last_name)
        assert callable(page.enter_postal_code)
        assert callable(page.fill_information)
        assert callable(page.click_continue)
        assert callable(page.click_cancel)
        assert callable(page.get_error_message)
        assert callable(page.is_error_displayed)
        assert callable(page.get_title_text)

    def test_checkout_step_two_methods(self, mock_driver):
        from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage

        page = CheckoutStepTwoPage(mock_driver)
        assert callable(page.open)
        assert callable(page.get_cart_items)
        assert callable(page.get_item_names)
        assert callable(page.get_item_prices)
        assert callable(page.get_item_quantities)
        assert callable(page.get_item_count)
        assert callable(page.get_payment_info)
        assert callable(page.get_shipping_info)
        assert callable(page.get_subtotal)
        assert callable(page.get_tax)
        assert callable(page.get_total)
        assert callable(page.click_finish)
        assert callable(page.click_cancel)
        assert callable(page.get_title_text)

    def test_checkout_flow_named_logins(self, mock_driver):
        from flows.login_flow import LoginFlow

        flow = LoginFlow(mock_driver, "https://example.com")
        assert callable(flow.login_as)
        assert callable(flow.login_as_standard_user)
        assert callable(flow.login_as_locked_out_user)
        assert callable(flow.login_as_problem_user)
        assert callable(flow.login_as_performance_glitch_user)
        assert callable(flow.login_as_error_user)
        assert callable(flow.login_as_visual_user)
        assert callable(flow.attempt_login)
        assert callable(flow.logout)
        assert callable(flow.dismiss_error)
        assert callable(flow.navigate_to_login)
        assert hasattr(flow, "error_message")
        assert hasattr(flow, "is_error_displayed")

    def test_cart_flow_methods(self, mock_driver):
        from flows.cart_flow import CartFlow

        flow = CartFlow(mock_driver)
        assert callable(flow.add_item)
        assert callable(flow.add_items)
        assert callable(flow.add_all_items)
        assert callable(flow.remove_item)
        assert callable(flow.remove_all_items)
        assert callable(flow.navigate_to_cart)
        assert callable(flow.navigate_to_inventory)
        assert callable(flow.proceed_to_checkout)
        assert hasattr(flow, "badge_count")
        assert hasattr(flow, "item_count")
        assert hasattr(flow, "item_names")
        assert hasattr(flow, "item_prices")
        assert hasattr(flow, "is_empty")

    def test_checkout_flow_methods(self, mock_driver):
        from flows.checkout_flow import CheckoutFlow

        flow = CheckoutFlow(mock_driver, "https://example.com")
        assert callable(flow.navigate_to_step_one)
        assert callable(flow.fill_shipping_information)
        assert callable(flow.fill_shipping_with_defaults)
        assert callable(flow.continue_to_overview)
        assert callable(flow.cancel_step_one)
        assert callable(flow.cancel_step_two)
        assert callable(flow.finish_order)
        assert callable(flow.complete_checkout)
        assert hasattr(flow, "error_message")
        assert hasattr(flow, "is_error_displayed")
        assert hasattr(flow, "item_count")
        assert hasattr(flow, "subtotal")
        assert hasattr(flow, "tax")
        assert hasattr(flow, "total")

    def test_flows_return_self_for_chaining(self, mock_driver):
        from flows.login_flow import LoginFlow
        from flows.cart_flow import CartFlow
        from flows.checkout_flow import CheckoutFlow

        login = LoginFlow(mock_driver)
        result = login.navigate_to_login()
        assert result is login

        cart = CartFlow(mock_driver)
        # add_item throws on mock because find_element returns a mock that
        # lacks proper .text, so only test non-IO methods
        result = cart.navigate_to_cart()
        assert result is cart

        checkout = CheckoutFlow(mock_driver)
        result = checkout.navigate_to_step_one()
        assert result is checkout

    def test_page_methods_return_self_for_chaining(self, mock_driver):
        from pages.login.login_page import LoginPage
        from pages.inventory.inventory_page import InventoryPage
        from pages.cart.cart_page import CartPage
        from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
        from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage

        for page_cls in [
            LoginPage,
            InventoryPage,
            CartPage,
            CheckoutStepOnePage,
            CheckoutStepTwoPage,
        ]:
            page = page_cls(mock_driver)
            if hasattr(page, "open"):
                result = page.open("https://example.com")
                assert result is page, f"{page_cls.__name__}.open() should return self"
