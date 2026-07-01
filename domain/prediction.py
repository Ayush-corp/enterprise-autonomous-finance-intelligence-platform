from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PredictionHorizon(str, Enum):
    ONE_DAY = "1D"
    SEVEN_DAYS = "7D"
    THIRTY_DAYS = "30D"
    NINETY_DAYS = "90D"


class PredictionStatus(str, Enum):
    OPEN = "open"
    EVALUATED = "evaluated"
    EXPIRED = "expired"
    FAILED = "failed"


class RunStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    RUNNING = "running"


class PredictionRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    run_type: str
    started_at: datetime
    finished_at: datetime | None = None
    status: RunStatus
    symbols_requested: int
    symbols_completed: int
    error_message: str | None = None
    metadata: dict[str, object] = Field(default_factory=dict)


class PredictionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    run_id: str | None = None
    symbol: str
    country: str
    horizon: PredictionHorizon
    prediction_date: date
    evaluation_due_date: date
    entry_price: float
    predicted_price: float
    predicted_return_pct: float
    recommendation: str
    confidence: float
    risk_level: str
    reasoning_summary: str
    graph_state: dict[str, object]
    created_at: datetime
    status: PredictionStatus
    response_metadata: dict[str, object] = Field(default_factory=dict)


class PredictionOutcome(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    prediction_id: str
    evaluation_date: date
    exit_price: float
    actual_return_pct: float
    benchmark_symbol: str
    benchmark_return_pct: float
    alpha_pct: float
    is_directionally_correct: bool
    is_market_beating: bool
    is_risk_adjusted_success: bool
    evaluated_at: datetime
    metadata: dict[str, object] = Field(default_factory=dict)


class WatchlistSymbol(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    symbol: str
    country: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, object] = Field(default_factory=dict)


class DataFreshnessRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    symbol: str
    country: str
    data_type: str
    last_refreshed_at: datetime
    fresh_until: datetime
    source: str
    metadata: dict[str, object] = Field(default_factory=dict)


class PredictionAccuracySummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_predictions: int
    evaluated_predictions: int
    open_predictions: int
    directional_accuracy_pct: float
    market_beating_pct: float
    avg_actual_return_pct: float
    avg_alpha_pct: float
    win_rate_pct: float
    by_horizon: dict[str, dict[str, float | int]]
    by_symbol: dict[str, dict[str, float | int]]
