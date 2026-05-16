# Selenium Python Automation Framework

Enterprise-grade Selenium automation framework built with Python 3.12+ and Pytest.

## Architecture

```
├── tests/            # Test cases (grouped by feature/module)
├── pages/            # Page Object Models
├── flows/            # Business flow orchestrations
├── components/       # Reusable UI components
├── core/             # Driver factory, base classes
├── api/              # API client & request wrappers
├── config/           # Environment & app configuration
├── data/             # Test data (JSON, YAML, fixtures)
├── utils/            # Logger, helpers, data generators
├── reports/          # Generated HTML reports
├── screenshots/      # Failure screenshots
├── logs/             # Framework logs
├── docker/           # Dockerfile & docker-compose
├── jenkins/          # Jenkins pipeline
└── .github/workflows/ # GitHub Actions CI
```

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v -m smoke --env=qa --browser=chrome
```

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--browser` | `chrome` | Browser: chrome, firefox, edge |
| `--env` | `qa` | Environment: dev, qa, staging, prod |
| `--headless` | `False` | Run headless mode |

## Markers

- `smoke` — Critical path
- `regression` — Full regression
- `sanity` — Post-deployment checks
- `e2e` — End-to-end flows
- `api` — API tests
- `ui` — UI tests
- `slow` — Slow tests
- `flaky` — Unstable tests

## CI/CD

- **GitHub Actions**: `.github/workflows/ci.yml`
- **Jenkins**: `jenkins/Jenkinsfile`
- **Docker**: `docker/Dockerfile` + `docker/docker-compose.yml`
