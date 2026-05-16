import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from faker import Faker


class BaseFactory:
    """Base class for all data factories.

    Provides a shared Faker instance, deterministic seed support,
    serialization helpers, and bulk generation.
    """

    _default_locale: str = "en_US"
    _default_seed: Optional[int] = None

    def __init__(self, seed: Optional[int] = None, locale: str = "en_US"):
        self._locale = locale
        self._seed = seed
        self.faker = Faker(locale)
        if seed is not None:
            Faker.seed(seed)

    # ── Subclass API ──────────────────────────────────────────────

    def json(self, **overrides: Any) -> Dict[str, Any]:
        raise NotImplementedError

    # ── Bulk Generation ───────────────────────────────────────────

    def list(self, count: int = 3, **shared_overrides: Any) -> List[Dict[str, Any]]:
        return [self.json(**shared_overrides) for _ in range(count)]

    def list_varying(self, *overrides_list: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [self.json(**o) for o in overrides_list]

    # ── Serialization ─────────────────────────────────────────────

    def to_json_file(self, path: Union[str, Path], **overrides: Any) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self.json(**overrides)
        path.write_text(json.dumps(data, indent=2, default=str))
        return path

    def to_json_file_bulk(
        self, path: Union[str, Path], count: int = 3, **shared_overrides: Any
    ) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self.list(count, **shared_overrides)
        path.write_text(json.dumps(data, indent=2, default=str))
        return path

    # ── Helpers ───────────────────────────────────────────────────

    def clone(self, seed: Optional[int] = None, locale: Optional[str] = None) -> "BaseFactory":
        return self.__class__(
            seed=seed if seed is not None else self._seed,
            locale=locale if locale is not None else self._locale,
        )

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def seed_value(self) -> Optional[int]:
        return self._seed
