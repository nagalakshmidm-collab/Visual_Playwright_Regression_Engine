# Visual Playwright Regression Engine (Local Sandbox Environment)

A Playwright + pytest harness for API mocking, UI assertions, and pixel-level visual regression testing against a fully fictional local sandbox.

## Sandbox endpoints

| Resource | URL |
|----------|-----|
| Application | `https://app.local-sandbox.internal/dashboard` |
| Metrics API | `https://api.local-sandbox.internal/v1/metrics` |

The application under test is **LocalHost Analytics Dashboard**. All routes and payloads are mocked locally via Playwright network interception—no external services are contacted.

## Setup

```bash
pip install -r requirements.txt
playwright install
```

## Run tests

```bash
# Headless (CI-friendly)
pytest -v

# Headed (debugging)
pytest -v --headed --slowmo=1000
```

Visual baselines are stored in `snapshots/`. Headed and headless runs maintain separate baseline images.
