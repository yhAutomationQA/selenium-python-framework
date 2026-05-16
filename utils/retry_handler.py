"""Retry handler utilities using tenacity for framework resilience.

Provides configurable retry strategies for:
- Stale element recovery (Selenium StaleElementReferenceException)
- Flaky test recovery (AssertionError)
- API connection retry (ConnectionError, Timeout)
- Smart wait with exponential backoff + jitter

Usage:
    from utils.retry_handler import (
        stale_element_retry, flaky_test_retry, api_retry, smart_retry,
        retry_call, RetryHandler,
    )

    # Decorator approach
    @stale_element_retry
    def click_element(driver, locator):
        driver.find_element(*locator).click()

    # Direct call approach
    result = retry_call(flaky_func, mode="flaky_test")

    # Class-based handler
    handler = RetryHandler(mode="smart_wait")
    result = handler.run(my_func, arg1, arg2)
"""

from __future__ import annotations

from contextlib import contextmanager
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
    wait_random_exponential,
)
from tenacity.stop import stop_base
from tenacity.wait import wait_base

try:
    from selenium.common.exceptions import StaleElementReferenceException
except ImportError:
    StaleElementReferenceException = type("StaleElementReferenceException", (Exception,), {})

from utils.logger import LoggerConfig

log = LoggerConfig.get_logger("retry")

F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")


class RetryMode(str, Enum):
    """Predefined retry strategies for common failure patterns."""

    STALE_ELEMENT = "stale_element"
    FLAKY_TEST = "flaky_test"
    API_RETRY = "api_retry"
    SMART_WAIT = "smart_wait"
    FAST = "fast"


class RetryConfig:
    """Configuration for a retry strategy.

    Args:
        attempts: Maximum number of retry attempts.
        min_wait: Minimum wait between retries in seconds.
        max_wait: Maximum wait between retries in seconds.
        wait_strategy: Type of wait - 'exponential', 'fixed', or 'random_exponential'.
        exceptions: Exception types to retry on. If None, retries on all exceptions.
        jitter: Whether to add jitter to exponential wait times.
        reraise: Whether to reraise the last exception after exhaustion.
    """

    def __init__(
        self,
        attempts: int = 3,
        min_wait: float = 0.5,
        max_wait: float = 10.0,
        wait_strategy: str = "exponential",
        exceptions: Optional[Tuple[Type[Exception], ...]] = None,
        jitter: bool = True,
        reraise: bool = True,
    ):
        self.attempts = attempts
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.wait_strategy = wait_strategy
        self.exceptions = exceptions
        self.jitter = jitter
        self.reraise = reraise

    def copy_with(self, **overrides: Any) -> "RetryConfig":
        """Return a new RetryConfig with overridden fields."""
        params = {
            "attempts": self.attempts,
            "min_wait": self.min_wait,
            "max_wait": self.max_wait,
            "wait_strategy": self.wait_strategy,
            "exceptions": self.exceptions,
            "jitter": self.jitter,
            "reraise": self.reraise,
        }
        params.update(overrides)
        return RetryConfig(**params)

    def __repr__(self) -> str:
        return (
            f"RetryConfig(attempts={self.attempts}, "
            f"min_wait={self.min_wait}, max_wait={self.max_wait}, "
            f"wait_strategy='{self.wait_strategy}', "
            f"exceptions={self.exceptions})"
        )


# ── Preset Configurations ─────────────────────────────────────────


STALE_ELEMENT_CONFIG = RetryConfig(
    attempts=3,
    min_wait=0.3,
    max_wait=2.0,
    wait_strategy="fixed",
    exceptions=(StaleElementReferenceException,),
    reraise=True,
)

FLAKY_TEST_CONFIG = RetryConfig(
    attempts=3,
    min_wait=1.0,
    max_wait=5.0,
    wait_strategy="exponential",
    exceptions=(AssertionError,),
    reraise=True,
)

API_RETRY_CONFIG = RetryConfig(
    attempts=3,
    min_wait=1.0,
    max_wait=30.0,
    wait_strategy="random_exponential",
    exceptions=(
        ConnectionError,
        TimeoutError,
    ),
    reraise=True,
)

SMART_WAIT_CONFIG = RetryConfig(
    attempts=5,
    min_wait=0.5,
    max_wait=10.0,
    wait_strategy="exponential",
    exceptions=None,
    reraise=True,
)

FAST_CONFIG = RetryConfig(
    attempts=2,
    min_wait=0.1,
    max_wait=0.5,
    wait_strategy="fixed",
    exceptions=None,
    reraise=True,
)


