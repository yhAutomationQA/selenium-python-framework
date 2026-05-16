from selenium.webdriver.common.by import By


class CheckoutStepTwoLocators:
    TITLE = (By.CSS_SELECTOR, ".title, [data-test='title']")
    CART_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item'], .cart_item")
    CART_ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name'], .inventory_item_name")
    CART_ITEM_DESC = (By.CSS_SELECTOR, ".inventory_item_desc, [data-test='inventory-item-desc']")
    CART_ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price, [data-test='inventory-item-price']")
    CART_ITEM_QUANTITY = (By.CSS_SELECTOR, ".cart_quantity, [data-test='item-quantity']")
    PAYMENT_INFO_LABEL = (By.CSS_SELECTOR, ".summary_info_label")
    PAYMENT_INFO_VALUE = (By.CSS_SELECTOR, ".summary_value_label")
    SUBTOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label, [data-test='subtotal-label']")
    TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label, [data-test='tax-label']")
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label, [data-test='total-label']")
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish'], #finish")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel'], #cancel")
