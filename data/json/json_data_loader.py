import json
from pathlib import Path
from typing import Any, Dict, List

_DATA_DIR = Path(__file__).resolve().parent


class JsonDataLoader:
    """Loads static JSON datasets from the data/json/ directory.

    Provides caching, key-based queries, and path helpers so tests
    never deal with raw file I/O.
    """

    _cache: Dict[str, Any] = {}

    @classmethod
    def _load(cls, filename: str) -> Dict[str, Any]:
        if filename not in cls._cache:
            path = _DATA_DIR / filename
            if not path.exists():
                raise FileNotFoundError(f"JSON dataset not found: {path}")
            cls._cache[filename] = json.loads(path.read_text(encoding="utf-8"))
        return cls._cache[filename]

    @classmethod
    def clear_cache(cls) -> None:
        cls._cache.clear()

    # ── Specific Datasets ─────────────────────────────────────────

    @classmethod
    def saucedemo_users(cls) -> Dict[str, Any]:
        return cls._load("saucedemo_users.json")

    @classmethod
    def saucedemo_products(cls) -> Dict[str, Any]:
        return cls._load("saucedemo_products.json")

    @classmethod
    def checkout_profiles(cls) -> Dict[str, Any]:
        return cls._load("checkout_profiles.json")

    @classmethod
    def error_messages(cls) -> Dict[str, Any]:
        return cls._load("error_messages.json")

    @classmethod
    def api_payloads(cls) -> Dict[str, Any]:
        return cls._load("api_payloads.json")

    # ── Convenience Queries ───────────────────────────────────────

    @classmethod
    def get_user(cls, key: str) -> Dict[str, str]:
        return dict(cls.saucedemo_users()["users"][key])

    @classmethod
    def get_product(cls, key: str) -> Dict[str, Any]:
        return dict(cls.saucedemo_products()["products"][key])

    @classmethod
    def get_error(cls, key: str) -> str:
        return str(cls.error_messages()["errors"][key])

    @classmethod
    def get_api_payload(cls, key: str) -> Dict[str, Any]:
        return dict(cls.api_payloads()["payloads"][key])

    @classmethod
    def product_names(cls) -> List[str]:
        return list(cls.saucedemo_products()["products"].keys())

    @classmethod
    def product_price_list(cls) -> List[float]:
        return [p["price"] for p in cls.saucedemo_products()["products"].values()]

    @classmethod
    def paths(cls) -> Dict[str, str]:
        return {"json_dir": str(_DATA_DIR.resolve())}

    @classmethod
    def reload(cls) -> None:
        cls.clear_cache()
