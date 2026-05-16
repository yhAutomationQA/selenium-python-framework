from selenium.webdriver.common.by import By


class CartLocators:
    CART_ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item'], .cart_item")
    CART_ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name'], .inventory_item_name")
    CART_ITEM_DESC = (By.CSS_SELECTOR, ".inventory_item_desc, [data-test='inventory-item-desc']")
    CART_ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price, [data-test='inventory-item-price']")
    CART_ITEM_QUANTITY = (By.CSS_SELECTOR, ".cart_quantity, [data-test='item-quantity']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test^='remove'], .cart_button")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "[data-test='continue-shopping'], #continue-shopping")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout'], #checkout")
    CART_TITLE = (By.CSS_SELECTOR, ".title, [data-test='title']")
    CART_EMPTY_TEXT = (By.CSS_SELECTOR, ".cart_empty, [data-test='cart-empty']")
    SUBTOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label, [data-test='subtotal-label']")
