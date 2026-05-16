from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.login.login_locators import LoginLocators


class LoginPage(BasePage):
    """Represents the SauceDemo login page.

    Provides UI interaction methods for the login flow without
    assertions or business logic.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        super().__init__(driver, timeout)
        self._locators = LoginLocators()

    def open(self, base_url: str = "") -> "LoginPage":
        """Navigate to the login page base URL.

        Args:
            base_url: The base URL of the application.
        """
        self.open_url(base_url)
        self.wait_until_visible(self._locators.LOGIN_BUTTON)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Type the username into the username field.

        Args:
            username: The username string to enter.
        """
        self.fill(self._locators.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Type the password into the password field.

        Args:
            password: The password string to enter.
        """
        self.fill(self._locators.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> "LoginPage":
        """Click the login button."""
        self.click(self._locators.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Perform a complete login flow: enter credentials and submit.

        Args:
            username: The username string.
            password: The password string.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self) -> str:
        """Return the visible login error text, or empty string if none."""
        if self.is_displayed(self._locators.ERROR_TEXT):
            return self.get_text(self._locators.ERROR_TEXT)
        return ""

    def close_error_message(self) -> "LoginPage":
        """Dismiss the error message by clicking the close button."""
        if self.is_displayed(self._locators.ERROR_CLOSE_BUTTON):
            self.click(self._locators.ERROR_CLOSE_BUTTON)
            self.wait_until_hidden(self._locators.ERROR_CONTAINER)
        return self

    def is_error_displayed(self) -> bool:
        """Check whether the error message container is visible."""
        return self.is_displayed(self._locators.ERROR_CONTAINER)

    def get_title_text(self) -> str:
        """Return the page title text."""
        return self.get_title()
