import logging as stdlib_logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

from selenium.webdriver.remote.webdriver import WebDriver

from config.constants import Directory
from utils.allure_manager import AllureManager

logger = stdlib_logging.getLogger(__name__)


class ScreenshotManager:
    """Manages screenshot capture with timestamping, failure context,
    cleanup, and automatic Allure attachment.

    Thread-safe design — each test creates its own manager or uses
    the shared instance from conftest.
    """

    def __init__(self, screenshot_dir: Union[str, Path] = Directory.SCREENSHOTS):
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    # ── Capture ───────────────────────────────────────────────────

    def capture(
        self,
        driver: WebDriver,
        name: Optional[str] = None,
        timestamp: bool = True,
        attach_allure: bool = True,
    ) -> Path:
        """Take a screenshot and optionally attach it to the Allure report.

        Args:
            driver: Selenium WebDriver instance.
            name:  Base filename (without extension).
            timestamp:  Whether to prepend a ``YYYYMMDD_HHMMSS`` prefix.
            attach_allure:  Also attach to the current Allure test.

        Returns:
            Path to the saved PNG file.
        """
        filename = self._build_filename(name or "screenshot", timestamp)
        path = self.screenshot_dir / filename
        driver.save_screenshot(str(path))

        if attach_allure:
            AllureManager.attach_screenshot(driver, name=name or "Screenshot")

        logger.debug("Screenshot saved: %s", path)
        return path

    def capture_element(
        self,
        element: Any,
        name: Optional[str] = None,
        timestamp: bool = True,
        driver_for_allure: Optional[WebDriver] = None,
    ) -> bytes:
        """Capture a screenshot of a specific element and return PNG bytes.

        Args:
            element: Selenium WebElement.
            name:  Display name for the Allure attachment.
            timestamp:  Not used for bytes — present for API consistency.
            driver_for_allure:  If set, also attach a full-page screenshot
                alongside the element crop.

        Returns:
            PNG bytes of the element screenshot.
        """
        png = element.screenshot_as_png
        allure_name = name or "Element Screenshot"

        if driver_for_allure is not None:
            AllureManager.attach_screenshot(driver_for_allure, name=f"{allure_name} (full page)")

        return png

    # ── Failure Handling ──────────────────────────────────────────

    def capture_on_failure(
        self,
        driver: WebDriver,
        test_name: str,
        exception: Optional[Exception] = None,
    ) -> Path:
        """Capture a timestamped screenshot on test failure with Allure +
        page source attachments.

        Args:
            driver: Selenium WebDriver instance.
            test_name:  Name of the failing test (sanitised for filename).
            exception:  Optional exception for context.

        Returns:
            Path to the saved PNG file.
        """
        sanitised = self._sanitise_test_name(test_name)
        path = self.capture(
            driver,
            name=f"{sanitised}_FAILED",
            timestamp=True,
            attach_allure=True,
        )

        AllureManager.attach_page_source(driver, name=f"{sanitised}_page_source")

        if exception:
            AllureManager.attach_text(
                name=f"{sanitised}_exception",
                content=f"{type(exception).__name__}: {exception}",
            )

        logger.warning("Failure screenshot captured: %s | %s", sanitised, exception or "")
        return path

    # ── Cleanup ───────────────────────────────────────────────────

    def cleanup(self, max_age_days: int = 30) -> int:
        """Remove screenshots older than ``max_age_days``.

        Args:
            max_age_days:  Maximum age in days before deletion.

        Returns:
            Number of files removed.
        """
        now = datetime.now()
        removed = 0
        for f in self.screenshot_dir.glob("*.png"):
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if (now - mtime).days > max_age_days:
                f.unlink()
                removed += 1
        if removed:
            logger.info("Cleaned up %d old screenshot(s)", removed)
        return removed

    def cleanup_all(self) -> int:
        """Remove every screenshot in the directory.

        Returns:
            Number of files removed.
        """
        removed = 0
        for f in self.screenshot_dir.glob("*.png"):
            f.unlink()
            removed += 1
        if removed:
            logger.info("Removed %d screenshot(s)", removed)
        return removed

    # ── Helpers ───────────────────────────────────────────────────

    def _build_filename(self, name: str, use_timestamp: bool) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        parts = [name]
        if use_timestamp:
            parts.insert(0, ts)
        return "_".join(parts) + ".png"

    @staticmethod
    def _sanitise_test_name(name: str) -> str:
        return name.replace("/", "_").replace(" ", "_").replace("[", "_").replace("]", "_")

    @property
    def count(self) -> int:
        return len(list(self.screenshot_dir.glob("*.png")))

    @property
    def file_list(self) -> list:
        return sorted(self.screenshot_dir.glob("*.png"))
