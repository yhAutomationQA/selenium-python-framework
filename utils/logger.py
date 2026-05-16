import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


class Logger:
    _instances: dict = {}

    def __new__(cls, name: str = "framework"):
        if name not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[name] = instance
        return cls._instances[name]

    def __init__(self, name: str = "framework"):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        file_handler = RotatingFileHandler(
            log_dir / "framework.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger
