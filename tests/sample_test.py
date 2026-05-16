import pytest
from selenium.webdriver.common.by import By
from core.base_test import BaseTest


@pytest.mark.smoke
@pytest.mark.ui
class TestSmoke(BaseTest):

    def test_page_title(self, base_url: str):
        self.navigate_to(base_url)
        title = self.get_title()
        assert title is not None, "Page title should not be None"

    def test_page_loads_successfully(self, base_url: str):
        self.navigate_to(base_url)
        current_url = self.get_current_url()
        assert base_url in current_url, f"Expected {base_url} to be in {current_url}"


@pytest.mark.regression
class TestRegression(BaseTest):

    @pytest.mark.parametrize("path", ["/", "/login", "/about"])
    def test_multiple_pages_load(self, base_url: str, path: str):
        url = f"{base_url}{path}"
        self.navigate_to(url)
        assert self.get_title() is not None