_PRESETS: Dict[RetryMode, RetryConfig] = {
    RetryMode.STALE_ELEMENT: STALE_ELEMENT_CONFIG,
    RetryMode.FLAKY_TEST: FLAKY_TEST_CONFIG,
    RetryMode.API_RETRY: API_RETRY_CONFIG,
    RetryMode.SMART_WAIT: SMART_WAIT_CONFIG,
    RetryMode.FAST: FAST_CONFIG,
}


# ── Wait / Stop Builder ─────────────────────────────────────────


def build_wait(config: RetryConfig) -> wait_base:
    """Build a tenacity wait strategy from a RetryConfig."""
    if config.wait_strategy == "fixed":
        return wait_fixed(config.min_wait)
    if config.wait_strategy == "random_exponential":
        return wait_random_exponential(
            multiplier=config.min_wait,
            max=config.max_wait,
        )
    return wait_exponential(
        multiplier=config.min_wait,
        min=config.min_wait,
        max=config.max_wait,
    )


def build_stop(config: RetryConfig) -> stop_base:
    """Build a tenacity stop strategy from a RetryConfig."""
    return stop_after_attempt(config.attempts)


def build_retry_condition(
    config: RetryConfig,
) -> Callable[[BaseException], bool]:
    """Build a tenacity retry condition from a RetryConfig."""
    if config.exceptions:
        return retry_if_exception_type(config.exceptions)
    return retry_if_exception_type(Exception)


# ── Logging Callback ────────────────────────────────────────────


def _before_retry_log(retry_state: Any) -> None:
    """Log retry attempts via Loguru."""
    attempt = retry_state.attempt_number
    fn_name = retry_state.fn.__name__ if retry_state.fn else "unknown"
    exception = retry_state.outcome.exception() if retry_state.outcome else None
    wait_next = retry_state.next_action.sleep if retry_state.next_action else 0

    log.warning(
        "Retry attempt {attempt}/{max} for '{fn}' failed: {exc}. Retrying in {wait:.2f}s...",
        attempt=attempt,
        max=getattr(retry_state.idle_for, "max", "?"),
        fn=fn_name,
        exc=exception,
        wait=wait_next,
    )


# ── Decorator Factory ───────────────────────────────────────────


def retry_decorator(
    config: Optional[RetryConfig] = None,
    mode: Optional[RetryMode] = None,
    **override_kwargs: Any,
) -> Callable[[F], F]:
    """Create a tenacity retry decorator from a preset mode or custom config.

    Args:
        config: A RetryConfig instance for custom retry settings.
        mode: A RetryMode preset to use.
        **override_kwargs: Override any RetryConfig field by name
            (attempts, min_wait, max_wait, wait_strategy, exceptions, jitter, reraise).

    Returns:
        A tenacity retry decorator.

    Raises:
        ValueError: If neither config nor mode is provided.

    Example:
        @retry_decorator(mode=RetryMode.STALE_ELEMENT)
        def fragile_element_op():
            ...

        @retry_decorator(config=RetryConfig(attempts=5, wait_strategy="fixed", min_wait=0.2))
        def custom_op():
            ...
    """
    if config is None and mode is None:
        raise ValueError("Either 'config' or 'mode' must be provided")

    resolved: RetryConfig
    if config is not None:
        resolved = config
    else:
        resolved = _PRESETS[mode]

    if override_kwargs:
        resolved = resolved.copy_with(**override_kwargs)

    wait = build_wait(resolved)
    stop = build_stop(resolved)
    retry_on = build_retry_condition(resolved)

    return retry(
        stop=stop,
        wait=wait,
        retry=retry_on,
        reraise=resolved.reraise,
        before_sleep=_before_retry_log,
    )


# ── Pre-built Decorators ────────────────────────────────────────


stale_element_retry = retry_decorator(mode=RetryMode.STALE_ELEMENT)
"""Retry decorator for StaleElementReferenceException recovery."""

flaky_test_retry = retry_decorator(mode=RetryMode.FLAKY_TEST)
"""Retry decorator for flaky test recovery (AssertionError)."""

api_retry = retry_decorator(mode=RetryMode.API_RETRY)
"""Retry decorator for API connection retry (ConnectionError, TimeoutError)."""

smart_retry = retry_decorator(mode=RetryMode.SMART_WAIT)
"""Retry decorator with exponential backoff and jitter for general use."""


# ── Direct Call Retry ───────────────────────────────────────────


