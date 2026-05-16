import logging
from typing import Dict, List, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from components.base_component import BaseComponent

logger = logging.getLogger(__name__)


class FooterComponent(BaseComponent):
    ROOT = (By.CSS_SELECTOR, "footer, .footer, [role='contentinfo']")

    COPYRIGHT = (By.CSS_SELECTOR, ".copyright, footer .copy, .footer-copyright")
    SOCIAL_LINKS = (By.CSS_SELECTOR, ".social-links a, .social-icons a, .follow-us a")
    FOOTER_LINKS = (By.CSS_SELECTOR, "footer a, .footer a, .footer-links a")
    NEWSLETTER_EMAIL = (By.CSS_SELECTOR, "#newsletter-email, .newsletter input[type='email']")
    NEWSLETTER_SUBMIT = (By.CSS_SELECTOR, ".newsletter button, #newsletter-submit")
    BACK_TO_TOP = (By.CSS_SELECTOR, ".back-to-top, #backToTop, .scroll-top")
    YEAR_TEXT = (By.CSS_SELECTOR, ".copyright .year, .footer-year, [data-testid='year']")
    SECTIONS = (By.CSS_SELECTOR, ".footer-section, .footer-column, footer .col")
    SECTION_HEADERS = (By.CSS_SELECTOR, ".footer-section h4, .footer-column h4, footer h4")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, self.ROOT, timeout)

    def get_copyright_text(self) -> str:
        return self.get_text(self.COPYRIGHT)

    def click_social_link(self, platform: str) -> "FooterComponent":
        logger.info("Footer | click_social_link | %s", platform)
        links = self.find_elements(self.SOCIAL_LINKS)
        for link in links:
            href = link.get_attribute("href") or ""
            title = link.get_attribute("title") or ""
            text = link.text.strip().lower()
            platform_lower = platform.lower()
            if platform_lower in href.lower() or platform_lower in title.lower() or platform_lower == text:
                link.click()
                return self
        raise ValueError(f"Social link for '{platform}' not found")

    def get_social_link_urls(self) -> Dict[str, str]:
        result = {}
        links = self.find_elements(self.SOCIAL_LINKS)
        for link in links:
            href = link.get_attribute("href") or ""
            text = link.text.strip() or href
            result[text] = href
        return result

    def get_all_footer_links(self) -> List[str]:
        return [el.text.strip() for el in self.find_elements(self.FOOTER_LINKS) if el.text.strip()]

    def click_footer_link(self, link_text: str) -> "FooterComponent":
        logger.info("Footer | click_footer_link | %s", link_text)
        links = self.find_elements(self.FOOTER_LINKS)
        for link in links:
            if link.text.strip() == link_text:
                link.click()
                return self
        raise ValueError(f"Footer link with text '{link_text}' not found")

    def subscribe_to_newsletter(self, email: str) -> "FooterComponent":
        logger.info("Footer | subscribe | %s", email)
        self.fill(self.NEWSLETTER_EMAIL, email)
        self.click(self.NEWSLETTER_SUBMIT)
        return self

    def scroll_to_footer(self) -> "FooterComponent":
        logger.info("Footer | scroll_to_footer")
        self.scroll_to(self.ROOT)
        return self

    def get_section_headers(self) -> List[str]:
        return [el.text.strip() for el in self.find_elements(self.SECTION_HEADERS) if el.text.strip()]

    def click_back_to_top(self) -> "FooterComponent":
        logger.info("Footer | back_to_top")
        self.click(self.BACK_TO_TOP)
        return self
