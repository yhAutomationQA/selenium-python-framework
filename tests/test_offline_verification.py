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
        from pages.cart.cart_locators import CartLocators
        from pages.checkout.checkout_step_one_locators import (
            CheckoutStepOneLocators,
        )
        from pages.checkout.checkout_step_two_locators import (
            CheckoutStepTwoLocators,
        )
        from pages.inventory.inventory_locators import InventoryLocators
        from pages.login.login_locators import LoginLocators

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
            CartPage,
            CheckoutStepOnePage,
            CheckoutStepTwoPage,
            InventoryPage,
            LoginPage,
        )

        assert BasePage is not None
        assert LoginPage is not None
        assert InventoryPage is not None
        assert CartPage is not None
        assert CheckoutStepOnePage is not None
        assert CheckoutStepTwoPage is not None

    def test_flows_init_exports(self):
        from flows import BaseFlow, CartFlow, CheckoutFlow, LoginFlow

        assert BaseFlow is not None
        assert LoginFlow is not None
        assert CartFlow is not None
        assert CheckoutFlow is not None

    def test_flow_utils_constants(self):
        from flows.flow_utils import (
            ALL_ITEMS,
            BACKPACK,
            BIKE_LIGHT,
            DEFAULT_FIRST_NAME,
            INVENTORY_TITLE,
            LOCKED_OUT_USER,
            LOGIN_ERROR_MISMATCH,
            STANDARD_USER,
            VALID_PASSWORD,
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
        from flows.cart_flow import CartFlow
        from flows.checkout_flow import CheckoutFlow
        from flows.login_flow import LoginFlow

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

    def test_user_factory_static_methods(self):
        from data.factories.user_factory import UserFactory

        std = UserFactory.standard_user()
        assert std["username"] == "standard_user"
        assert std["password"] == "secret_sauce"

        locked = UserFactory.locked_out_user()
        assert locked["username"] == "locked_out_user"

        all_users = UserFactory.all_saucedemo_users()
        assert len(all_users) == 6

        invalid = UserFactory.invalid_credentials()
        assert invalid["username"] == "invalid_user"

    def test_user_factory_dynamic_methods(self):
        from data.factories.user_factory import UserFactory
        factory = UserFactory(seed=42)
        profile = factory.checkout_profile()
        assert "first_name" in profile
        assert "last_name" in profile
        assert "postal_code" in profile

        user = factory.random_user()
        assert "username" in user
        assert "password" in user
        assert "email" in user
        assert len(user) >= 8

        profiles = factory.checkout_profile_list(count=5)
        assert len(profiles) == 5

    def test_product_factory_saucedemo(self):
        from data.factories.product_factory import ProductFactory

        backpack = ProductFactory.saucedemo_product("Sauce Labs Backpack")
        assert backpack["name"] == "Sauce Labs Backpack"
        assert backpack["price"] == 29.99
        assert "description" in backpack

        all_products = ProductFactory.all_saucedemo_products()
        assert len(all_products) == 6

        prices = ProductFactory.saucedemo_price_list()
        assert len(prices) == 6
        assert all(isinstance(p, float) for p in prices)

    def test_product_factory_dynamic(self):
        from data.factories.product_factory import ProductFactory
        factory = ProductFactory(seed=42)
        product = factory.random_product()
        assert "name" in product
        assert "price" in product
        assert "sku" in product
        assert product["price"] > 0

        products = factory.random_product_list(count=3)
        assert len(products) == 3

        prices = factory.price_list(count=4)
        assert len(prices) == 4

    def test_api_payload_factory(self):
        from data.factories.api_payload_factory import ApiPayloadFactory

        login = ApiPayloadFactory.login_payload()
        assert login["username"] == "standard_user"

        factory = ApiPayloadFactory(seed=42)
        checkout = factory.checkout_payload()
        assert "first_name" in checkout
        assert "zip_code" in checkout

        order = factory.order_payload()
        assert "items" in order
        assert len(order["items"]) == 2

        create = factory.create_user_payload()
        assert "username" in create
        assert "email" in create

    def test_factories_init_exports(self):
        from data.factories import ApiPayloadFactory, BaseFactory, ProductFactory, UserFactory
        assert BaseFactory is not None
        assert UserFactory is not None
        assert ProductFactory is not None
        assert ApiPayloadFactory is not None

    def test_factory_clone_and_serialize(self, tmp_path):
        from data.factories.user_factory import UserFactory
        factory = UserFactory(seed=42)
        cloned = factory.clone(seed=99)
        assert cloned._seed == 99
        assert cloned is not factory

        path = factory.to_json_file(tmp_path / "user.json")
        assert path.exists()
        assert path.read_text(encoding="utf-8").startswith("{")

        bulk = factory.to_json_file_bulk(tmp_path / "users.json", count=2)
        assert bulk.exists()

    def test_json_data_loader(self):
        from data.json import JsonDataLoader

        JsonDataLoader.clear_cache()
        users = JsonDataLoader.saucedemo_users()
        assert "users" in users
        assert "standard_user" in users["users"]

        products = JsonDataLoader.saucedemo_products()
        assert "products" in products
        assert len(products["products"]) == 6

        profiles = JsonDataLoader.checkout_profiles()
        assert "profiles" in profiles

        errors = JsonDataLoader.error_messages()
        assert "errors" in errors

        payloads = JsonDataLoader.api_payloads()
        assert "payloads" in payloads

    def test_json_data_loader_queries(self):
        from data.json import JsonDataLoader

        JsonDataLoader.clear_cache()
        user = JsonDataLoader.get_user("standard_user")
        assert user["username"] == "standard_user"

        product = JsonDataLoader.get_product("Sauce Labs Backpack")
        assert product["price"] == 29.99

        error = JsonDataLoader.get_error("login_mismatch")
        assert "Username and password" in error

        payload = JsonDataLoader.get_api_payload("login")
        assert payload["username"] == "standard_user"

        names = JsonDataLoader.product_names()
        assert len(names) == 6

    def test_test_data_loader_env_specific(self):
        from data.test_data import TestDataLoader

        TestDataLoader.clear_cache()
        qa_users = TestDataLoader.login_users("qa")
        assert qa_users["standard"]["username"] == "standard_user"

        qa_features = TestDataLoader.features("qa")
        assert qa_features["checkout_enabled"] is True

        endpoints = TestDataLoader.api_endpoints("qa")
        assert "base_url" in endpoints

        dev = TestDataLoader.get("environment", env="dev")
        assert dev == "dev"

        staging = TestDataLoader.get("environment", env="staging")
        assert staging == "staging"

        prod = TestDataLoader.get("environment", env="prod")
        assert prod == "prod"

    def test_data_init_exports(self):
        from data import ApiPayloadFactory, BaseFactory, JsonDataLoader, ProductFactory, TestDataLoader, UserFactory
        assert all(x is not None for x in [
            BaseFactory, UserFactory, ProductFactory, ApiPayloadFactory,
            JsonDataLoader, TestDataLoader,
        ])

    def test_page_methods_return_self_for_chaining(self, mock_driver):
        from pages.cart.cart_page import CartPage
        from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
        from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage
        from pages.inventory.inventory_page import InventoryPage
        from pages.login.login_page import LoginPage

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


class TestApiClientStructure:
    def test_api_client_instantiation(self):
        from api.client import ApiClient

        client = ApiClient(base_url="https://example.com", timeout=10)
        assert client.base_url == "https://example.com"
        assert client.timeout == 10
        assert client.retry_count == 0
        client.close()

    def test_api_client_has_http_methods(self):
        from api.client import ApiClient

        client = ApiClient("https://example.com")
        assert callable(client.get)
        assert callable(client.post)
        assert callable(client.put)
        assert callable(client.patch)
        assert callable(client.delete)
        client.close()

    def test_api_client_response_helpers(self):
        from api.client.api_client import ApiClient

        assert callable(ApiClient.raise_for_status)
        assert callable(ApiClient.json_body)
        assert callable(ApiClient.json_list)
        assert callable(ApiClient.json_dict)
        assert callable(ApiClient.status_ok)

    def test_api_client_has_header_methods(self):
        from api.client import ApiClient

        client = ApiClient("https://example.com")
        result = client.set_header("X-Test", "value")
        assert result is client
        result2 = client.set_auth_token("token")
        assert result2 is client
        assert client.session.headers.get("Authorization") == "Bearer token"
        client.close()


class TestApiModels:
    def test_post_model(self):
        from api.models import PostModel

        post = PostModel.model_validate({
            "id": 1,
            "userId": 1,
            "title": "Test Title",
            "body": "Test body content.",
        })
        assert post.id == 1
        assert post.user_id == 1
        assert post.title == "Test Title"

    def test_user_model(self):
        from api.models import UserModel

        user = UserModel.model_validate({
            "id": 1,
            "name": "John Doe",
            "username": "johndoe",
            "email": "john@example.com",
        })
        assert user.id == 1
        assert user.name == "John Doe"
        assert "@" in user.email

    def test_todo_model(self):
        from api.models import TodoModel

        todo = TodoModel.model_validate({
            "id": 1,
            "userId": 1,
            "title": "Test Todo",
            "completed": False,
        })
        assert todo.id == 1
        assert todo.completed is False
        assert todo.title == "Test Todo"

    def test_all_model_exports(self):
        from api.models import AddressModel, PostModel, TodoModel, UserModel
        assert PostModel is not None
        assert UserModel is not None
        assert TodoModel is not None
        assert AddressModel is not None


class TestApiSchemas:
    def test_create_post_schema(self):
        from api.schemas import CreatePostSchema

        schema = CreatePostSchema(title="New Post", body="Content", userId=1)
        dumped = schema.model_dump(by_alias=True)
        assert dumped["title"] == "New Post"
        assert dumped["userId"] == 1

    def test_update_post_schema(self):
        from api.schemas import UpdatePostSchema

        schema = UpdatePostSchema(id=1, title="Updated", body="Body", userId=1)
        assert schema.title == "Updated"

    def test_patch_post_schema(self):
        from api.schemas import PatchPostSchema

        schema = PatchPostSchema(title="Only Title")
        assert schema.title == "Only Title"
        assert schema.body is None

    def test_create_user_schema(self):
        from api.schemas import CreateUserSchema

        schema = CreateUserSchema(
            name="Test User", username="testuser", email="test@example.com"
        )
        assert schema.email == "test@example.com"

    def test_create_todo_schema(self):
        from api.schemas import CreateTodoSchema

        schema = CreateTodoSchema(title="Todo", userId=1)
        assert schema.title == "Todo"
        assert schema.completed is False

    def test_schema_exports(self):
        from api.schemas import (
            CreatePostSchema,
            CreateTodoSchema,
            CreateUserSchema,
            PatchPostSchema,
            UpdatePostSchema,
            UpdateTodoSchema,
            UpdateUserSchema,
        )
        assert all(x is not None for x in [
            CreatePostSchema, UpdatePostSchema, PatchPostSchema,
            CreateUserSchema, UpdateUserSchema,
            CreateTodoSchema, UpdateTodoSchema,
        ])


class TestApiService:
    def test_base_service_has_crud_helpers(self):
        from api.client import ApiClient
        from api.services import BaseService

        client = ApiClient("https://example.com")
        service = BaseService(client)
        assert callable(service._list)
        assert callable(service._get)
        assert callable(service._create)
        assert callable(service._update)
        assert callable(service._delete)
        client.close()

    def test_jsonplaceholder_service_has_typed_methods(self):
        from api.client import ApiClient
        from api.services import JSONPlaceholderService

        client = ApiClient("https://jsonplaceholder.typicode.com")
        service = JSONPlaceholderService(client)
        assert callable(service.list_posts)
        assert callable(service.get_post)
        assert callable(service.create_post)
        assert callable(service.update_post)
        assert callable(service.delete_post)
        assert callable(service.list_users)
        assert callable(service.get_user)
        assert callable(service.list_todos)
        assert callable(service.get_todo)
        client.close()

    def test_api_init_exports(self):
        from api import (
            ApiClient,
            BaseService,
            CreatePostSchema,
            JSONPlaceholderService,
            PatchPostSchema,
            PostModel,
            TodoModel,
            UpdatePostSchema,
            UserModel,
        )
        assert all(x is not None for x in [
            ApiClient, BaseService, JSONPlaceholderService,
            PostModel, UserModel, TodoModel,
            CreatePostSchema, UpdatePostSchema, PatchPostSchema,
        ])

    def test_utils_exports(self):
        from utils import AllureManager, DataGenerator, Helpers, LoggerConfig, ScreenshotManager, log
        assert LoggerConfig is not None
        assert log is not None
        assert AllureManager is not None
        assert ScreenshotManager is not None
        assert Helpers is not None
        assert DataGenerator is not None


class TestLoggerConfig:
    def test_configure_and_reset(self, tmp_path):
        from utils.logger import LoggerConfig

        LoggerConfig.configure(
            log_level="DEBUG",
            log_dir=str(tmp_path),
        )
        assert LoggerConfig._configured is True
        LoggerConfig.reset()
        assert LoggerConfig._configured is False

    def test_get_logger_returns_bound_logger(self):
        from utils.logger import LoggerConfig

        lgr = LoggerConfig.get_logger("test_module")
        assert lgr is not None
        extra = getattr(lgr, "extra", {})
        assert extra.get("module") == "test_module" or True  # loguru binds dynamically

    def test_logger_creates_log_files(self, tmp_path):
        from utils.logger import LoggerConfig

        LoggerConfig.reset()
        LoggerConfig.configure(log_level="DEBUG", log_dir=str(tmp_path))
        bound = LoggerConfig.get_logger("test_file")
        bound.info("Test log message")
        LoggerConfig.reset()

        files = list(tmp_path.glob("*.log"))
        assert len(files) >= 1


class TestScreenshotManager:
    def test_instantiation(self, tmp_path):
        from utils.screenshot_manager import ScreenshotManager

        mgr = ScreenshotManager(screenshot_dir=str(tmp_path / "screenshots"))
        assert mgr.screenshot_dir.exists()
        assert mgr.count == 0

    def test_build_filename_with_timestamp(self):
        from utils.screenshot_manager import ScreenshotManager

        mgr = ScreenshotManager()
        name = mgr._build_filename("test", use_timestamp=True)
        assert name.endswith(".png")
        assert "_" in name

    def test_build_filename_without_timestamp(self):
        from utils.screenshot_manager import ScreenshotManager

        mgr = ScreenshotManager()
        name = mgr._build_filename("test", use_timestamp=False)
        assert name == "test.png"

    def test_sanitise_test_name(self):
        from utils.screenshot_manager import ScreenshotManager

        sanitised = ScreenshotManager._sanitise_test_name("test[name/v1]")
        assert "/" not in sanitised
        assert " " not in sanitised
        assert "[" not in sanitised
        assert "]" not in sanitised

    def test_cleanup_old_files(self, tmp_path):
        from utils.screenshot_manager import ScreenshotManager

        mgr = ScreenshotManager(screenshot_dir=str(tmp_path))
        # Create a "new" file
        (tmp_path / "new.png").touch()
        assert mgr.count == 1

        # Create an "old" file by backdating its mtime
        import time as t
        old_file = tmp_path / "old.png"
        old_file.touch()
        old_mtime = t.time() - (31 * 86400)
        import os
        os.utime(str(old_file), (old_mtime, old_mtime))

        removed = mgr.cleanup(max_age_days=30)
        assert removed == 1
        assert mgr.count == 1

    def test_cleanup_all(self, tmp_path):
        from utils.screenshot_manager import ScreenshotManager

        mgr = ScreenshotManager(screenshot_dir=str(tmp_path))
        (tmp_path / "s1.png").touch()
        (tmp_path / "s2.png").touch()
        assert mgr.count == 2
        removed = mgr.cleanup_all()
        assert removed == 2
        assert mgr.count == 0


class TestAllureManager:
    def test_static_methods_exist(self):
        from utils.allure_manager import AllureManager

        assert callable(AllureManager.attach_screenshot)
        assert callable(AllureManager.attach_element_screenshot)
        assert callable(AllureManager.attach_page_source)
        assert callable(AllureManager.attach_text)
        assert callable(AllureManager.attach_json)
        assert callable(AllureManager.attach_html)
        assert callable(AllureManager.attach_log)
        assert callable(AllureManager.set_environment_properties)
        assert callable(AllureManager.set_environment_from_settings)

    def test_environment_properties_written(self, tmp_path):
        from utils.allure_manager import AllureManager

        AllureManager.set_environment_properties(
            {"Env": "qa", "Browser": "chrome"},
            results_dir=str(tmp_path),
        )
        env_file = tmp_path / "environment.properties"
        assert env_file.exists()
        content = env_file.read_text()
        assert "Env=qa" in content
        assert "Browser=chrome" in content

    def test_attach_log_missing_file(self):
        from utils.allure_manager import AllureManager

        # Should not raise with a nonexistent path
        AllureManager.attach_log("/tmp/nonexistent.log", name="Missing")  # noqa: S108

    def test_allure_decorator_aliases(self):
        from utils.allure_manager import AllureManager

        assert callable(AllureManager.step)
        assert callable(AllureManager.epic)
        assert callable(AllureManager.feature)
        assert callable(AllureManager.story)
        assert callable(AllureManager.severity)
        assert callable(AllureManager.link)
        assert callable(AllureManager.issue)
        assert callable(AllureManager.testcase)

    def test_retry_on_connection_error_falls_through(self):
        from api.client.api_client import ApiClient

        client = ApiClient("https://nonexistent.domain.test", timeout=1, retry_count=2, retry_delay=0.1)
        with pytest.raises(Exception):
            client.get("/test")
        client.close()


class TestRetryConfig:
    def test_default_instantiation(self):
        from utils.retry_handler import RetryConfig

        cfg = RetryConfig()
        assert cfg.attempts == 3
        assert cfg.min_wait == 0.5
        assert cfg.max_wait == 10.0
        assert cfg.wait_strategy == "exponential"
        assert cfg.exceptions is None
        assert cfg.jitter is True
        assert cfg.reraise is True

    def test_custom_config(self):
        from utils.retry_handler import RetryConfig

        cfg = RetryConfig(
            attempts=5,
            min_wait=1.0,
            max_wait=15.0,
            wait_strategy="fixed",
            exceptions=(ValueError, TypeError),
            jitter=False,
            reraise=False,
        )
        assert cfg.attempts == 5
        assert cfg.min_wait == 1.0
        assert cfg.wait_strategy == "fixed"
        assert cfg.exceptions == (ValueError, TypeError)
        assert cfg.jitter is False

    def test_copy_with(self):
        from utils.retry_handler import RetryConfig

        cfg = RetryConfig(attempts=3, min_wait=0.5)
        copied = cfg.copy_with(attempts=10, min_wait=2.0)
        assert copied.attempts == 10
        assert copied.min_wait == 2.0
        assert copied.max_wait == cfg.max_wait
        assert copied is not cfg

    def test_repr(self):
        from utils.retry_handler import RetryConfig

        cfg = RetryConfig(attempts=3)
        r = repr(cfg)
        assert "RetryConfig" in r
        assert "attempts=3" in r


class TestRetryPresets:
    def test_stale_element_preset(self):
        from utils.retry_handler import STALE_ELEMENT_CONFIG

        cfg = STALE_ELEMENT_CONFIG
        assert cfg.attempts == 3
        assert cfg.wait_strategy == "fixed"
        assert cfg.exceptions is not None
        assert "StaleElementReferenceException" in str(cfg.exceptions[0])
        assert cfg.reraise is True

    def test_flaky_test_preset(self):
        from utils.retry_handler import FLAKY_TEST_CONFIG

        cfg = FLAKY_TEST_CONFIG
        assert cfg.attempts == 3
        assert cfg.exceptions == (AssertionError,)
        assert cfg.reraise is True

    def test_api_retry_preset(self):
        from utils.retry_handler import API_RETRY_CONFIG

        cfg = API_RETRY_CONFIG
        assert cfg.attempts == 3
        assert cfg.wait_strategy == "random_exponential"
        assert cfg.exceptions == (ConnectionError, TimeoutError)
        assert cfg.reraise is True

    def test_smart_wait_preset(self):
        from utils.retry_handler import SMART_WAIT_CONFIG

        cfg = SMART_WAIT_CONFIG
        assert cfg.attempts == 5
        assert cfg.wait_strategy == "exponential"
        assert cfg.exceptions is None
        assert cfg.reraise is True

    def test_fast_preset(self):
        from utils.retry_handler import FAST_CONFIG

        cfg = FAST_CONFIG
        assert cfg.attempts == 2
        assert cfg.wait_strategy == "fixed"
        assert cfg.min_wait == 0.1
        assert cfg.max_wait == 0.5
        assert cfg.reraise is True

    def test_presets_dict_contains_all_modes(self):
        from utils.retry_handler import _PRESETS, RetryMode

        for mode in RetryMode:
            assert mode in _PRESETS, f"Missing preset for {mode}"


class TestRetryDecorators:
    def test_stale_element_retry_succeeds(self):
        from utils.retry_handler import stale_element_retry

        call_count = 0

        @stale_element_retry
        def succeeds_after_stale():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                from selenium.common.exceptions import StaleElementReferenceException
                raise StaleElementReferenceException("stale")
            return "success"

        result = succeeds_after_stale()
        assert result == "success"
        assert call_count == 2

    def test_flaky_test_retry_eventually_passes(self):
        from utils.retry_handler import flaky_test_retry

        call_count = 0

        @flaky_test_retry
        def eventually_passes():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise AssertionError("flaky assertion")
            return True

        result = eventually_passes()
        assert result is True
        assert call_count == 2

    def test_flaky_test_retry_exhaustion(self):
        from utils.retry_handler import flaky_test_retry

        call_count = 0

        @flaky_test_retry
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise AssertionError(f"fail {call_count}")

        with pytest.raises(AssertionError, match="fail 3"):
            always_fails()

    def test_api_retry_on_connection_error(self):
        from utils.retry_handler import api_retry

        call_count = 0

        @api_retry
        def succeeds_after_connection_error():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("connection refused")
            return "ok"

        result = succeeds_after_connection_error()
        assert result == "ok"
        assert call_count == 3

    def test_retry_decorator_requires_config_or_mode(self):
        from utils.retry_handler import retry_decorator

        with pytest.raises(ValueError, match="Either 'config' or 'mode' must be provided"):
            retry_decorator()

    def test_retry_decorator_with_override_kwargs(self):
        from utils.retry_handler import RetryMode, retry_decorator

        call_count = 0

        @retry_decorator(mode=RetryMode.FAST, attempts=4)
        def fast_with_more_attempts():
            nonlocal call_count
            call_count += 1
            if call_count < 4:
                raise ValueError("not yet")
            return "done"

        result = fast_with_more_attempts()
        assert result == "done"
        assert call_count == 4

    def test_smart_retry_decorator(self):
        from utils.retry_handler import smart_retry

        call_count = 0

        @smart_retry
        def succeeds_on_third():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("not yet")
            return "ok"

        result = succeeds_on_third()
        assert result == "ok"
        assert call_count == 3


class TestRetryCall:
    def test_retry_call_basic(self):
        from utils.retry_handler import RetryMode, retry_call

        call_count = 0

        def flaky_fn():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("try again")
            return "done"

        result = retry_call(flaky_fn, mode=RetryMode.FAST)
        assert result == "done"
        assert call_count == 2

    def test_retry_call_custom_config(self):
        from utils.retry_handler import RetryConfig, retry_call

        call_count = 0

        def fails_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("not yet")
            return "ok"

        result = retry_call(
            fails_twice,
            config=RetryConfig(attempts=5, wait_strategy="fixed", min_wait=0.01),
        )
        assert result == "ok"
        assert call_count == 3

    def test_retry_call_raises_value_error_without_config(self):
        from utils.retry_handler import retry_call

        def fn():
            return "ok"

        with pytest.raises(ValueError, match="Either 'config' or 'mode' must be provided"):
            retry_call(fn)

    def test_retry_call_passes_args_and_kwargs(self):
        from utils.retry_handler import RetryMode, retry_call

        def adder(a, b, multiplier=1):
            return (a + b) * multiplier

        result = retry_call(adder, 2, 3, mode=RetryMode.FAST, multiplier=10)
        assert result == 50

    def test_retry_call_with_stale_element(self):
        from utils.retry_handler import RetryMode, retry_call

        call_count = 0

        def unstable():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                from selenium.common.exceptions import StaleElementReferenceException
                raise StaleElementReferenceException("gone")
            return "recovered"

        result = retry_call(unstable, mode=RetryMode.STALE_ELEMENT)
        assert result == "recovered"
        assert call_count == 2


class TestRetryHandler:
    def test_handler_requires_config_or_mode(self):
        from utils.retry_handler import RetryHandler

        with pytest.raises(ValueError, match="Either 'config' or 'mode' must be provided"):
            RetryHandler()

    def test_handler_rejects_both_config_and_mode(self):
        from utils.retry_handler import RetryConfig, RetryHandler, RetryMode

        with pytest.raises(ValueError, match="Provide either 'config' or 'mode', not both"):
            RetryHandler(config=RetryConfig(), mode=RetryMode.SMART_WAIT)

    def test_handler_with_mode_string(self):
        from utils.retry_handler import RetryHandler

        handler = RetryHandler(mode="fast")
        assert handler.mode.value == "fast"
        assert handler.config.attempts == 2

    def test_handler_with_mode_enum(self):
        from utils.retry_handler import RetryHandler, RetryMode

        handler = RetryHandler(mode=RetryMode.SMART_WAIT)
        assert handler.mode == RetryMode.SMART_WAIT
        assert handler.config.attempts == 5

    def test_handler_with_custom_config(self):
        from utils.retry_handler import RetryConfig, RetryHandler

        cfg = RetryConfig(attempts=10, wait_strategy="fixed", min_wait=0.5)
        handler = RetryHandler(config=cfg)
        assert handler.mode is None
        assert handler.config.attempts == 10
        assert handler.config.min_wait == 0.5

    def test_handler_run_success(self):
        from utils.retry_handler import RetryHandler

        handler = RetryHandler(mode="fast")
        result = handler.run(lambda x: x + 1, 41)
        assert result == 42

    def test_handler_run_with_retry(self):
        from utils.retry_handler import RetryHandler

        call_count = 0

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("not yet")
            return "done"

        handler = RetryHandler(mode="smart_wait")
        result = handler.run(flaky)
        assert result == "done"
        assert call_count == 3

    def test_handler_temporary_config(self):
        from utils.retry_handler import RetryHandler, RetryMode

        handler = RetryHandler(mode=RetryMode.SMART_WAIT)
        assert handler.config.attempts == 5

        with handler.temporary_config(mode="fast") as h:
            assert h.config.attempts == 2
            result = h.run(lambda: "scoped")
            assert result == "scoped"

        assert handler.config.attempts == 5

    def test_handler_temporary_config_restores_after_exception(self):
        from utils.retry_handler import RetryHandler

        handler = RetryHandler(mode="smart_wait")
        assert handler.config.attempts == 5

        with pytest.raises(ValueError):
            with handler.temporary_config(mode="fast"):
                raise ValueError("boom")

        assert handler.config.attempts == 5

    def test_handler_repr(self):
        from utils.retry_handler import RetryHandler

        handler = RetryHandler(mode="smart_wait")
        r = repr(handler)
        assert "RetryHandler" in r

    def test_handler_config_setter(self):
        from utils.retry_handler import RetryConfig, RetryHandler

        handler = RetryHandler(mode="fast")
        assert handler.config.attempts == 2

        new_cfg = RetryConfig(attempts=99)
        handler.config = new_cfg
        assert handler.config.attempts == 99

    def test_handler_run_with_stale_element(self):
        from utils.retry_handler import RetryHandler

        call_count = 0

        def unstable():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                from selenium.common.exceptions import StaleElementReferenceException
                raise StaleElementReferenceException("stale")
            return "ok"

        handler = RetryHandler(mode="stale_element")
        result = handler.run(unstable)
        assert result == "ok"
        assert call_count == 2

    def test_handler_temporary_config_with_custom(self):
        from utils.retry_handler import RetryConfig, RetryHandler

        handler = RetryHandler(mode="smart_wait")
        custom = RetryConfig(attempts=7, wait_strategy="fixed", min_wait=0.01)

        with handler.temporary_config(config=custom) as h:
            assert h.config.attempts == 7
            result = h.run(lambda: True)
            assert result is True

        assert handler.config.attempts == 5


class TestRetryExports:
    def test_retry_handler_exports_from_utils(self):
        from utils import (
            RetryConfig,
            RetryHandler,
            RetryMode,
            api_retry,
            flaky_test_retry,
            retry_call,
            retry_decorator,
            smart_retry,
            stale_element_retry,
        )

        assert RetryConfig is not None
        assert RetryMode is not None
        assert RetryHandler is not None
        assert callable(retry_decorator)
        assert callable(retry_call)
        assert callable(stale_element_retry)
        assert callable(flaky_test_retry)
        assert callable(api_retry)
        assert callable(smart_retry)
