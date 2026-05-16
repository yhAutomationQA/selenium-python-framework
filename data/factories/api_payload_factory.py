from typing import Any, Dict, List, Optional

from data.factories.base_factory import BaseFactory


class ApiPayloadFactory(BaseFactory):
    """Generates API request payloads for service-level and integration tests.

    Covers authentication, checkout, order, and generic CRUD payloads
    for REST API testing alongside the UI layer.
    """

    # ── Auth Payloads ─────────────────────────────────────────────

    @staticmethod
    def login_payload(username: str = "standard_user", password: str = "secret_sauce") -> Dict[str, str]:
        return {"username": username, "password": password}

    @staticmethod
    def token_refresh_payload(refresh_token: str) -> Dict[str, str]:
        return {"refresh_token": refresh_token}

    # ── Checkout Payloads ─────────────────────────────────────────

    def checkout_payload(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        zip_code: Optional[str] = None,
        **overrides: Any,
    ) -> Dict[str, Any]:
        data = {
            "first_name": first_name or self.faker.first_name(),
            "last_name": last_name or self.faker.last_name(),
            "zip_code": zip_code or self.faker.zipcode(),
        }
        data.update(overrides)
        return data

    # ── Order Payloads ────────────────────────────────────────────

    def order_payload(
        self,
        items: Optional[List[Dict[str, Any]]] = None,
        shipping_address: Optional[Dict[str, str]] = None,
        **overrides: Any,
    ) -> Dict[str, Any]:
        data = {
            "items": items or [
                {"product_id": self.faker.uuid4(), "quantity": 1, "price": 29.99},
                {"product_id": self.faker.uuid4(), "quantity": 2, "price": 9.99},
            ],
            "shipping_address": shipping_address or {
                "first_name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "street": self.faker.street_address(),
                "city": self.faker.city(),
                "state": self.faker.state_abbr(),
                "zip": self.faker.zipcode(),
            },
            "payment_method": "credit_card",
        }
        data.update(overrides)
        return data

    # ── User Profile Payloads ─────────────────────────────────────

    def create_user_payload(self, **overrides: Any) -> Dict[str, Any]:
        data = {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "password": self.faker.password(length=12),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "role": "customer",
        }
        data.update(overrides)
        return data

    def update_user_payload(self, **overrides: Any) -> Dict[str, Any]:
        data = {
            "email": self.faker.email(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "phone": self.faker.phone_number(),
        }
        data.update(overrides)
        return data

    # ── Generic CRUD Payloads ─────────────────────────────────────

    def create_payload(self, resource: str = "item", **overrides: Any) -> Dict[str, Any]:
        data = {
            "name": self.faker.catch_phrase(),
            "description": self.faker.text(max_nb_chars=100),
            "status": "active",
        }
        data.update(overrides)
        return data

    def json(self, **overrides: Any) -> Dict[str, Any]:
        return self.create_user_payload(**overrides)
