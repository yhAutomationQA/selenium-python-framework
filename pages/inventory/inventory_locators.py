from selenium.webdriver.common.by import By


class InventoryLocators:
    ITEM = (By.CSS_SELECTOR, "[data-test='inventory-item'], .inventory_item")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name'], .inventory_item_name")
    ITEM_DESC = (By.CSS_SELECTOR, ".inventory_item_desc, [data-test='inventory-item-desc']")
    ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price, [data-test='inventory-item-price']")
    ITEM_IMAGE = (By.CSS_SELECTOR, ".inventory_item_img, img.inventory_item_img")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test^='add-to-cart'], .btn_inventory.btn_primary")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test^='remove'], .btn_inventory.btn_secondary")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container'], .product_sort_container")
    SHOPPING_CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge, [data-test='shopping-cart-badge']")
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link, [data-test='shopping-cart-link']")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    BURGER_MENU = (By.CSS_SELECTOR, ".bm-menu, .bm-menu-wrap")
    LOGOUT_SIDEBAR_LINK = (By.ID, "logout_sidebar_link")
    ALL_ITEMS_SIDEBAR_LINK = (By.ID, "inventory_sidebar_link")
    ABOUT_SIDEBAR_LINK = (By.ID, "about_sidebar_link")
    RESET_SIDEBAR_LINK = (By.ID, "reset_sidebar_link")
    CLOSE_MENU_BUTTON = (By.ID, "react-burger-cross-btn")
    TITLE = (By.CSS_SELECTOR, ".title, [data-test='title']")
    FOOTER = (By.CSS_SELECTOR, ".footer, footer")
