from .base_api import BaseAPI
from config.config_loader import load_settings


class APIClient(BaseAPI):
    _instances: dict = {}

    def __new__(cls, env: str | None = None):
        env = env or "qa"
        if env not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[env] = instance
        return cls._instances[env]

    def __init__(self, env: str | None = None):
        if not getattr(self, "_initialized", False):
            settings = load_settings(env)
            super().__init__(base_url=settings.api_url)
            self._initialized = True
