"""Shared flow constants, credentials, and product data for SauceDemo flows."""

# ── SauceDemo Users ──────────────────────────────────────────────
STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
PERFORMANCE_GLITCH_USER = "performance_glitch_user"
ERROR_USER = "error_user"
VISUAL_USER = "visual_user"
VALID_PASSWORD = "secret_sauce"

ALL_USERS = [
    STANDARD_USER,
    LOCKED_OUT_USER,
    PROBLEM_USER,
    PERFORMANCE_GLITCH_USER,
    ERROR_USER,
    VISUAL_USER,
]

# ── Product Names ─────────────────────────────────────────────────
BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
BOLT_TSHIRT = "Sauce Labs Bolt T-Shirt"
FLEECE_JACKET = "Sauce Labs Fleece Jacket"
ONESIE = "Sauce Labs Onesie"
RED_TSHIRT = "Test.allTheThings() T-Shirt (Red)"

ALL_ITEMS = [BACKPACK, BIKE_LIGHT, BOLT_TSHIRT, FLEECE_JACKET, ONESIE, RED_TSHIRT]

# ── Checkout Defaults ─────────────────────────────────────────────
DEFAULT_FIRST_NAME = "Test"
DEFAULT_LAST_NAME = "User"
DEFAULT_POSTAL_CODE = "12345"

# ── Expected Error Messages ───────────────────────────────────────
LOGIN_ERROR_MISMATCH = "Username and password do not match"
LOGIN_ERROR_LOCKED = "Sorry, this user has been locked out"
LOGIN_ERROR_USERNAME_REQUIRED = "Username is required"
LOGIN_ERROR_PASSWORD_REQUIRED = "Password is required"
CHECKOUT_ERROR_FIRST_NAME = "First Name is required"
CHECKOUT_ERROR_LAST_NAME = "Last Name is required"
CHECKOUT_ERROR_POSTAL_CODE = "Postal Code is required"

# ── Page Titles ───────────────────────────────────────────────────
INVENTORY_TITLE = "Products"
CHECKOUT_STEP_ONE_TITLE = "Checkout: Your Information"
CHECKOUT_STEP_TWO_TITLE = "Checkout: Overview"
CART_TITLE = "Your Cart"
