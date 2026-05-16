import pytest

from flows.flow_utils import (
    STANDARD_USER,
    LOCKED_OUT_USER,
    VALID_PASSWORD,
    LOGIN_ERROR_MISMATCH,
    LOGIN_ERROR_LOCKED,
    LOGIN_ERROR_USERNAME_REQUIRED,
    LOGIN_ERROR_PASSWORD_REQUIRED,
    INVENTORY_TITLE,
)
from flows.login_flow import LoginFlow

pytestmark = [pytest.mark.ui, pytest.mark.smoke]


class TestLoginPositive:
    def test_valid_login(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.login_as_standard_user()
        assert flow.current_page.get_title_text() == INVENTORY_TITLE

    def test_logout(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.login_as_standard_user().logout()
        assert "inventory" not in driver.current_url

    @pytest.mark.negative
    def test_empty_username(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.navigate_to_login().attempt_login("", VALID_PASSWORD)
        assert flow.is_error_displayed
        assert LOGIN_ERROR_USERNAME_REQUIRED in flow.error_message

    @pytest.mark.negative
    def test_empty_password(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.navigate_to_login().attempt_login(STANDARD_USER, "")
        assert flow.is_error_displayed
        assert LOGIN_ERROR_PASSWORD_REQUIRED in flow.error_message


class TestLoginNegative:
    @pytest.mark.negative
    def test_invalid_credentials(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.attempt_login("invalid_user", "bad_password")
        assert flow.is_error_displayed
        assert LOGIN_ERROR_MISMATCH in flow.error_message

    @pytest.mark.negative
    def test_locked_out_user(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.login_as_locked_out_user()
        assert flow.is_error_displayed
        assert LOGIN_ERROR_LOCKED.lower() in flow.error_message.lower()

    @pytest.mark.negative
    def test_error_dismissal(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.attempt_login("invalid_user", "bad_password")
        assert flow.is_error_displayed
        flow.dismiss_error()
        assert not flow.is_error_displayed
