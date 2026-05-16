from selenium.webdriver.common.by import By


class LoginLocators:
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-test='username'], #user-name")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='password'], #password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button'], #login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error'], .error-message-container")
    ERROR_TEXT = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CSS_SELECTOR, ".error-button")
    LOGIN_LOGO = (By.CSS_SELECTOR, ".login_logo, .bot_column")
    LOGIN_CREDENTIALS = (By.CSS_SELECTOR, ".login_credentials, #login_credentials")
    LOGIN_PASSWORD_HINT = (By.CSS_SELECTOR, ".login_password, #login_password")
