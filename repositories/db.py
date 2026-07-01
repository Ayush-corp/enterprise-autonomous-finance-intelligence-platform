from __future__ import annotations

import sqlite3
from pathlib import Path

from app.config import get_settings


def get_db_path() -> Path:
    settings = get_settings()
    path = Path(settings.sqlite_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path is not None else get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path: str | Path | None = None) -> None:
    with get_connection(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS prediction_runs (
                id TEXT PRIMARY KEY,
                run_type TEXT NOT NULL,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                symbols_requested INTEGER NOT NULL,
                symbols_completed INTEGER NOT NULL,
                error_message TEXT,
                metadata_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS predictions (
                id TEXT PRIMARY KEY,
                run_id TEXT,
                symbol TEXT NOT NULL,
                country TEXT NOT NULL,
                horizon TEXT NOT NULL,
                prediction_date TEXT NOT NULL,
                evaluation_due_date TEXT NOT NULL,
                entry_price REAL NOT NULL,
                predicted_price REAL NOT NULL,
                predicted_return_pct REAL NOT NULL,
                recommendation TEXT NOT NULL,
                confidence REAL NOT NULL,
                risk_level TEXT NOT NULL,
                reasoning_summary TEXT NOT NULL,
                graph_state_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(run_id) REFERENCES prediction_runs(id)
            );

            CREATE INDEX IF NOT EXISTS idx_predictions_symbol_horizon_created
            ON predictions(symbol, horizon, created_at);

            CREATE INDEX IF NOT EXISTS idx_predictions_due_status
            ON predictions(evaluation_due_date, status);

            CREATE TABLE IF NOT EXISTS prediction_outcomes (
                id TEXT PRIMARY KEY,
                prediction_id TEXT NOT NULL UNIQUE,
                evaluation_date TEXT NOT NULL,
                exit_price REAL NOT NULL,
                actual_return_pct REAL NOT NULL,
                benchmark_symbol TEXT NOT NULL,
                benchmark_return_pct REAL NOT NULL,
                alpha_pct REAL NOT NULL,
                is_directionally_correct INTEGER NOT NULL,
                is_market_beating INTEGER NOT NULL,
                is_risk_adjusted_success INTEGER NOT NULL,
                evaluated_at TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                FOREIGN KEY(prediction_id) REFERENCES predictions(id)
            );

            CREATE TABLE IF NOT EXISTS watchlist_symbols (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL UNIQUE,
                country TEXT NOT NULL,
                is_active INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS data_freshness (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                country TEXT NOT NULL,
                data_type TEXT NOT NULL,
                last_refreshed_at TEXT NOT NULL,
                fresh_until TEXT NOT NULL,
                source TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                UNIQUE(symbol, country, data_type)
            );

            CREATE TABLE IF NOT EXISTS analysis_runs (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                country TEXT NOT NULL,
                horizon TEXT NOT NULL,
                request_payload_json TEXT NOT NULL,
                graph_state_json TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
