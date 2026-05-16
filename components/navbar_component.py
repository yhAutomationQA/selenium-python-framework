import logging
from typing import List, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from components.base_component import BaseComponent

logger = logging.getLogger(__name__)


class NavbarComponent(BaseComponent):
    ROOT = (By.CSS_SELECTOR, "nav.navbar, header.navbar, [role='navigation']")

    BRAND = (By.CSS_SELECTOR, ".navbar-brand, .brand, header .logo")
    NAV_LINKS = (By.CSS_SELECTOR, ".nav-link, nav a, .navbar-nav a")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], .search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], .search-btn")
    USER_MENU = (By.CSS_SELECTOR, ".user-menu, .dropdown-toggle, .profile-icon")
    USER_MENU_ITEMS = (By.CSS_SELECTOR, ".dropdown-menu a, .user-menu-items a")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a.logout, .logout-link, [data-action='logout']")
    NOTIFICATION_ICON = (By.CSS_SELECTOR, ".notifications, .notification-bell, .badge")
    MOBILE_TOGGLE = (By.CSS_SELECTOR, ".navbar-toggler, .mobile-menu-toggle, .hamburger")
    ACTIVE_LINK = (By.CSS_SELECTOR, ".nav-link.active, nav a.active, .navbar-nav a.active")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, self.ROOT, timeout)

    def navigate_to(self, link_text: str) -> "NavbarComponent":
        logger.info("Navbar | navigate_to | %s", link_text)
        links = self.find_elements(self.NAV_LINKS)
        if not links:
            raise RuntimeError(f"No nav links found. Locator: {self.NAV_LINKS}")
        for link in links:
            if link.text.strip() == link_text:
                link.click()
                return self
        raise ValueError(f"Nav link with text '{link_text}' not found")

    def navigate_by_href(self, href_fragment: str) -> "NavbarComponent":
        logger.info("Navbar | navigate_by_href | %s", href_fragment)
        locator = (By.CSS_SELECTOR, f"nav a[href*='{href_fragment}'], .navbar-nav a[href*='{href_fragment}']")
        self.click(locator)
        return self

    def search(self, query: str) -> "NavbarComponent":
        logger.info("Navbar | search | %s", query)
        self.fill(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        return self

    def open_user_menu(self) -> "NavbarComponent":
        logger.info("Navbar | open_user_menu")
        self.click(self.USER_MENU)
        return self

    def logout(self) -> "NavbarComponent":
        logger.info("Navbar | logout")
        self.open_user_menu()
        self.click(self.LOGOUT_LINK)
        self.wait_until_hidden(self.ROOT)
        return self

    def get_brand_text(self) -> str:
        return self.get_text(self.BRAND)

    def get_active_link_text(self) -> str:
        return self.get_text(self.ACTIVE_LINK)

    def get_all_link_texts(self) -> List[str]:
        return [el.text.strip() for el in self.find_elements(self.NAV_LINKS) if el.text.strip()]

    def get_notification_count(self) -> Optional[str]:
        try:
            return self.get_text(self.NOTIFICATION_ICON)
        except Exception:
            return None

    def is_mobile_menu_open(self) -> bool:
        return self.is_displayed(self.NAV_LINKS)

    def toggle_mobile_menu(self) -> "NavbarComponent":
        logger.info("Navbar | toggle_mobile_menu")
        self.click(self.MOBILE_TOGGLE)
        return self

    def is_logged_in(self) -> bool:
        return self.is_displayed(self.USER_MENU)
