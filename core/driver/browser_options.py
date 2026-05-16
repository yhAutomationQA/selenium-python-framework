from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from typing import Optional, Union


class ChromeOptionsBuilder:
    def __init__(self):
        self._opts = webdriver.ChromeOptions()

    def headless(self, enabled: bool = True) -> "ChromeOptionsBuilder":
        if enabled:
            self._opts.add_argument("--headless=new")
        return self

    def incognito(self, enabled: bool = True) -> "ChromeOptionsBuilder":
        if enabled:
            self._opts.add_argument("--incognito")
        return self

    def sandbox(self, enabled: bool = True) -> "ChromeOptionsBuilder":
        if not enabled:
            self._opts.add_argument("--no-sandbox")
        return self

    def dev_shm(self, enabled: bool = True) -> "ChromeOptionsBuilder":
        if not enabled:
            self._opts.add_argument("--disable-dev-shm-usage")
        return self

    def gpu(self, enabled: bool = True) -> "ChromeOptionsBuilder":
        if not enabled:
            self._opts.add_argument("--disable-gpu")
        return self

    def window_size(self, width: int = 1920, height: int = 1080) -> "ChromeOptionsBuilder":
        self._opts.add_argument(f"--window-size={width},{height}")
        return self

    def disable_notifications(self) -> "ChromeOptionsBuilder":
        self._opts.add_argument("--disable-notifications")
        return self

    def disable_popups(self) -> "ChromeOptionsBuilder":
        self._opts.add_argument("--disable-popup-blocking")
        return self

    def disable_extensions(self) -> "ChromeOptionsBuilder":
        self._opts.add_argument("--disable-extensions")
        return self

    def disable_infobars(self) -> "ChromeOptionsBuilder":
        self._opts.add_argument("--disable-infobars")
        return self

    def download_dir(self, path: str) -> "ChromeOptionsBuilder":
        prefs = {
            "download.default_directory": path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
        }
        self._opts.add_experimental_option("prefs", prefs)
        return self

    def add_argument(self, arg: str) -> "ChromeOptionsBuilder":
        self._opts.add_argument(arg)
        return self

    def add_experimental_option(self, name: str, value) -> "ChromeOptionsBuilder":
        self._opts.add_experimental_option(name, value)
        return self

    def build(self) -> ChromeOptions:
        return self._opts


class FirefoxOptionsBuilder:
    def __init__(self):
        self._opts = webdriver.FirefoxOptions()

    def headless(self, enabled: bool = True) -> "FirefoxOptionsBuilder":
        if enabled:
            self._opts.add_argument("--headless")
        return self

    def incognito(self, enabled: bool = True) -> "FirefoxOptionsBuilder":
        if enabled:
            self._opts.set_preference("browser.privatebrowsing.autostart", True)
        return self

    def window_size(self, width: int = 1920, height: int = 1080) -> "FirefoxOptionsBuilder":
        self._opts.add_argument(f"--width={width}")
        self._opts.add_argument(f"--height={height}")
        return self

    def download_dir(self, path: str) -> "FirefoxOptionsBuilder":
        self._opts.set_preference("browser.download.folderList", 2)
        self._opts.set_preference("browser.download.dir", path)
        self._opts.set_preference("browser.download.useDownloadDir", True)
        self._opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "*/*")
        self._opts.set_preference("pdfjs.disabled", True)
        return self

    def add_argument(self, arg: str) -> "FirefoxOptionsBuilder":
        self._opts.add_argument(arg)
        return self

    def set_preference(self, key: str, value) -> "FirefoxOptionsBuilder":
        self._opts.set_preference(key, value)
        return self

    def build(self) -> FirefoxOptions:
        return self._opts


class EdgeOptionsBuilder:
    def __init__(self):
        self._opts = webdriver.EdgeOptions()

    def headless(self, enabled: bool = True) -> "EdgeOptionsBuilder":
        if enabled:
            self._opts.add_argument("--headless=new")
        return self

    def incognito(self, enabled: bool = True) -> "EdgeOptionsBuilder":
        if enabled:
            self._opts.add_argument("--inprivate")
        return self

    def sandbox(self, enabled: bool = True) -> "EdgeOptionsBuilder":
        if not enabled:
            self._opts.add_argument("--no-sandbox")
        return self

    def window_size(self, width: int = 1920, height: int = 1080) -> "EdgeOptionsBuilder":
        self._opts.add_argument(f"--window-size={width},{height}")
        return self

    def disable_notifications(self) -> "EdgeOptionsBuilder":
        self._opts.add_argument("--disable-notifications")
        return self

    def download_dir(self, path: str) -> "EdgeOptionsBuilder":
        prefs = {
            "download.default_directory": path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        }
        self._opts.add_experimental_option("prefs", prefs)
        return self

    def add_argument(self, arg: str) -> "EdgeOptionsBuilder":
        self._opts.add_argument(arg)
        return self

    def add_experimental_option(self, name: str, value) -> "EdgeOptionsBuilder":
        self._opts.add_experimental_option(name, value)
        return self

    def build(self) -> EdgeOptions:
        return self._opts


BrowserOptions = Union[ChromeOptions, FirefoxOptions, EdgeOptions]


class BrowserOptionsFactory:

    @staticmethod
    def create_options(
        browser: str,
        headless: bool = False,
        incognito: bool = False,
        download_dir: Optional[str] = None,
    ) -> BrowserOptions:
        browser = browser.lower()
        factories = {
            "chrome": BrowserOptionsFactory._chrome_options,
            "firefox": BrowserOptionsFactory._firefox_options,
            "edge": BrowserOptionsFactory._edge_options,
        }
        builder = factories.get(browser)
        if not builder:
            raise ValueError(f"Unsupported browser: {browser}")
        return builder(headless, incognito, download_dir)

    @staticmethod
    def _chrome_options(headless: bool, incognito: bool, download_dir: Optional[str]) -> ChromeOptions:
        builder = ChromeOptionsBuilder()
        builder.headless(headless)
        builder.incognito(incognito)
        builder.sandbox(False)
        builder.dev_shm(False)
        builder.gpu(False)
        builder.window_size()
        builder.disable_notifications()
        builder.disable_popups()
        builder.disable_extensions()
        builder.disable_infobars()
        if download_dir:
            builder.download_dir(download_dir)
        return builder.build()

    @staticmethod
    def _firefox_options(headless: bool, incognito: bool, download_dir: Optional[str]) -> FirefoxOptions:
        builder = FirefoxOptionsBuilder()
        builder.headless(headless)
        builder.incognito(incognito)
        builder.window_size()
        if download_dir:
            builder.download_dir(download_dir)
        return builder.build()

    @staticmethod
    def _edge_options(headless: bool, incognito: bool, download_dir: Optional[str]) -> EdgeOptions:
        builder = EdgeOptionsBuilder()
        builder.headless(headless)
        builder.incognito(incognito)
        builder.sandbox(False)
        builder.window_size()
        builder.disable_notifications()
        if download_dir:
            builder.download_dir(download_dir)
        return builder.build()
