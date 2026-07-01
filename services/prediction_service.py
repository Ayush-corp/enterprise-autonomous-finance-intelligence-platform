from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import structlog

from domain.graph_state import GraphState
from domain.prediction import PredictionHorizon, PredictionRecord, PredictionRun, PredictionStatus, RunStatus, WatchlistSymbol
from graph.graph import graph
from app.config import get_settings
from app.dependencies.services import get_market_provider
from repositories.analysis_repository import AnalysisRepository
from repositories.prediction_repository import PredictionRepository
from services.data_freshness_service import DataFreshnessService


logger = structlog.get_logger(__name__)


class PredictionService:
    horizon_days = {
        PredictionHorizon.ONE_DAY: 1,
        PredictionHorizon.SEVEN_DAYS: 7,
        PredictionHorizon.THIRTY_DAYS: 30,
        PredictionHorizon.NINETY_DAYS: 90,
    }

    def __init__(
        self,
        prediction_repository: PredictionRepository | None = None,
        analysis_repository: AnalysisRepository | None = None,
        freshness_service: DataFreshnessService | None = None,
        db_path: str | Path | None = None,
    ) -> None:
        self._prediction_repository = prediction_repository or PredictionRepository(db_path)
        self._analysis_repository = analysis_repository or AnalysisRepository(db_path)
        self._freshness_service = freshness_service or DataFreshnessService(db_path=db_path)
        self.last_run: PredictionRun | None = None

    def create_run(self, run_type: str, symbols_requested: int) -> PredictionRun:
        run = PredictionRun(
            id=str(uuid4()),
            run_type=run_type,
            started_at=datetime.utcnow(),
            finished_at=None,
            status=RunStatus.RUNNING,
            symbols_requested=symbols_requested,
            symbols_completed=0,
            error_message=None,
            metadata={},
        )
        return self._prediction_repository.save_run(run)

    def finish_run(
        self,
        run: PredictionRun,
        *,
        status: RunStatus,
        symbols_completed: int,
        error_message: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> PredictionRun:
        finished = run.model_copy(
            update={
                "finished_at": datetime.utcnow(),
                "status": status,
                "symbols_completed": symbols_completed,
                "error_message": error_message,
                "metadata": metadata or run.metadata,
            }
        )
        return self._prediction_repository.save_run(finished)

    def generate_prediction(
        self,
        symbol: str,
        country: str | None,
        horizon: PredictionHorizon,
        run_id: str | None = None,
        force_refresh: bool = False,
    ) -> PredictionRecord:
        normalized_symbol = symbol.strip().upper()
        normalized_country = (country or self._infer_country(normalized_symbol)).strip().upper()
        state = GraphState(symbol=normalized_symbol, country=normalized_country, horizon=horizon.value)
        result = asyncio.run(graph.ainvoke(state))
        graph_state = GraphState.model_validate(result)
        benchmark_symbol = get_settings().default_benchmark_symbol
        benchmark_snapshot = asyncio.run(get_market_provider().get_snapshot(benchmark_symbol, "IN"))
        graph_state.metadata["benchmark_symbol"] = benchmark_symbol
        graph_state.metadata["benchmark_entry_price"] = benchmark_snapshot.current_price
        self._analysis_repository.save_analysis(
            symbol=normalized_symbol,
            country=normalized_country,
            horizon=horizon.value,
            request_payload={
                "symbol": normalized_symbol,
                "country": normalized_country,
                "horizon": horizon.value,
                "force_refresh": force_refresh,
            },
            graph_state=graph_state,
        )

        prediction = self._record_from_state(
            graph_state=graph_state,
            horizon=horizon,
            run_id=run_id,
        )
        saved = self._prediction_repository.save_prediction(prediction)
        self._freshness_service.mark_refreshed(normalized_symbol, normalized_country, "market", "market_provider")
        self._freshness_service.mark_refreshed(normalized_symbol, normalized_country, "news", "news_provider")
        return saved

    def generate_daily_predictions(
        self,
        symbols: list[WatchlistSymbol],
        horizons: list[PredictionHorizon],
    ) -> list[PredictionRecord]:
        run = self.create_run("scheduled", len(symbols) * len(horizons))
        predictions: list[PredictionRecord] = []
        errors: list[str] = []
        for item in symbols:
            for horizon in horizons:
                try:
                    predictions.append(
                        self.generate_prediction(
                            item.symbol,
                            item.country,
                            horizon,
                            run_id=run.id,
                        )
                    )
                except Exception as exc:
                    logger.exception(
                        "daily_prediction_failed",
                        symbol=item.symbol,
                        country=item.country,
                        horizon=horizon.value,
                    )
                    errors.append(f"{item.symbol}:{horizon.value}:{exc}")
        status = RunStatus.SUCCESS if not errors else RunStatus.PARTIAL if predictions else RunStatus.FAILED
        self.last_run = self.finish_run(
            run,
            status=status,
            symbols_completed=len(predictions),
            error_message="; ".join(errors) if errors else None,
            metadata={"errors": errors},
        )
        return predictions

    def _record_from_state(
        self,
        *,
        graph_state: GraphState,
        horizon: PredictionHorizon,
        run_id: str | None,
    ) -> PredictionRecord:
        if graph_state.market is None or graph_state.forecast is None or graph_state.recommendation is None or graph_state.risk is None:
            raise ValueError("GraphState is missing required prediction outputs")

        prediction_date = date.today()
        entry_price = graph_state.market.current_price
        predicted_price = graph_state.forecast.predicted_price
        predicted_return_pct = ((predicted_price - entry_price) / entry_price) * 100
        confidence = graph_state.recommendation.confidence
        metadata = {
            "disclaimer": "This is not financial advice. Use for research and education only.",
            "data_freshness": self._freshness_service.freshness_metadata(graph_state.symbol, graph_state.country),
        }
        if confidence < 0.6:
            metadata["confidence_warning"] = "Low confidence prediction"

        return PredictionRecord(
            id=str(uuid4()),
            run_id=run_id,
            symbol=graph_state.symbol,
            country=graph_state.country,
            horizon=horizon,
            prediction_date=prediction_date,
            evaluation_due_date=prediction_date + timedelta(days=self.horizon_days[horizon]),
            entry_price=entry_price,
            predicted_price=predicted_price,
            predicted_return_pct=predicted_return_pct,
            recommendation=graph_state.recommendation.action,
            confidence=confidence,
            risk_level=graph_state.risk.level,
            reasoning_summary=graph_state.recommendation.reasoning,
            graph_state=graph_state.model_dump(mode="json"),
            created_at=datetime.utcnow(),
            status=PredictionStatus.OPEN,
            response_metadata=metadata,
        )

    def _infer_country(self, symbol: str) -> str:
        if symbol.endswith((".NS", ".BO")):
            return "IN"
        return "US"
