from typing import Any, Dict, List, Optional

from data.factories.base_factory import BaseFactory
from flows.flow_utils import (
    ERROR_USER,
    LOCKED_OUT_USER,
    PERFORMANCE_GLITCH_USER,
    PROBLEM_USER,
    STANDARD_USER,
    VALID_PASSWORD,
    VISUAL_USER,
)


class UserFactory(BaseFactory):
    """Generates user-related test data.

    Covers SauceDemo credentials, checkout/shipping profiles,
    and random customer data for broader tests.
    """

    # ── SauceDemo Users ───────────────────────────────────────────

    @staticmethod
    def standard_user() -> Dict[str, str]:
        return {"username": STANDARD_USER, "password": VALID_PASSWORD}

    @staticmethod
    def locked_out_user() -> Dict[str, str]:
        return {"username": LOCKED_OUT_USER, "password": VALID_PASSWORD}

    @staticmethod
    def problem_user() -> Dict[str, str]:
        return {"username": PROBLEM_USER, "password": VALID_PASSWORD}

    @staticmethod
    def performance_glitch_user() -> Dict[str, str]:
        return {"username": PERFORMANCE_GLITCH_USER, "password": VALID_PASSWORD}

    @staticmethod
    def error_user() -> Dict[str, str]:
        return {"username": ERROR_USER, "password": VALID_PASSWORD}

    @staticmethod
    def visual_user() -> Dict[str, str]:
        return {"username": VISUAL_USER, "password": VALID_PASSWORD}

    @staticmethod
    def all_saucedemo_users() -> List[Dict[str, str]]:
        return [
            UserFactory.standard_user(),
            UserFactory.locked_out_user(),
            UserFactory.problem_user(),
            UserFactory.performance_glitch_user(),
            UserFactory.error_user(),
            UserFactory.visual_user(),
        ]

    # ── Checkout / Shipping Profiles ──────────────────────────────

    def checkout_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        postal_code: Optional[str] = None,
    ) -> Dict[str, str]:
        return {
            "first_name": first_name or self.faker.first_name(),
            "last_name": last_name or self.faker.last_name(),
            "postal_code": postal_code or self.faker.zipcode(),
        }

    def checkout_profile_list(self, count: int = 3) -> List[Dict[str, str]]:
        return [self.checkout_profile() for _ in range(count)]

    # ── Random Customer Data ──────────────────────────────────────

    def random_user(self, **overrides: Any) -> Dict[str, str]:
        data = {
            "username": self.faker.user_name(),
            "password": self.faker.password(length=12),
            "email": self.faker.email(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "phone": self.faker.phone_number(),
            "address": self.faker.street_address(),
            "city": self.faker.city(),
            "state": self.faker.state(),
            "postal_code": self.faker.zipcode(),
            "country": self.faker.country(),
        }
        data.update(overrides)
        return data

    def json(self, **overrides: Any) -> Dict[str, Any]:
        return self.random_user(**overrides)

    # ── Invalid / Edge-Case Data ──────────────────────────────────

    @staticmethod
    def invalid_credentials() -> Dict[str, str]:
        return {"username": "invalid_user", "password": "wrong_password"}

    @staticmethod
    def empty_credentials() -> Dict[str, str]:
        return {"username": "", "password": ""}
