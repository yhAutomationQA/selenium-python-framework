import warnings
from typing import Optional

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = Field(default="qa")
    base_url: str = Field(default="")
    api_url: str = Field(default="")

    browser: str = Field(default="chrome")
    headless: bool = Field(default=False)
    incognito: bool = Field(default=False)
    browser_timeout: int = Field(default=30, ge=5, le=300)
    implicit_wait: int = Field(default=10, ge=0, le=120)
    explicit_wait: int = Field(default=15, ge=0, le=120)
    page_load_timeout: int = Field(default=30, ge=5, le=300)

    screenshot_on_failure: bool = Field(default=True)
    log_level: str = Field(default="INFO")
    retry_count: int = Field(default=0, ge=0, le=10)
    parallel_workers: int = Field(default=1, ge=1, le=32)

    webdriver_remote_url: Optional[str] = Field(default=None)
    webdriver_download_path: Optional[str] = Field(default=None)
    allure_dir: str = Field(default="allure-results")

    @field_validator("base_url", "api_url")
    @classmethod
    def validate_urls(cls, v: str) -> str:
        if v and not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError(f"URL must start with http:// or https://, got: '{v}'")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = v.upper()
        if upper not in allowed:
            raise ValueError(f"Invalid log_level: {v}. Allowed: {allowed}")
        return upper

    @field_validator("browser")
    @classmethod
    def validate_browser(cls, v: str) -> str:
        allowed = {"chrome", "firefox", "edge", "safari"}
        lower = v.lower()
        if lower not in allowed:
            raise ValueError(f"Invalid browser: {v}. Allowed: {allowed}")
        return lower

    @model_validator(mode="after")
    def warn_if_base_url_missing(self) -> "Settings":
        if not self.base_url:
            warnings.warn(
                f"BASE_URL is not configured for environment '{self.env}'. "
                f"Set it in .env.{self.env} or export BASE_URL.",
                stacklevel=2,
            )
        return self

    model_config = SettingsConfigDict(extra="ignore")
