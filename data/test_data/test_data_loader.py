import json
from pathlib import Path
from typing import Any, Dict, Optional

from config.config_loader import resolve_env

_ENV_DATA_DIR = Path(__file__).resolve().parent
_CACHE: Dict[str, Dict[str, Any]] = {}
_ENV_OVERRIDE_CACHE: Dict[str, Dict[str, Any]] = {}


class TestDataLoader:
    """Environment-aware test data loader.

    Loads a base dataset for the active environment (dev/qa/staging/prod)
    and falls back to common data where env-specific files don't exist.
    """

    @classmethod
    def _env_dir(cls, env: Optional[str] = None) -> Path:
        env = resolve_env(env)
        return _ENV_DATA_DIR / env

    @classmethod
    def _file_path(cls, filename: str, env: Optional[str] = None) -> Path:
        return cls._env_dir(env) / filename

    @classmethod
    def _load_file(cls, filepath: Path) -> Dict[str, Any]:
        if not filepath.exists():
            return {}
        return dict(json.loads(filepath.read_text(encoding="utf-8")))

    @classmethod
    def _load_env_data(cls, env: Optional[str] = None) -> Dict[str, Any]:
        env = resolve_env(env)
        if env not in _CACHE:
            env_dir = cls._env_dir(env)
            if not env_dir.exists():
                _CACHE[env] = {}
            else:
                merged: Dict[str, Any] = {}
                for json_file in sorted(env_dir.glob("*.json")):
                    data = cls._load_file(json_file)
                    merged.update(data)
                _CACHE[env] = merged
        return _CACHE[env]

    @classmethod
    def get(cls, key: str, default: Any = None, env: Optional[str] = None) -> Any:
        data = cls._load_env_data(env)
        return data.get(key, default)

    @classmethod
    def get_nested(cls, *keys: str, env: Optional[str] = None) -> Any:
        data = cls._load_env_data(env)
        for key in keys:
            if not isinstance(data, dict):
                return None
            data = data.get(key)
            if data is None:
                return None
        return data

    @classmethod
    def login_users(cls, env: Optional[str] = None) -> Dict[str, Any]:
        return cls.get("login_users", {}, env)

    @classmethod
    def checkout_data(cls, env: Optional[str] = None) -> Dict[str, Any]:
        return cls.get("checkout_data", {}, env)

    @classmethod
    def api_endpoints(cls, env: Optional[str] = None) -> Dict[str, str]:
        return cls.get("api_endpoints", {}, env)

    @classmethod
    def features(cls, env: Optional[str] = None) -> Dict[str, bool]:
        return cls.get("features", {}, env)

    @classmethod
    def env_name(cls, env: Optional[str] = None) -> str:
        return resolve_env(env)

    @classmethod
    def reload(cls, env: Optional[str] = None) -> None:
        env_key = resolve_env(env)
        _CACHE.pop(env_key, None)

    @classmethod
    def clear_cache(cls) -> None:
        _CACHE.clear()

    @classmethod
    def data_dir(cls, env: Optional[str] = None) -> str:
        return str(cls._env_dir(env).resolve())

    @classmethod
    def has_key(cls, key: str, env: Optional[str] = None) -> bool:
        return key in cls._load_env_data(env)
