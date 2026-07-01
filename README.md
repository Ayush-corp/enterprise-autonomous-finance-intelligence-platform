# Autonomous Investing Agent

FastAPI service that orchestrates a multi-step investing analysis workflow with LangGraph. The default local mode uses deterministic mock providers, so the API can run and test without external market data or LLM credentials.

## Project Layout

- `app/` - FastAPI entrypoint, routers, configuration, dependency wiring, logging, and exceptions.
- `domain/` - Pydantic models used as API and graph state contracts.
- `graph/` - LangGraph workflow and graph helper functions.
- `infrastructure/` - Provider implementations for LLM, market, and news integrations.
- `services/` - Application service abstractions that coordinate providers.
- `agents/` - Reusable agent base class and focused domain agent wrappers.
- `tests/` - Unit and integration tests.

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

## Run

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs`.

## Test

```powershell
pytest
```

## API

Health check:

```http
GET /health
```

Analysis:

```http
POST /api/v1/analyze
Content-Type: application/json

{"symbol": "RELIANCE.NS"}
```

Country-aware routing:

```http
POST /api/v1/analyze
Content-Type: application/json

{"symbol": "RELIANCE", "country": "IN"}
```

`country="IN"` routes market data through `yfinance`; `country="US"` routes market data through Massive/Polygon.

Watchlist:

```http
POST /api/v1/watchlist
GET /api/v1/watchlist
DELETE /api/v1/watchlist/{symbol}
```

Predictions:

```http
POST /api/v1/predictions/run
GET /api/v1/predictions/latest
GET /api/v1/predictions/{symbol}
GET /api/v1/predictions/{symbol}/latest
POST /api/v1/predictions/evaluate-due
POST /api/v1/predictions/{prediction_id}/evaluate
```

Accuracy:

```http
GET /api/v1/accuracy
GET /api/v1/accuracy/{symbol}?horizon=1D&days=90
```

CLI jobs:

```powershell
python scripts/seed_watchlist.py
python scripts/run_daily_predictions.py
python scripts/evaluate_due_predictions.py
```

Scheduler settings are disabled by default. Set `ENABLE_SCHEDULER=true` to run daily jobs inside the API process.
