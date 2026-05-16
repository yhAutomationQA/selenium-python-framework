from enum import Enum


class Browser(str, Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"


class Environment(str, Enum):
    DEV = "dev"
    QA = "qa"
    STAGING = "staging"
    PROD = "prod"


class Timeout(float, Enum):
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    PAGE_LOAD = 30
    POLL_FREQUENCY = 0.5


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DriverPath(str, Enum):
    CHROME = "chrome"
    FIREFOX = "gecko"
    EDGE = "edge"


class Directory:
    REPORTS = "reports"
    SCREENSHOTS = "screenshots"
    LOGS = "logs"
    ALLURE_RESULTS = "allure-results"
    ALLURE_REPORT = "allure-report"
    DOWNLOADS = "downloads"
