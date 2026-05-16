from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from components.footer_component import FooterComponent
from components.modal_component import ModalComponent
from components.navbar_component import NavbarComponent
from components.sidebar_component import SidebarComponent
from pages.base_page import BasePage


class DashboardPage(BasePage):
    WELCOME_HEADER = (By.CSS_SELECTOR, ".welcome-header, h1")
    METRIC_CARDS = (By.CSS_SELECTOR, ".metric-card, .stat-card, .dashboard-card")
    RECENT_ACTIVITY = (By.CSS_SELECTOR, ".recent-activity, .activity-log")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, timeout)
        self._navbar = NavbarComponent(driver, timeout)
        self._sidebar = SidebarComponent(driver, timeout)
        self._footer = FooterComponent(driver, timeout)
        self._modal = ModalComponent(driver, timeout)

    @property
    def navbar(self) -> NavbarComponent:
        return self._navbar

    @property
    def sidebar(self) -> SidebarComponent:
        return self._sidebar

    @property
    def footer(self) -> FooterComponent:
        return self._footer

    @property
    def modal(self) -> ModalComponent:
        return self._modal

    def open(self) -> "DashboardPage":
        self.open_url("/dashboard")
        self.wait_for_loaded()
        return self

    def wait_for_loaded(self) -> "DashboardPage":
        self.wait_until_visible(self.WELCOME_HEADER)
        return self

    def get_welcome_text(self) -> str:
        return self.get_text(self.WELCOME_HEADER)

    def get_metric_count(self) -> int:
        return len(self.find_elements(self.METRIC_CARDS))

    def has_activity_log(self) -> bool:
        return self.is_displayed(self.RECENT_ACTIVITY)
