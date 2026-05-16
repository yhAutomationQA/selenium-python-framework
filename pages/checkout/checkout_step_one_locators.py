from selenium.webdriver.common.by import By


class CheckoutStepOneLocators:
    TITLE = (By.CSS_SELECTOR, ".title, [data-test='title']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='firstName'], #first-name")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='lastName'], #last-name")
    POSTAL_CODE_INPUT = (By.CSS_SELECTOR, "[data-test='postalCode'], #postal-code")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue'], #continue")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel'], #cancel")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error'], .error-message-container")
    ERROR_TEXT = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CSS_SELECTOR, ".error-button")
