import logging
import threading
from typing import Dict, Optional

from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class DriverManager:
    def __init__(self):
        self._drivers: Dict[int, WebDriver] = {}
        self._lock = threading.Lock()

    def register(self, driver: WebDriver) -> None:
        tid = threading.get_ident()
        with self._lock:
            self._drivers[tid] = driver
        logger.info("Driver registered | thread=%d | session=%s", tid, driver.session_id)

    def get(self) -> Optional[WebDriver]:
        tid = threading.get_ident()
        return self._drivers.get(tid)

    def _find_tid(self, driver: WebDriver) -> Optional[int]:
        for tid, d in list(self._drivers.items()):
            if d is driver:
                return tid
        return None

    def _remove(self, tid: int) -> Optional[WebDriver]:
        with self._lock:
            return self._drivers.pop(tid, None)

    def quit(self, driver: WebDriver) -> None:
        tid = self._find_tid(driver) or threading.get_ident()
        if tid not in self._drivers:
            logger.warning("Driver not tracked, quitting directly | session=%s", driver.session_id)
            try:
                driver.quit()
            except Exception as e:
                logger.error("Driver quit failed | error=%s", e)
            return
        self._remove(tid)
        try:
            driver.quit()
            logger.info("Driver quit | tid=%d | session=%s", tid, driver.session_id)
        except Exception as e:
            logger.error("Driver quit failed | tid=%d | error=%s", tid, e)

    def quit_registered(self) -> None:
        tid = threading.get_ident()
        driver = self._remove(tid)
        if driver:
            try:
                driver.quit()
                logger.info("Registered driver quit | tid=%d", tid)
            except Exception as e:
                logger.error("Registered driver quit failed | tid=%d | error=%s", tid, e)

    def quit_all(self) -> None:
        with self._lock:
            drivers = list(self._drivers.items())
            self._drivers.clear()
        for tid, driver in drivers:
            try:
                driver.quit()
                logger.info("Driver force-quit | tid=%d | session=%s", tid, driver.session_id)
            except Exception as e:
                logger.warning("Driver force-quit failed | tid=%d | error=%s", tid, e)
        logger.info("All drivers quit: %d total", len(drivers))

    @property
    def active_count(self) -> int:
        with self._lock:
            return len(self._drivers)
