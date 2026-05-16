import random
import string
from datetime import datetime, timedelta
from typing import Any


class DataGenerator:
    @staticmethod
    def random_string(length: int = 10) -> str:
        return "".join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def random_email(domain: str = "test.com") -> str:
        return f"{DataGenerator.random_string(8).lower()}@{domain}"

    @staticmethod
    def random_int(min_val: int = 0, max_val: int = 1000) -> int:
        return random.randint(min_val, max_val)

    @staticmethod
    def random_float(min_val: float = 0.0, max_val: float = 1000.0, decimals: int = 2) -> float:
        return round(random.uniform(min_val, max_val), decimals)

    @staticmethod
    def random_phone() -> str:
        return f"+1{random.randint(2000000000, 9999999999)}"

    @staticmethod
    def random_boolean() -> bool:
        return random.choice([True, False])

    @staticmethod
    def random_choice(items: list) -> Any:
        return random.choice(items)

    @staticmethod
    def current_timestamp(fmt: str = "%Y-%m-%d_%H-%M-%S") -> str:
        return datetime.now().strftime(fmt)

    @staticmethod
    def future_date(days_ahead: int = 30) -> str:
        return (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    @staticmethod
    def past_date(days_ago: int = 30) -> str:
        return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
