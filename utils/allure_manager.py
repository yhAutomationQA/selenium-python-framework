import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.remote.webdriver import WebDriver


class AllureManager:
    """Centralised Allure attachment and environment helpers.

    All methods are static — no state, safe for parallel xdist usage.
    """

    # ── Screenshots ───────────────────────────────────────────────

    @staticmethod
    def attach_screenshot(
        driver: WebDriver,
        name: str = "Screenshot",
        quality: Optional[int] = None,
    ) -> None:
        """Capture and attach a PNG screenshot to the current Allure test."""
        png = driver.get_screenshot_as_png()
        allure.attach(png, name=name, attachment_type=AttachmentType.PNG)

    @staticmethod
    def attach_element_screenshot(
        driver: WebDriver,
        element,
        name: str = "Element Screenshot",
    ) -> None:
        """Capture and attach a screenshot of a specific element."""
        png = element.screenshot_as_png
        allure.attach(png, name=name, attachment_type=AttachmentType.PNG)

    # ── Page Source ───────────────────────────────────────────────

    @staticmethod
    def attach_page_source(
        driver: WebDriver,
        name: str = "Page Source",
    ) -> None:
        """Attach the current DOM as XML (useful for failure analysis)."""
        source = driver.page_source
        allure.attach(source, name=name, attachment_type=AttachmentType.XML)

    # ── Text ──────────────────────────────────────────────────────

    @staticmethod
    def attach_text(name: str, content: str) -> None:
        """Attach an arbitrary text blob."""
        allure.attach(content, name=name, attachment_type=AttachmentType.TEXT)

    @staticmethod
    def attach_log(
        log_path: Union[str, Path],
        name: str = "Test Log",
        max_lines: int = 500,
    ) -> None:
        """Attach the tail of a log file."""
        path = Path(log_path)
        if not path.exists():
            allure.attach(
                f"[File not found: {path}]",
                name=name,
                attachment_type=AttachmentType.TEXT,
            )
            return
        lines = path.read_text(encoding="utf-8").splitlines()
        tail = lines[-max_lines:]
        content = "\n".join(tail)
        allure.attach(content, name=name, attachment_type=AttachmentType.TEXT)

    # ── JSON ──────────────────────────────────────────────────────

    @staticmethod
    def attach_json(name: str, data: Any, indent: int = 2) -> None:
        """Attach a Python object serialised as pretty-printed JSON."""
        serialised = json.dumps(data, indent=indent, default=str, ensure_ascii=False)
        allure.attach(serialised, name=name, attachment_type=AttachmentType.JSON)

    @staticmethod
    def attach_network_log(
        name: str,
        entries: List[Dict[str, Any]],
    ) -> None:
        """Attach HAR-style network entries as JSON."""
        AllureManager.attach_json(name, entries)

    # ── HTML ──────────────────────────────────────────────────────

    @staticmethod
    def attach_html(name: str, content: str) -> None:
        """Attach an HTML fragment rendered inline in the Allure report."""
        allure.attach(content, name=name, attachment_type=AttachmentType.HTML)

    # ── Environment / Meta ────────────────────────────────────────

    @staticmethod
    def set_environment_properties(
        properties: Dict[str, str],
        results_dir: Union[str, Path] = "allure-results",
    ) -> None:
        """Write ``environment.properties`` for the Allure dashboard.

        This is a session-level operation best called from
        ``pytest_sessionfinish``.
        """
        path = Path(results_dir)
        path.mkdir(parents=True, exist_ok=True)
        env_path = path / "environment.properties"
        lines = [f"{k}={v}\n" for k, v in sorted(properties.items())]
        env_path.write_text("".join(lines), encoding="utf-8")

    @staticmethod
    def set_environment_from_settings(settings, results_dir: str = "allure-results") -> None:
        """Convenience: dump common Settings fields to environment.properties."""
        AllureManager.set_environment_properties(
            {
                "Environment": settings.env,
                "Browser": settings.browser,
                "Headless": str(settings.headless),
                "Incognito": str(settings.incognito),
                "Base_URL": settings.base_url,
                "API_URL": settings.api_url,
                "Log_Level": settings.log_level,
                "Python_Version": __import__("sys").version,
            },
            results_dir,
        )

    # ── Step Decorator ────────────────────────────────────────────

    @staticmethod
    def step(name: str):
        """Convenience alias for ``allure.step``."""
        return allure.step(name)

    @staticmethod
    def epic(name: str):
        """Alias for ``allure.epic``."""
        return allure.epic(name)

    @staticmethod
    def feature(name: str):
        """Alias for ``allure.feature``."""
        return allure.feature(name)

    @staticmethod
    def story(name: str):
        """Alias for ``allure.story``."""
        return allure.story(name)

    @staticmethod
    def severity(level: str):
        """Alias for ``allure.severity``."""
        return allure.severity(level)

    @staticmethod
    def tag(tag: str):
        """Alias for ``allure.tag``."""
        return allure.tag(tag)

    @staticmethod
    def link(url: str, name: Optional[str] = None):
        """Alias for ``allure.link``."""
        return allure.link(url, name)

    @staticmethod
    def issue(url: str, name: Optional[str] = None):
        """Alias for ``allure.issue``."""
        return allure.issue(url, name)

    @staticmethod
    def testcase(url: str, name: Optional[str] = None):
        """Alias for ``allure.testcase``."""
        return allure.testcase(url, name)
