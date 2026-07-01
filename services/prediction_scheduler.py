from __future__ import annotations

import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import structlog

from app.config import get_settings
from domain.prediction import PredictionHorizon, PredictionRun
from services.prediction_evaluator import PredictionEvaluator
from services.prediction_service import PredictionService
from services.watchlist_service import WatchlistService


logger = structlog.get_logger(__name__)


class PredictionScheduler:
    def __init__(
        self,
        prediction_service: PredictionService | None = None,
        evaluator: PredictionEvaluator | None = None,
        watchlist_service: WatchlistService | None = None,
    ) -> None:
        self._settings = get_settings()
        self._prediction_service = prediction_service or PredictionService()
        self._evaluator = evaluator or PredictionEvaluator()
        self._watchlist_service = watchlist_service or WatchlistService()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_daily_run_date: str | None = None
        self._last_refresh_run_date: str | None = None
        self._last_evaluation_run_date: str | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, name="investoros-scheduler", daemon=True)
        self._thread.start()
        logger.info("prediction_scheduler_started")

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("prediction_scheduler_stopped")

    def run_daily_prediction_job(self) -> PredictionRun:
        symbols = self._watchlist_service.seed_default_watchlist()
        horizons = self._configured_horizons()
        self._prediction_service.generate_daily_predictions(symbols, horizons)
        if self._prediction_service.last_run is None:
            return self._prediction_service.create_run("scheduled", len(symbols) * len(horizons))
        return self._prediction_service.last_run

    def run_data_refresh_job(self) -> None:
        self._watchlist_service.seed_default_watchlist()
        logger.info("data_refresh_job_completed")

    def run_evaluation_job(self):
        return self._evaluator.evaluate_due_predictions()

    def _run_loop(self) -> None:
        timezone = ZoneInfo(self._settings.scheduler_timezone)
        while not self._stop_event.is_set():
            now = datetime.now(timezone)
            if now.weekday() < 5:
                today_key = now.date().isoformat()
                current_time = now.strftime("%H:%M")
                if current_time >= self._settings.data_refresh_time and self._last_refresh_run_date != today_key:
                    self.run_data_refresh_job()
                    self._last_refresh_run_date = today_key
                if current_time >= self._settings.daily_prediction_time and self._last_daily_run_date != today_key:
                    self.run_daily_prediction_job()
                    self._last_daily_run_date = today_key
                if current_time >= self._settings.evaluation_time and self._last_evaluation_run_date != today_key:
                    self.run_evaluation_job()
                    self._last_evaluation_run_date = today_key
            self._stop_event.wait(30)

    def _configured_horizons(self) -> list[PredictionHorizon]:
        return [
            PredictionHorizon(value.strip())
            for value in self._settings.prediction_horizons.split(",")
            if value.strip()
        ]