def retry_call(
    fn: Callable[..., T],
    *args: Any,
    config: Optional[RetryConfig] = None,
    mode: Optional[RetryMode] = None,
    **kwargs: Any,
) -> T:
    """Execute a callable with retry logic.

    Args:
        fn: The callable to execute.
        *args: Positional arguments passed to fn.
        config: A RetryConfig instance for custom retry settings.
        mode: A RetryMode preset to use.
        **kwargs: Keyword arguments passed to fn.

    Returns:
        The return value of fn.

    Raises:
        ValueError: If neither config nor mode is provided.
        Exception: The last exception raised by fn after retry exhaustion.

    Example:
        result = retry_call(api.get, "/users", mode="api_retry")
        result = retry_call(
            driver.find_element, locator,
            config=RetryConfig(attempts=5, exceptions=(StaleElementReferenceException,)),
        )
    """
    if config is None and mode is None:
        raise ValueError("Either 'config' or 'mode' must be provided")

    resolved: RetryConfig
    if config is not None:
        resolved = config
    else:
        resolved = _PRESETS[mode]

    wait = build_wait(resolved)
    stop = build_stop(resolved)
    retry_on = build_retry_condition(resolved)

    decorated = retry(
        stop=stop,
        wait=wait,
        retry=retry_on,
        reraise=resolved.reraise,
        before_sleep=_before_retry_log,
    )(fn)

    return decorated(*args, **kwargs)


# ── Class-based Handler ─────────────────────────────────────────


class RetryHandler:
    """Class-based handler for configurable retry logic.

    Provides a reusable instance with:
    - Decorator-style usage via ``.run()``
    - Context manager for scoped retry config
    - Property-based access to config

    Args:
        config: A RetryConfig instance. Mutually exclusive with mode.
        mode: A RetryMode preset. Mutually exclusive with config.

    Raises:
        ValueError: If both or neither of config/mode are provided.

    Example:
        handler = RetryHandler(mode="smart_wait")
        result = handler.run(my_function, arg1, arg2)

        with RetryHandler(mode="stale_element") as r:
            result = r.run(click_element, locator)
    """

    def __init__(
        self,
        config: Optional[RetryConfig] = None,
        mode: Optional[Union[RetryMode, str]] = None,
    ):
        if config is not None and mode is not None:
            raise ValueError("Provide either 'config' or 'mode', not both")
        if config is None and mode is None:
            raise ValueError("Either 'config' or 'mode' must be provided")

        if isinstance(mode, str):
            mode = RetryMode(mode)

        self._config: RetryConfig
        if config is not None:
            self._config = config
        else:
            self._config = _PRESETS[mode]

        self._mode: Optional[RetryMode] = mode
        self._decorator: Optional[Callable[[F], F]] = None

    @property
    def config(self) -> RetryConfig:
        """The current RetryConfig for this handler."""
        return self._config

    @config.setter
    def config(self, value: RetryConfig) -> None:
        self._config = value
        self._decorator = None

    @property
    def mode(self) -> Optional[RetryMode]:
        """The RetryMode preset (None if using custom config)."""
        return self._mode

    def _get_decorator(self) -> Callable[[F], F]:
        if self._decorator is None:
            self._decorator = retry_decorator(config=self._config)
        return self._decorator

    def run(self, fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute a callable with this handler's retry configuration.

        Args:
            fn: The callable to execute.
            *args: Positional arguments passed to fn.
            **kwargs: Keyword arguments passed to fn.

        Returns:
            The return value of fn.

        Raises:
            Exception: The last exception raised by fn after retry exhaustion.
        """
        decorator = self._get_decorator()
        return decorator(fn)(*args, **kwargs)

    @contextmanager
    def temporary_config(
        self,
        config: Optional[RetryConfig] = None,
        mode: Optional[Union[RetryMode, str]] = None,
    ) -> Generator["RetryHandler", None, None]:
        """Temporarily override the retry configuration for a scoped block.

        Args:
            config: Temporary RetryConfig. Mutually exclusive with mode.
            mode: Temporary RetryMode. Mutually exclusive with config.

        Yields:
            The RetryHandler instance with the temporary config applied.

        Example:
            handler = RetryHandler(mode="smart_wait")
            with handler.temporary_config(mode="fast") as h:
                h.run(quick_op)
        """
        original_config = self._config
        original_mode = self._mode

        try:
            if config is not None:
                self._config = config
                self._mode = None
            elif mode is not None:
                if isinstance(mode, str):
                    mode = RetryMode(mode)
                self._config = _PRESETS[mode]
                self._mode = mode
            self._decorator = None
            yield self
        finally:
            self._config = original_config
            self._mode = original_mode
            self._decorator = None

    def __repr__(self) -> str:
        mode_str = f"mode={self._mode.value}" if self._mode else "custom"
        return f"RetryHandler({mode_str}, {self._config})"
