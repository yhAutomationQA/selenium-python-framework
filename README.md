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

## Docker

Run tests inside a container with Selenium Grid (Chrome + Firefox nodes).

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
```

### Standalone (No Grid, Local Browser in Container)

```bash
# Build the image
docker build -f docker/Dockerfile -t selenium-framework .

# Run locally (requires Chrome installed in image — use for single-browser runs)
docker run --rm -v "$(pwd)/reports:/app/reports" \
                -v "$(pwd)/screenshots:/app/screenshots" \
                -v "$(pwd)/logs:/app/logs" \
                -v "$(pwd)/allure-results:/app/allure-results" \
  selenium-framework -v --env=qa --headless -m "not offline"
```

### Grid Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Chrome Node  │────▶│              │◀────│ Firefox Node  │
│  :5901 (VNC)  │     │ Selenium Hub │     │ :5902 (VNC)   │
└──────────────┘     │  :4444/wd/hub │     └──────────────┘
                     └──────┬───────┘
                            │
┌───────────────────────────┴────────────┐
│          test-runner container          │
│  pytest --env=qa --headless             │
│  WebDriverRemoteUrl → hub:4444          │
│  volumes: reports/ screenshots/ logs/   │
└─────────────────────────────────────────┘
```

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `./reports` | `/app/reports` | HTML/Allure reports |
| `./screenshots` | `/app/screenshots` | Failure screenshots |
| `./logs` | `/app/logs` | Framework logs |
| `./allure-results` | `/app/allure-results` | Allure result files |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | `qa` | Target environment (dev/qa/staging/prod) |
| `BROWSER` | `chrome` | Browser (chrome/firefox/edge) |
| `HEADLESS` | `true` | Headless mode |
| `WEBDRIVER_REMOTE_URL` | — | Selenium Grid URL (auto-set in compose) |

### Viewing Tests via VNC

- Chrome: `vnc://localhost:5901` (password: `selenium`)
- Firefox: `vnc://localhost:5902` (password: `selenium`)

### Cleanup

```bash
# Stop and remove all containers
docker compose -f docker/docker-compose.yml down

# Also remove volumes
docker compose -f docker/docker-compose.yml down -v
```

## CI/CD

- **GitHub Actions**: `.github/workflows/ci.yml`
- **Jenkins**: `jenkins/Jenkinsfile`
- **Docker**: `docker/Dockerfile` + `docker/docker-compose.yml`
