import os
from pathlib import Path

from dotenv import load_dotenv

from config.settings import Settings

_CONFIG_CACHE: dict[str, Settings] = {}

_SUPPORTED_ENVS = frozenset({"dev", "qa", "staging", "prod"})


def resolve_env(env: str | None = None) -> str:
    env = env or os.getenv("ENV") or "qa"
    env = env.lower().strip()
    if env not in _SUPPORTED_ENVS:
        raise ValueError(f"Unsupported environment: '{env}'. Must be one of {sorted(_SUPPORTED_ENVS)}")
    return env


def load_settings(env: str | None = None) -> Settings:
    env = resolve_env(env)

    if env in _CONFIG_CACHE:
        return _CONFIG_CACHE[env]

    env_file = Path(f".env.{env}")

    if not env_file.exists():
        raise FileNotFoundError(
            f"Environment file not found: {env_file.resolve()}\n"
            f"Create it from .env.example:  cp .env.example .env.{env}"
        )

    load_dotenv(dotenv_path=env_file, override=True)

    settings = Settings()
    _CONFIG_CACHE[env] = settings
    return settings


def reload_settings(env: str | None = None) -> Settings:
    env = resolve_env(env)
    _CONFIG_CACHE.pop(env, None)
    return load_settings(env)
