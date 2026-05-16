from typing import List, Optional

from flows.base_flow import BaseFlow
from flows.flow_utils import (
    DEFAULT_FIRST_NAME,
    DEFAULT_LAST_NAME,
    DEFAULT_POSTAL_CODE,
)
from pages.checkout.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout.checkout_step_two_page import CheckoutStepTwoPage


class CheckoutFlow(BaseFlow):
    """Business workflows for SauceDemo checkout (steps one and two).

    Orchestrates CheckoutStepOnePage and CheckoutStepTwoPage into
    reusable, chainable checkout operations.
    """

    def __init__(self, driver, base_url: str = "", timeout: int = 10):
        super().__init__(driver, base_url, timeout)
        self._step_one = CheckoutStepOnePage(driver, timeout)
        self._step_two = CheckoutStepTwoPage(driver, timeout)

    # ── Step One ──────────────────────────────────────────────────

    def navigate_to_step_one(self) -> "CheckoutFlow":
        self._step_one.open(self.base_url)
        return self

    def fill_shipping_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> "CheckoutFlow":
        self._step_one.fill_information(first_name, last_name, postal_code)
        return self

    def fill_shipping_with_defaults(self) -> "CheckoutFlow":
        self._step_one.fill_information(
            DEFAULT_FIRST_NAME, DEFAULT_LAST_NAME, DEFAULT_POSTAL_CODE
        )
        return self

    def continue_to_overview(self) -> "CheckoutFlow":
        self._step_one.click_continue()
        return self

    def cancel_step_one(self) -> "CheckoutFlow":
        self._step_one.click_cancel()
        return self

    def dismiss_error(self) -> "CheckoutFlow":
        if hasattr(self._step_one, "close_error_message"):
            self._step_one.close_error_message()
        return self

    # ── Step Two ──────────────────────────────────────────────────

    def finish_order(self) -> "CheckoutFlow":
        self._step_two.click_finish()
        return self

    def cancel_step_two(self) -> "CheckoutFlow":
        self._step_two.click_cancel()
        return self

    # ── Composite Flows ───────────────────────────────────────────

    def complete_checkout(
        self,
        first_name: str = DEFAULT_FIRST_NAME,
        last_name: str = DEFAULT_LAST_NAME,
        postal_code: str = DEFAULT_POSTAL_CODE,
    ) -> "CheckoutFlow":
        self.fill_shipping_information(first_name, last_name, postal_code)
        self.continue_to_overview()
        self.finish_order()
        return self

    # ── Queries ───────────────────────────────────────────────────

    @property
    def error_message(self) -> str:
        return self._step_one.get_error_message()

    @property
    def is_error_displayed(self) -> bool:
        return self._step_one.is_error_displayed()

    @property
    def item_count(self) -> int:
        return self._step_two.get_item_count()

    @property
    def item_names(self) -> List[str]:
        return self._step_two.get_item_names()

    @property
    def item_prices(self) -> List[float]:
        return self._step_two.get_item_prices()

    @property
    def item_quantities(self) -> List[int]:
        return self._step_two.get_item_quantities()

    @property
    def subtotal(self) -> str:
        return self._step_two.get_subtotal()

    @property
    def tax(self) -> str:
        return self._step_two.get_tax()

    @property
    def total(self) -> str:
        return self._step_two.get_total()

    @property
    def payment_info(self) -> str:
        return self._step_two.get_payment_info()

    @property
    def shipping_info(self) -> str:
        return self._step_two.get_shipping_info()

    @property
    def step_one_page(self) -> CheckoutStepOnePage:
        return self._step_one

    @property
    def step_two_page(self) -> CheckoutStepTwoPage:
        return self._step_two
