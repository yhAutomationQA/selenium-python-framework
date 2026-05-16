from .base_api import BaseAPI
from config.environments import ENV_CONFIG


class APIClient(BaseAPI):
    _instances: dict = {}

    def __new__(cls, env: str = "qa"):
        if env not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[env] = instance
        return cls._instances[env]

    def __init__(self, env: str = "qa"):
        if not getattr(self, "_initialized", False):
            config = ENV_CONFIG.get(env, ENV_CONFIG["qa"])
            super().__init__(base_url=config["api_url"])
            self._initialized = True
