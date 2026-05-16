# Selenium Python Automation Framework

Enterprise-grade Selenium automation framework built with Python 3.12+ and Pytest. Features Page Object Model, business flow orchestration, typed API testing, Allure reporting, Docker/Selenium Grid support, and multi-platform CI/CD (GitHub Actions + Jenkins).

---

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Execution Commands](#execution-commands)
- [Docker Usage](#docker-usage)
- [Coding Standards](#coding-standards)
- [Reporting Guide](#reporting-guide)
- [CI/CD Overview](#cicd-overview)
- [Contribution Guide](#contribution-guide)
- [Branching Strategy](#branching-strategy)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Sample Screenshots](#sample-screenshots)

---

## Architecture

```
selenium-python-framework/
├── tests/                    # Test cases (grouped by feature/module)
│   ├── test_saucedemo_login.py
│   ├── test_saucedemo_cart.py
│   ├── test_saucedemo_checkout.py
│   ├── test_saucedemo_inventory.py
│   ├── test_jsonplaceholder_api.py
│   ├── test_sample.py
│   └── test_offline_verification.py
├── pages/                    # Page Object Models
│   ├── base_page.py          # BasePage (38 methods, zero direct Selenium)
│   ├── login/
│   │   ├── login_page.py
│   │   └── login_locators.py
│   ├── inventory/
│   │   ├── inventory_page.py
│   │   └── inventory_locators.py
│   ├── cart/
│   │   ├── cart_page.py
│   │   └── cart_locators.py
│   └── checkout/
│       ├── checkout_step_one_page.py
│       ├── checkout_step_one_locators.py
│       ├── checkout_step_two_page.py
│       └── checkout_step_two_locators.py
├── flows/                    # Business flow orchestrations
│   ├── base_flow.py          # BaseFlow (driver, navigation helpers)
│   ├── login_flow.py         # LoginFlow (7 named user logins)
│   ├── cart_flow.py          # CartFlow (add/remove/checkout)
│   ├── checkout_flow.py      # CheckoutFlow (fill/continue/finish)
│   └── flow_utils.py         # Shared constants (users, products, errors)
├── components/               # Reusable UI components
│   ├── base_component.py
│   ├── navbar_component.py
│   ├── sidebar_component.py
│   ├── footer_component.py
│   └── modal_component.py
├── core/                     # Driver and wrapper infrastructure
│   ├── driver/
│   │   ├── browser_options.py    # Chrome/Firefox/Edge option builders
│   │   ├── driver_factory.py     # Local + remote/Selenium Grid drivers
│   │   └── driver_manager.py     # Thread-safe lifecycle (threading.Lock)
│   ├── wrappers/
│   │   ├── waits.py              # Fluent wait strategies (0.5s poll)
│   │   ├── element_actions.py    # Retry/intercept/fallback logic
│   │   └── javascript_actions.py # JS click/scroll/set_value/highlight
│   └── base_test.py
├── api/                      # API automation layer
│   ├── client/
│   │   └── api_client.py         # Typed HTTP client (GET/POST/PUT/PATCH/DELETE)
│   ├── models/
│   │   ├── post_model.py
│   │   ├── user_model.py
│   │   └── todo_model.py
│   ├── schemas/
│   │   ├── post_schema.py
│   │   ├── user_schema.py
│   │   └── todo_schema.py
│   └── services/
│       ├── base_service.py       # Typed CRUD helpers
│       └── jsonplaceholder_service.py  # 20 typed methods
├── config/                   # Configuration management
│   ├── settings.py           # Pydantic settings (validated)
│   ├── constants.py          # Enums (Browser, Environment, Timeout, etc.)
│   └── config_loader.py      # .env loader with cache + reload
├── data/                     # Test data
│   ├── factories/
│   │   ├── user_factory.py       # SauceDemo + random user generators
│   │   ├── product_factory.py
│   │   ├── api_payload_factory.py
│   │   └── base_factory.py
│   ├── json/                # Static JSON datasets
│   ├── test_data/            # Env-specific test data (dev/qa/staging/prod)
│   └── test_data.json
├── utils/                    # Utilities
│   ├── logger.py                 # Loguru (4 sinks, rotation, structured JSON)
│   ├── allure_manager.py         # Allure attachments + env properties
│   ├── screenshot_manager.py     # Timestamped captures + failure context
│   ├── retry_handler.py          # Tenacity-based (5 presets)
│   ├── data_generator.py         # Random data helpers
│   └── helpers.py                # JSON/YAML/file I/O utilities
├── docker/                   # Containerization
│   ├── Dockerfile                # Multi-stage (builder + runtime)
│   └── docker-compose.yml        # Hub + Chrome + Firefox + test-runner
├── jenkins/
│   └── Jenkinsfile               # Declarative pipeline (10 stages)
├── .github/workflows/
│   └── ci.yml                    # GitHub Actions (9 jobs)
├── reports/                  # Generated reports (gitignored)
├── screenshots/              # Failure screenshots (gitignored)
├── logs/                     # Framework logs (gitignored)
├── allure-results/           # Allure result files (gitignored)
├── conftest.py               # Pytest fixtures (session + function scope)
├── pytest.ini                # Pytest configuration
├── pyproject.toml             # Project metadata, ruff, bandit config
├── sonar-project.properties  # SonarQube configuration
├── requirements.txt          # Runtime dependencies
├── requirements-dev.txt      # Dev/CI tooling (ruff, bandit, pytest-cov)
└── .env.qa / .env.dev / .env.staging  # Environment config files
```

### Architecture Layers

```
┌──────────────────────────────────────────────────┐
│                    TESTS                          │
│  (thin, business-intent, flow-driven)            │
├──────────────────────────────────────────────────┤
│                    FLOWS                          │
│  (orchestrate pages → business workflows)        │
├──────────────────────────────────────────────────┤
│   PAGES         │   COMPONENTS    │    API        │
│  (UI inter-     │  (reusable      │  (typed CRUD  │
│   actions, no   │   UI fragments) │   services)   │
│   assertions)   │                 │               │
├─────────────────┴─────────────────┴──────────────┤
│                    CORE                           │
│  (driver factory, element waits, actions, JS)     │
├──────────────────────────────────────────────────┤
│      CONFIG     │    DATA        │    UTILS       │
│  (settings,     │  (factories,   │  (logging,     │
│   env loader)   │   JSON, env-   │   reporting,   │
│                 │   aware)       │   retry)       │
└──────────────────────────────────────────────────┘
```

### Design Principles

- **Composition over inheritance** — BasePage composes ElementActions, ElementWaits, JavaScriptActions
- **Separation of concerns** — Locators in `*_locators.py`, pages in `*_page.py`, flows orchestrate pages
- **No assertions in pages** — Pages return self or data; tests/assertions live in test functions
- **No time.sleep** — Explicit waits only (0.5s poll frequency)
- **No implicit waits** — `implicitly_wait` set at driver creation, but all element interactions use explicit waits
- **Thread-safe** — DriverManager uses `threading.Lock`, pytest-xdist compatible
- **Fluent APIs** — Methods return `self` for chaining (pages and flows)
- **Dual selectors** — SauceDemo locators use `data-test` first, CSS fallbacks second

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12+ |
| Test Framework | Pytest 9.x |
| Browser Automation | Selenium 4.x |
| API Testing | Requests + Pydantic models |
| Configuration | Pydantic-Settings + python-dotenv |
| Logging | Loguru (rotation, retention, structured) |
| Reporting | Allure Framework + pytest-html |
| Test Data | Faker, JSON datasets, factory pattern |
| Retry | Tenacity (5 preset strategies) |
| Driver Management | webdriver-manager |
| Parallel Execution | pytest-xdist |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions, Jenkins |
| Code Quality | Ruff, Bandit, SonarQube |
| Security | Snyk, pip-audit, Safety |

---

## Quick Start

```bash
# Clone and enter
git clone <repo-url>
cd selenium-python-framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run offline tests (no browser needed)
pytest -m offline -v

# Run smoke tests on QA env with Chrome
pytest -m smoke --env=qa --browser=chrome -v

# Run full regression with xdist
pytest -m regression --env=qa --browser=chrome --headless -n auto
```

---

## Environment Setup

### Configuration Files

Environment-specific `.env.` files in the project root:

| File | Environment | Tracked? |
|------|-------------|----------|
| `.env.example` | Template | Yes |
| `.env.dev` | Development | Yes |
| `.env.qa` | Quality Assurance | Yes |
| `.env.staging` | Staging | Yes |
| `.env` | Local overrides | **No** (gitignored) |
| `.env.production` | Production | **No** (gitignored) |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | `qa` | Target environment |
| `BROWSER` | `chrome` | Browser selection |
| `HEADLESS` | `false` | Headless mode |
| `INCOGNITO` | `false` | Private/incognito mode |
| `BROWSER_TIMEOUT` | `30` | Browser timeout (s) |
| `IMPLICIT_WAIT` | `10` | Implicit wait (s) |
| `EXPLICIT_WAIT` | `15` | Explicit wait timeout (s) |
| `PAGE_LOAD_TIMEOUT` | `30` | Page load timeout (s) |
| `BASE_URL` | — | Application base URL |
| `API_URL` | — | API base URL |
| `WEBDRIVER_REMOTE_URL` | — | Selenium Grid URL |
| `SCREENSHOT_ON_FAILURE` | `true` | Auto-capture on failure |
| `LOG_LEVEL` | `INFO` | Logging level |
| `RETRY_COUNT` | `0` | API retry attempts |
| `PARALLEL_WORKERS` | `1` | pytest-xdist workers |
| `ALLURE_DIR` | `allure-results` | Allure output directory |

### Creating a New Environment

```bash
cp .env.example .env.myenv
# Edit .env.myenv with your settings
ENV=myenv pytest -m smoke
```

---

## Execution Commands

### CLI Options

| Flag | Default | Choices | Description |
|------|---------|---------|-------------|
| `--browser` | from `.env` | chrome, firefox, edge, safari | Browser selection |
| `--env` | `qa` | dev, qa, staging, prod | Target environment |
| `--headless` | from `.env` | flag | Headless mode |
| `--incognito` | from `.env` | flag | Private/incognito mode |
| `--log-level-cli` | from `.env` | DEBUG, INFO, WARNING, ERROR, CRITICAL | Override log level |

### Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Critical path tests |
| `regression` | Full regression suite |
| `sanity` | Post-deployment checks |
| `e2e` | End-to-end user journeys |
| `api` | API contract and functional tests |
| `ui` | UI interaction tests |
| `integration` | Integration tests |
| `offline` | Static structure tests (no browser) |
| `slow` | Slow tests (>30s) |
| `flaky` | Known flaky tests requiring reruns |
| `parallel` | Tests safe for parallel execution |
| `data_driven` | Data-driven parameterized tests |
| `negative` | Negative/error path tests |

### Common Execution Patterns

```bash
# Offline structural verification (fast, no browser)
pytest -m offline -v

# API tests only
pytest -m api -v

# UI tests (exclude offline)
pytest -m "not offline" -v

# Smoke tests across browsers
pytest -m smoke --browser=chrome --env=qa
pytest -m smoke --browser=firefox --env=qa

# Headless mode
pytest -m smoke --headless -v

# Parallel execution
pytest -m regression -n auto --dist loadgroup

# With Allure reporting
pytest -m smoke --alluredir=allure-results

# Rerun flaky tests
pytest -m flaky --reruns 2 --reruns-delay 5

# Re-run last failed only
pytest --last-failed

# Debug logging
pytest -m smoke -v --log-level-cli=DEBUG

# HTML report
pytest -m smoke --html=reports/report.html --self-contained-html

# Stop on first failure
pytest -m smoke -x

# Code coverage
pytest -m offline --cov=pages --cov=flows --cov=core --cov=api --cov=utils --cov-report=term
```

### SauceDemo Test Users

All users share password `secret_sauce`:

| User | Type | Expected Behavior |
|------|------|------------------|
| `standard_user` | Normal | Full functionality |
| `locked_out_user` | Locked | Login error when attempting |
| `problem_user` | Problematic | Images fail to load, intermittent issues |
| `performance_glitch_user` | Slow | 5-10s delays on page transitions |
| `error_user` | Error | Various form errors on checkout |
| `visual_user` | Visual | Layout differences |

---

## Docker Usage

### Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Chrome Node  │────▶│              │◀────│ Firefox Node  │
│  :5901 (VNC)  │     │ Selenium Hub │     │ :5902 (VNC)   │
└──────────────┘     │  :4444/wd/hub │     └──────────────┘
                     └──────┬───────┘
                            │
┌────────────────────────────┴────────────────────┐
│              test-runner container               │
│  pytest --env=qa --browser=chrome --headless     │
│  WEBDRIVER_REMOTE_URL → http://selenium-hub:4444 │
│  Volumes: reports/ screenshots/ logs/            │
└──────────────────────────────────────────────────┘
```

### Prerequisites

- Docker Engine 24+
- Docker Compose V2

### Quick Start (Full Grid)

```bash
# Build image and start grid + tests
docker compose -f docker/docker-compose.yml up --build

# Run a specific test marker
docker compose -f docker/docker-compose.yml run --rm test-runner \
  -v --env=qa --browser=chrome --headless -m smoke

# Run with Firefox
docker compose -f docker/docker-compose.yml run --rm test-runner \
  -v --env=qa --browser=firefox --headless -m "not offline"

# Pass custom arguments
docker compose -f docker/docker-compose.yml run --rm test-runner \
  -v --env=qa --browser=chrome --headless \
  -m "not offline" -n auto \
  --alluredir=allure-results \
  --html=reports/docker_report.html --self-contained-html
```

### Standalone (No Grid)

```bash
# Build the image
docker build -f docker/Dockerfile -t selenium-framework .

# Run locally (single browser, requires browser in image)
docker run --rm \
  -v "$(pwd)/reports:/app/reports" \
  -v "$(pwd)/screenshots:/app/screenshots" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/allure-results:/app/allure-results" \
  selenium-framework -v --env=qa --headless -m "not offline"
```

### Viewing Tests via VNC

- Chrome: `vnc://localhost:5901` (password: `selenium`)
- Firefox: `vnc://localhost:5902` (password: `selenium`)

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `./reports` | `/app/reports` | HTML/Allure reports |
| `./screenshots` | `/app/screenshots` | Failure screenshots |
| `./logs` | `/app/logs` | Framework logs |
| `./allure-results` | `/app/allure-results` | Allure result files |

### Environment Variables (Docker)

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | `qa` | Target environment |
| `BROWSER` | `chrome` | Browser selection |
| `HEADLESS` | `true` | Headless mode |
| `WEBDRIVER_REMOTE_URL` | — | Selenium Grid URL (auto-set in compose) |

### Cleanup

```bash
# Stop and remove containers
docker compose -f docker/docker-compose.yml down

# Also remove volumes
docker compose -f docker/docker-compose.yml down -v --remove-orphans
```

---

## Coding Standards

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Directories | lowercase with hyphens | `page-objects` |
| Python files | snake_case | `login_page.py` |
| Classes | PascalCase | `LoginPage`, `CheckoutFlow` |
| Methods | snake_case | `click_login()`, `get_item_count()` |
| Variables | snake_case | `item_count`, `current_url` |
| Constants | UPPER_SNAKE_CASE | `STANDARD_USER`, `BASE_URL` |
| Locators | UPPER_SNAKE_CASE | `USERNAME_INPUT`, `LOGIN_BUTTON` |
| Test functions | snake_case prefixed `test_` | `test_valid_login` |
| Test classes | PascalCase prefixed `Test` | `TestLoginPositive` |
| Private members | `_` prefix | `_login_page`, `_locators` |
| Type aliases | PascalCase | `BrowserOptions` |

### Page Object Rules

1. **Locators are separated** — stored in `*_locators.py`, imported by pages
2. **No assertions in pages** — pages return data; tests assert
3. **No business logic in pages** — orchestration belongs in flows
4. **Methods return `self`** for fluent chaining (except getters)
5. **All element interactions go through BasePage** — zero direct Selenium calls
6. **Docstrings on all public methods** — describe what, not how

Example page structure:

```python
class LoginPage(BasePage):
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        super().__init__(driver, timeout)
        self._locators = LoginLocators()

    def open(self, base_url: str = "") -> "LoginPage":
        """Navigate to login page and wait for readiness."""
        self.open_url(base_url)
        self.wait_until_visible(self._locators.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Complete login flow: enter credentials and submit."""
        self.fill(self._locators.USERNAME_INPUT, username)
        self.fill(self._locators.PASSWORD_INPUT, password)
        self.click(self._locators.LOGIN_BUTTON)
        return self

    def get_error_message(self) -> str:
        """Return visible error text, or empty string."""
        if self.is_displayed(self._locators.ERROR_TEXT):
            return self.get_text(self._locators.ERROR_TEXT)
        return ""
```

### Flow Rules

1. **Flows orchestrate multiple pages** into business operations
2. **Methods return `self`** for chaining
3. **Properties** expose page state without breaking chains
4. **Named methods** for common operations (e.g. `login_as_standard_user()`)
5. **Tests call flows, not pages directly**

Example flow:

```python
class LoginFlow(BaseFlow):
    def login_as_standard_user(self) -> "LoginFlow":
        return self.login_as(STANDARD_USER)

    def attempt_login(self, username: str, password: str) -> "LoginFlow":
        self._login_page.open(self.base_url)
        self._login_page.enter_username(username)
        self._login_page.enter_password(password)
        self._login_page.click_login()
        return self

    @property
    def error_message(self) -> str:
        return self._login_page.get_error_message()
```

### Test Structure

```python
import pytest
from flows.login_flow import LoginFlow
from flows.flow_utils import STANDARD_USER, INVENTORY_TITLE

pytestmark = [pytest.mark.ui, pytest.mark.smoke]

class TestLoginPositive:
    def test_valid_login(self, driver, base_url):
        flow = LoginFlow(driver, base_url)
        flow.login_as_standard_user()
        assert flow.current_page.get_title_text() == INVENTORY_TITLE
```

### General Rules

- **No `time.sleep()`** — use explicit waits with 0.5s polling
- **No hardcoded values** — use constants, settings, or factories
- **Type hints required** on all function signatures
- **Docstrings required** on all public methods
- **Line length** — 120 characters
- **Quote style** — double quotes
- **Format** — Ruff (runs `ruff format .`)
- **Lint** — Ruff (runs `ruff check .`)

---

## Reporting Guide

### Allure Framework

Allure is the primary reporting framework. Generate and view reports:

```bash
# Run tests with Allure results
pytest -m smoke --alluredir=allure-results

# Generate HTML report (requires Allure CLI)
allure generate allure-results -o allure-report --clean

# Open report
allure open allure-report

# Serve live (dynamic updates as tests run)
allure serve allure-results
```

#### Allure Features Available

| Feature | Decorator / Method |
|---------|-------------------|
| Epic | `@allure.epic("name")` |
| Feature | `@allure.feature("name")` |
| Story | `@allure.story("name")` |
| Severity | `@allure.severity(allure.severity_level.CRITICAL)` |
| Step | `AllureManager.step("step name")` |
| Link | `@allure.link("url")` |
| Issue | `@allure.issue("url")` |
| Test Case | `@allure.testcase("url")` |

#### AllureManager Utilities

```python
from utils.allure_manager import AllureManager

# Attachments
AllureManager.attach_screenshot(driver, name="Login Page")
AllureManager.attach_page_source(driver)
AllureManager.attach_text(name="Response Body", content=response.text)
AllureManager.attach_json(name="API Response", data=api_response)
AllureManager.attach_html(name="DOM Snapshot", content=html_content)

# Decorator-style
with AllureManager.step("Login to application"):
    login_page.login(username, password)
```

### pytest-html Reports

```bash
pytest -m smoke --html=reports/report.html --self-contained-html
```

### JUnit XML (CI Integration)

```bash
pytest -m smoke --junitxml=reports/junit_report.xml
```

### Loguru Logging

Logs are written to `logs/` directory with rotation (10 MB) and retention (30 days):

| Sink | File | Level | Format |
|------|------|-------|--------|
| Console | stdout | Configured | Colorized, human-readable |
| File | `framework_YYYY-MM-DD.log` | DEBUG | Detailed with file/line |
| File | `errors_YYYY-MM-DD.log` | ERROR | Errors with tracebacks |
| JSON | `structured_YYYY-MM-DD.json` | DEBUG | Machine-readable (optional) |

### Screenshots

Automatic screenshot capture on test failure via `attach_on_failure` autouse fixture:

```
screenshots/
├── 20260516_120000_test_valid_login_FAILED.png
├── 20260516_120001_test_invalid_credentials_FAILED.png
└── ...
```

### Environment Properties

Written to `allure-results/environment.properties` at session end:

```
Base_URL: https://www.saucedemo.com
Browser: chrome
Environment: qa
Headless: True
Log_Level: INFO
Python_Version: 3.12.3
```

---

## CI/CD Overview

### GitHub Actions (`.github/workflows/ci.yml`)

Enterprise 9-job pipeline triggered by:
- Push to `main`, `develop`, `release/**`
- Pull requests to `main`, `develop`
- Scheduled weekdays at 06:00 UTC
- Manual dispatch (choice of env/browser/marker)

| Job | Trigger | Description |
|-----|---------|-------------|
| `lint` | Always | Ruff check + format |
| `security` | Always | Bandit SAST scan (non-blocking) |
| `sonarqube` | After lint | SonarQube with coverage (needs SONAR_TOKEN) |
| `snyk-scan` | Always | Snyk dependency scan (non-blocking) |
| `offline-tests` | Always | `pytest -m offline` with JUnit + Allure |
| `smoke-tests` | After lint+security | Chrome + Firefox + Edge matrix |
| `regression-tests` | After smoke | Chrome + Firefox matrix (Edge excluded) |
| `allure-report` | After test jobs | Aggregated Allure HTML report |
| `pipeline-summary` | Always | Markdown status table |

Key features:
- `concurrency.cancel-in-progress` — cancels duplicate runs
- `setup-python` with `cache: pip` — dependency caching
- Edge auto-installed via Microsoft repos
- Allure results aggregated across matrix jobs
- Coverage generated on offline tests (no browser needed)

### Jenkins Pipeline (`jenkins/Jenkinsfile`)

Declarative Pipeline with 10 stages:

| Stage | Description |
|-------|-------------|
| Checkout | SCM checkout |
| Dependencies | Docker build OR local venv (parallel) |
| Quality Gates | Lint + Security scan (parallel) |
| SonarQube Analysis | Coverage + SonarQube scan |
| Snyk Dependency Scan | Vulnerability scanning |
| Offline Tests | `pytest -m offline` |
| Smoke Tests | Browser matrix (Chrome/Firefox/Edge) |
| Regression Tests | Browser matrix (Edge excluded) |
| Allure Reporting | Aggregated report |
| Archive | Reports, screenshots, logs, coverage |

Parameters:

| Parameter | Options | Default |
|-----------|---------|---------|
| `EXECUTION_MODE` | docker, local | docker |
| `BROWSER` | chrome, firefox, edge, all | chrome |
| `ENVIRONMENT` | dev, qa, staging | qa |
| `MARKERS` | smoke, regression, sanity, e2e, offline | smoke |
| `HEADLESS` | boolean | true |
| `RUN_LINT` | boolean | true |
| `RUN_SECURITY` | boolean | true |

Required Jenkins plugins:
- Pipeline
- Allure Jenkins Plugin
- JUnit Plugin
- SonarQube Scanner
- Credentials Binding

### SonarQube (`sonar-project.properties`)

- Sources: `pages,flows,core,api,utils,config,data,components`
- Tests: `tests`
- Excluded from coverage: `tests/**`, `**/__init__.py`, `**/*_locators.py`, `**/conftest.py`, `config/constants.py`, `core/driver/**`, `docker/**`, `jenkins/**`
- Quality gate wait: 300s timeout

### Security Scanning

- **Bandit** — SAST scan (excludes `B101,B311,B403,B404,B603,B607`)
- **Snyk** — Dependency vulnerability scanning (`snyk test` + `snyk monitor` on main)
- **pip-audit** / **safety** — Additional dependency checks (via requirements-dev.txt)

---

## Contribution Guide

### Getting Started

1. Fork the repository
2. Create a feature branch (see [Branching Strategy](#branching-strategy))
3. Set up your local development environment
4. Make changes following the [Coding Standards](#coding-standards)
5. Run verification checks
6. Submit a pull request

### Verification Checklist

Before submitting a PR, run:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# 1. Lint
ruff check .
ruff format --check .

# 2. Security
bandit -r . --skip B101,B311,B403,B404,B603,B607

# 3. Offline tests (must pass 100%)
pytest -m offline -v --tb=long

# 4. Coverage for changed code
pytest -m offline \
  --cov=pages --cov=flows --cov=core --cov=api --cov=utils \
  --cov-report=term-missing

# 5. Browser tests (if applicable)
pytest -m smoke --env=qa --browser=chrome --headless -v
```

### Commit Messages

Follow conventional commits:

```
<type>(<scope>): <short summary>

<optional body>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `ci`, `chore`
Scope: module name (e.g. `login`, `cart`, `docker`, `ci`)

Examples:
```
feat(login): add biometric authentication flow
fix(cart): handle empty badge edge case
docs(readme): update Docker usage examples
ci(actions): reduce smoke test timeout to 15m
```

### Pull Request Process

1. Ensure all checks pass (lint, security, offline tests)
2. Update documentation if adding/changing features
3. Add or update tests for new functionality
4. Request review from at least one maintainer
5. Squash commits before merge

---

## Branching Strategy

### Branch Naming

| Branch | Pattern | Source | Description |
|--------|---------|--------|-------------|
| `main` | `main` | — | Production-ready code, protected |
| `develop` | `develop` | `main` | Integration branch for features |
| `release/` | `release/v*.*.*` | `develop` | Release preparation |
| `feature/` | `feature/<issue>-<short-desc>` | `develop` | New features |
| `fix/` | `fix/<issue>-<short-desc>` | `develop` | Bug fixes |
| `hotfix/` | `hotfix/<issue>-<short-desc>` | `main` | Critical production fixes |
| `chore/` | `chore/<short-desc>` | `develop` | Tooling, dependencies, docs |
| `refactor/` | `refactor/<short-desc>` | `develop` | Code improvements |

### Workflow

```
main ──────●────────────────────●─────────────●──
            \                  / \           /
develop     ●──●──●──●──●────●───●──●──●──●──────
                 \          /       \      /
feature/          ●──●──●─●         ●──●─●
```

1. **Feature branches** branch from `develop`, merge back via PR
2. **Release branches** branch from `develop` when ready, merge to `main` and back to `develop`
3. **Hotfix branches** branch from `main`, merge to both `main` and `develop`
4. **Direct commits to `main` and `develop` are prohibited** — all changes go through PRs
5. **PRs require** passing CI checks and at least one approval

---

## Troubleshooting Guide

### Common Issues

#### Selenium WebDriver

| Issue | Cause | Solution |
|-------|-------|----------|
| `NoSuchDriverException` | Missing browser driver | `webdriver-manager` auto-installs; ensure no proxy blocking |
| `SessionNotCreatedException` | Browser/Driver version mismatch | Update browser or pin `webdriver-manager` version |
| `WebDriverException: chrome not reachable` | Browser crash or resource exhaustion | Reduce `-n` workers, increase `shm_size` in Docker |
| `StaleElementReferenceException` | DOM element re-rendered | Use `stale_element_retry` decorator on the method |
| `ElementClickInterceptedException` | Overlay/modals blocking element | Use `js_click()` or wait for overlay to disappear |
| `TimeoutException` | Element not found within wait time | Increase `EXPLICIT_WAIT`, check locator correctness |

#### Docker

| Issue | Cause | Solution |
|-------|-------|----------|
| `Container is unhealthy` | Grid nodes not starting in time | Increase `start_period` in healthcheck |
| `Connection refused: selenium-hub:4444` | Hub not ready when tests start | Ensure `depends_on` has `condition: service_healthy` |
| `Test failed: cannot open display` | Headless not set | Add `--headless` flag or set `HEADLESS=true` |
| `Disk full: /var/lib/docker` | Orphaned containers/volumes | `docker system prune -af --volumes` |
| VNC connection refused | Port not published on host | Check `ports` mapping in compose file |

#### Tests

| Issue | Cause | Solution |
|-------|-------|----------|
| `test_cleanup_old_files` fails | Missing `import os` in test | Add `import os` to the test function |
| Tests fail only in CI | Headless rendering differences | Use explicit waits, avoid CSS `:hover` dependent tests |
| `AssertionError` intermittently | Flaky element timing | Add `@flaky_test_retry` or increase wait timeout |
| Parallel tests interfering | Shared state between tests | Use `--dist loadgroup` or ensure test isolation |
| SauceDemo credentials fail | Password changed | Verify `secret_sauce` in `flows/flow_utils.py` |

#### Configuration

| Issue | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: .env.qa` | Missing env file | `cp .env.example .env.qa` |
| `ValueError: URL must start with http` | Invalid `BASE_URL` | Ensure URL includes `https://` |
| API tests hitting wrong endpoint | Wrong `API_URL` | Check `.env.qa` `API_URL` value |
| Loguru double initialization | Logger configured twice | `LoggerConfig.reset()` before reconfiguring |

### Debugging Tips

```bash
# Run with DEBUG logging
pytest -m smoke --log-level-cli=DEBUG -v --tb=long

# Run a single test
pytest tests/test_saucedemo_login.py::TestLoginPositive::test_valid_login -vvs

# Skip slow tests
pytest -m "not slow" -v

# Re-run only failed tests from last run
pytest --last-failed -v

# Pause on failure for debugging
pytest -m smoke -x --pdb

# Check browser console logs (Chrome)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
caps = DesiredCapabilities.CHROME.copy()
caps["goog:loggingPrefs"] = {"browser": "ALL"}
```

### Logs Location

| Log Type | Location | Content |
|----------|----------|---------|
| Framework debug logs | `logs/framework_YYYY-MM-DD.log` | All framework activity |
| Error logs | `logs/errors_YYYY-MM-DD.log` | Errors with full tracebacks |
| Test logs | `logs/` | Per-test log output |
| Console | stdout/stderr | Real-time colored output |

### Getting Help

- Check the logs in `logs/` for detailed error context
- Enable `--log-level-cli=DEBUG` for verbose output
- Review failure screenshots in `screenshots/`
- Check Allure report for step-by-step failure analysis
- Open an issue at the repository with:
  - Full error traceback
  - Test command used
  - Environment details (OS, browser version, Python version)
  - Relevant log excerpts

---

## Sample Screenshots

### Console Output

```
tests/test_saucedemo_login.py::TestLoginPositive::test_valid_login PASSED [  7%]
tests/test_saucedemo_login.py::TestLoginPositive::test_logout PASSED     [ 14%]
tests/test_saucedemo_login.py::TestLoginNegative::test_locked_out_user PASSED [ 21%]
tests/test_saucedemo_cart.py::TestCartWithItems::test_cart_contains_added_items PASSED [ 28%]
```

### Allure Report Dashboard

The Allure report dashboard shows:
- **Overview** — total tests, pass rate, duration, severity breakdown
- **Categories** — failed tests grouped by failure type
- **Suites** — test class hierarchy
- **Graphs** — duration trends, pass/fail over time
- **Timeline** — test execution timeline (useful for parallel runs)
- **Behaviors** — epic/feature/story hierarchy
- **Packages** — module-level breakdown

### Sample Execution

```
$ pytest -m smoke --env=qa --browser=chrome --headless -v

============================= test session starts ==============================
platform darwin -- Python 3.12.6, pytest-9.0.3, pluggy-1.5.0
rootdir: /Users/user/selenium-python-framework
configfile: pytest.ini
plugins: xdist-3.6.1, html-4.1.1, rerunfailures-14.0, allure-pytest-2.13.2
collected 173 items / 120 deselected / 53 selected

tests/test_saucedemo_login.py::TestLoginPositive::test_valid_login PASSED [  2%]
tests/test_saucedemo_login.py::TestLoginPositive::test_logout PASSED     [  4%]
...
tests/test_saucedemo_checkout.py::TestCheckout::test_complete_order PASSED [ 98%]

= 53 passed, 120 deselected, 1 warning in 142.35s (0:02:22) =
```

### Sample Allure Report

```
┌──────────────────────────────────────────────────────────┐
│                  Allure Report Overview                    │
├──────────────────────────────────────────────────────────┤
│  Tests: 53  │  Passed: 53  │  Failed: 0  │  Duration: 2m │
├──────────────────────────────────────────────────────────┤
│  Smoke Tests                                              │
│  ├── Login Flow                                           │
│  │   ├── ✅ test_valid_login (1.2s)                      │
│  │   ├── ✅ test_logout (0.8s)                           │
│  │   └── ✅ test_locked_out_user (0.6s)                  │
│  ├── Cart Flow                                            │
│  │   ├── ✅ test_cart_contains_added_items (1.5s)         │
│  │   └── ✅ test_checkout_navigation (0.9s)              │
│  └── Checkout Flow                                        │
│      ├── ✅ test_complete_order (2.1s)                    │
│      └── ✅ test_checkout_error_validation (0.7s)         │
└──────────────────────────────────────────────────────────┘
```

### Sample Log Output

```
2026-05-16 12:00:00.123 | INFO     | app              | ============================================================
2026-05-16 12:00:00.123 | INFO     | app              | Test session started | env=qa | browser=chrome
2026-05-16 12:00:00.123 | INFO     | app              | ============================================================
2026-05-16 12:00:00.456 | INFO     | app              | TEST  │ tests/test_saucedemo_login.py::TestLoginPositive::test_valid_login │ setup
2026-05-16 12:00:00.789 | INFO     | LoginPage         | navigate | https://www.saucedemo.com
2026-05-16 12:00:01.234 | INFO     | LoginPage         | login | standard_user
2026-05-16 12:00:02.567 | INFO     | app              | TEST  │ tests/test_saucedemo_login.py::TestLoginPositive::test_valid_login │ PASSED (2.111s)
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Support

- Report issues at the repository issue tracker
- For questions, contact the QA team
