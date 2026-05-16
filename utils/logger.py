import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from config.constants import Directory, LogLevel as LogLevelEnum


class LoggerConfig:
    """Configures Loguru sinks with rotation, retention, and structured output.

    Singleton guard prevents double-initialisation in pytest sessions.
    """

    _configured: bool = False

    @classmethod
    def configure(
        cls,
        log_level: str = "INFO",
        log_dir: str = Directory.LOGS,
        rotation: str = "10 MB",
        retention: str = "30 days",
        compression: str = "gz",
        serialize: bool = False,
        context: Optional[dict] = None,
    ) -> None:
        if cls._configured:
            return

        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        logger.remove()

        cls._configured = True

        # Ensure level is uppercase
        level = log_level.upper()

        # ── Console sink (colourised, human-readable) ─────────────
        logger.add(
            sys.stdout,
            level=level,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level:<8}</level> | "
                "<cyan>{extra[module]:<15}</cyan> | "
                "<level>{message}</level>"
            ),
            colorize=True,
            enqueue=True,
        )

        # ── Daily-rotating file sink (all levels) ─────────────────
        logger.add(
            log_path / "framework_{time:YYYY-MM-DD}.log",
            level="DEBUG",
            format=(
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | "
                "{extra[module]:<15} | {name}:{function}:{line} | {message}"
            ),
            rotation=rotation,
            retention=retention,
            compression=compression,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        # ── Error-only file sink ──────────────────────────────────
        logger.add(
            log_path / "errors_{time:YYYY-MM-DD}.log",
            level="ERROR",
            format=(
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | "
                "{extra[module]:<15} | {name}:{function}:{line} | {message}"
                "\n{exception}"
            ),
            rotation=rotation,
            retention=retention,
            compression=compression,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        # ── Structured JSON sink (machine-readable) ───────────────
        if serialize:
            logger.add(
                log_path / "structured_{time:YYYY-MM-DD}.json",
                level="DEBUG",
                serialize=True,
                rotation=rotation,
                retention=retention,
                compression=compression,
                enqueue=True,
            )

        bound = {"module": "init"}
        if context:
            bound.update(context)
        logger.configure(extra=bound)

    @classmethod
    def reset(cls) -> None:
        cls._configured = False
        logger.remove()

    @staticmethod
    def get_logger(module: str = "app") -> "logger":  # type: ignore[name-defined]
        """Return a Loguru logger bound to the given module name."""
        return logger.bind(module=module)


# Pre-bound convenience loggers
log = LoggerConfig.get_logger("app")
