import logging
from typing import List, Optional, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from components.base_component import BaseComponent

logger = logging.getLogger(__name__)


class SidebarComponent(BaseComponent):
    ROOT = (By.CSS_SELECTOR, ".sidebar, aside, [role='complementary'], .side-nav")

    MENU_ITEMS = (By.CSS_SELECTOR, ".sidebar-menu li a, .nav-item a, aside a")
    MENU_ITEM_ACTIVE = (By.CSS_SELECTOR, ".sidebar-menu li.active a, .nav-item.active a, li.active a")
    SECTION_HEADERS = (By.CSS_SELECTOR, ".sidebar-section h3, .nav-section h3, .menu-category")
    COLLAPSE_BUTTONS = (By.CSS_SELECTOR, ".collapse-btn, .toggle-btn, .expand-icon")
    TOGGLE_BUTTON = (By.CSS_SELECTOR, ".sidebar-toggle, .collapse-sidebar, #sidebarCollapse")
    SUBMENU = (By.CSS_SELECTOR, ".sub-menu, .nav-children, .collapse-menu")
    SUBMENU_ITEMS = (By.CSS_SELECTOR, ".sub-menu a, .nav-children a, .collapse-menu a")
    USER_INFO = (By.CSS_SELECTOR, ".sidebar-user, .user-profile, .profile-info")
    COLLAPSE_INDICATOR = (By.CSS_SELECTOR, ".collapse-icon, .arrow-icon, .chevron")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, self.ROOT, timeout)

    def navigate_to(self, item_text: str) -> "SidebarComponent":
        logger.info("Sidebar | navigate_to | %s", item_text)
        items = self.find_elements(self.MENU_ITEMS)
        if not items:
            raise RuntimeError(f"No sidebar menu items found. Locator: {self.MENU_ITEMS}")
        for item in items:
            if item.text.strip() == item_text:
                item.click()
                return self
        raise ValueError(f"Sidebar item with text '{item_text}' not found")

    def get_active_item_text(self) -> str:
        return self.get_text(self.MENU_ITEM_ACTIVE)

    def get_all_menu_items(self) -> List[str]:
        return [el.text.strip() for el in self.find_elements(self.MENU_ITEMS) if el.text.strip()]

    def expand_section(self, section_name: str) -> "SidebarComponent":
        logger.info("Sidebar | expand_section | %s", section_name)
        headers = self.find_elements(self.SECTION_HEADERS)
        for header in headers:
            if header.text.strip() == section_name:
                parent = header.find_element(By.XPATH, "..")
                collapse_btn = parent.find_element(*self.COLLAPSE_BUTTONS)
                collapse_btn.click()
                return self
        raise ValueError(f"Sidebar section '{section_name}' not found")

    def toggle_collapse(self) -> "SidebarComponent":
        logger.info("Sidebar | toggle_collapse")
        self.click(self.TOGGLE_BUTTON)
        return self

    def is_collapsed(self) -> bool:
        classes = self.get_attribute(self.ROOT, "class") or ""
        return "collapsed" in classes or "closed" in classes

    def get_user_info_text(self) -> str:
        return self.get_text(self.USER_INFO)

    def has_submenu(self, item_text: str) -> bool:
        items = self.find_elements(self.MENU_ITEMS)
        for item in items:
            if item.text.strip() == item_text:
                parent = item.find_element(By.XPATH, "..")
                submenus = parent.find_elements(*self.SUBMENU)
                return len(submenus) > 0
        return False
