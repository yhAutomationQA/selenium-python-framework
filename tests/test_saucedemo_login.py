import pytest
from pages.login.login_page import LoginPage
from pages.inventory.inventory_page import InventoryPage

pytestmark = [pytest.mark.ui, pytest.mark.smoke]

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
LOCKED_USER = "locked_out_user"
INVALID_USER = "invalid_user"
INVALID_PASS = "wrong_password"


class TestLoginPositive:
    def test_valid_login(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open(base_url).login(VALID_USER, VALID_PASS)
        assert InventoryPage(driver).get_page_title() == "Products"

    def test_logout(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open(base_url).login(VALID_USER, VALID_PASS)
        InventoryPage(driver).logout()
        assert "inventory" not in driver.current_url

    @pytest.mark.negative
    def test_empty_username(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open(base_url).enter_password(VALID_PASS).click_login()
        assert login_page.is_error_displayed()
        assert "Username is required" in login_page.get_error_message()

    @pytest.mark.negative
    def test_empty_password(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open(base_url).enter_username(VALID_USER).click_login()
        assert login_page.is_error_displayed()
        assert "Password is required" in login_page.get_error_message()


class TestLoginNegative:
    @pytest.mark.negative
    def test_invalid_credentials(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open(base_url).login(INVALID_USER, INVALID_PASS)
        assert login_page.is_error_displayed()
        assert "Username and password do not match" in login_page.get_error_message()

    @pytest.mark.negative
    def test_locked_out_user(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open(base_url).login(LOCKED_USER, VALID_PASS)
        assert login_page.is_error_displayed()
        assert "locked out" in login_page.get_error_message().lower()

    @pytest.mark.negative
    def test_error_dismissal(self, driver, base_url):
        login_page = LoginPage(driver)
        login_page.open(base_url).login(INVALID_USER, INVALID_PASS)
        assert login_page.is_error_displayed()
        login_page.close_error_message()
        assert not login_page.is_error_displayed()
