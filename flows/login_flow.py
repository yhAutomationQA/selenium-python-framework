from flows.base_flow import BaseFlow
from flows.flow_utils import (
    ERROR_USER,
    LOCKED_OUT_USER,
    PERFORMANCE_GLITCH_USER,
    PROBLEM_USER,
    STANDARD_USER,
    VALID_PASSWORD,
    VISUAL_USER,
)
from pages.inventory.inventory_page import InventoryPage
from pages.login.login_page import LoginPage


class LoginFlow(BaseFlow):
    """Business workflows for SauceDemo authentication.

    Orchestrates LoginPage and InventoryPage (logout) into
    reusable test-level steps.
    """

    def __init__(self, driver, base_url: str = "", timeout: int = 10):
        super().__init__(driver, base_url, timeout)
        self._login_page = LoginPage(driver, timeout)
        self._inventory_page = InventoryPage(driver, timeout)

    # ── Navigation ────────────────────────────────────────────────

    def navigate_to_login(self) -> "LoginFlow":
        self._login_page.open(self.base_url)
        return self

    # ── Named User Logins ─────────────────────────────────────────

    def login_as(self, username: str, password: str = VALID_PASSWORD) -> "LoginFlow":
        self._login_page.open(self.base_url).login(username, password)
        return self

    def login_as_standard_user(self) -> "LoginFlow":
        return self.login_as(STANDARD_USER)

    def login_as_locked_out_user(self) -> "LoginFlow":
        return self.login_as(LOCKED_OUT_USER)

    def login_as_problem_user(self) -> "LoginFlow":
        return self.login_as(PROBLEM_USER)

    def login_as_performance_glitch_user(self) -> "LoginFlow":
        return self.login_as(PERFORMANCE_GLITCH_USER)

    def login_as_error_user(self) -> "LoginFlow":
        return self.login_as(ERROR_USER)

    def login_as_visual_user(self) -> "LoginFlow":
        return self.login_as(VISUAL_USER)

    # ── Auth Actions ──────────────────────────────────────────────

    def attempt_login(self, username: str, password: str = VALID_PASSWORD) -> "LoginFlow":
        self._login_page.open(self.base_url).enter_username(username).enter_password(
            password
        ).click_login()
        return self

    def logout(self) -> "LoginFlow":
        self._inventory_page.logout()
        return self

    def dismiss_error(self) -> "LoginFlow":
        self._login_page.close_error_message()
        return self

    # ── Queries ───────────────────────────────────────────────────

    @property
    def error_message(self) -> str:
        return self._login_page.get_error_message()

    @property
    def is_error_displayed(self) -> bool:
        return self._login_page.is_error_displayed()

    @property
    def current_page(self) -> LoginPage:
        return self._login_page

    @property
    def is_logged_in(self) -> bool:
        return "inventory" in self.driver.current_url
