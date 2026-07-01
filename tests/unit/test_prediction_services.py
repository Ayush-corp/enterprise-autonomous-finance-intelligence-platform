from datetime import date, datetime, timedelta

from domain.prediction import PredictionHorizon, PredictionRecord, PredictionStatus
from repositories.accuracy_repository import AccuracyRepository
from repositories.prediction_repository import PredictionRepository
from services.accuracy_service import AccuracyService
from services.data_freshness_service import DataFreshnessService
from services.prediction_evaluator import PredictionEvaluator
from services.prediction_scheduler import PredictionScheduler
from services.prediction_service import PredictionService
from services.watchlist_service import WatchlistService


def test_watchlist_add_list_remove(tmp_path):
    service = WatchlistService(db_path=tmp_path / "investoros.sqlite3")

    item = service.add_symbol("RELIANCE.NS")
    active = service.list_active_symbols()
    service.remove_symbol("RELIANCE.NS")

    assert item.country == "IN"
    assert len(active) == 1
    assert service.list_active_symbols() == []


def test_data_freshness_ttl_logic(tmp_path):
    service = DataFreshnessService(db_path=tmp_path / "investoros.sqlite3")

    assert not service.is_fresh("RELIANCE.NS", "IN", "news")
    service.mark_refreshed("RELIANCE.NS", "IN", "news", "test", ttl_minutes=240)

    assert service.is_fresh("RELIANCE.NS", "IN", "news")


def test_generate_daily_predictions_for_multiple_horizons(tmp_path):
    db_path = tmp_path / "investoros.sqlite3"
    watchlist = WatchlistService(db_path=db_path)
    symbol = watchlist.add_symbol("RELIANCE.NS", "IN")
    service = PredictionService(db_path=db_path)

    records = service.generate_daily_predictions(
        [symbol],
        [PredictionHorizon.ONE_DAY, PredictionHorizon.SEVEN_DAYS],
    )

    assert len(records) == 2
    assert {record.horizon for record in records} == {
        PredictionHorizon.ONE_DAY,
        PredictionHorizon.SEVEN_DAYS,
    }


def test_evaluate_due_prediction_and_accuracy_summary(tmp_path):
    db_path = tmp_path / "investoros.sqlite3"
    repo = PredictionRepository(db_path)
    prediction = PredictionRecord(
        id="prediction-due",
        run_id=None,
        symbol="RELIANCE.NS",
        country="IN",
        horizon=PredictionHorizon.ONE_DAY,
        prediction_date=date.today() - timedelta(days=2),
        evaluation_due_date=date.today() - timedelta(days=1),
        entry_price=2500.0,
        predicted_price=2550.0,
        predicted_return_pct=2.0,
        recommendation="BUY",
        confidence=0.7,
        risk_level="medium",
        reasoning_summary="Due prediction",
        graph_state={"metadata": {"benchmark_entry_price": 2500.0}},
        created_at=datetime.utcnow() - timedelta(days=2),
        status=PredictionStatus.OPEN,
    )
    repo.save_prediction(prediction)

    outcome = PredictionEvaluator(db_path=db_path).evaluate_prediction("prediction-due")
    summary = AccuracyService(db_path=db_path).get_accuracy_summary(days=90)

    assert outcome.prediction_id == "prediction-due"
    assert summary.evaluated_predictions == 1
    assert "1D" in summary.by_horizon


def test_scheduler_job_methods_without_background_scheduler(tmp_path):
    db_path = tmp_path / "investoros.sqlite3"
    watchlist = WatchlistService(db_path=db_path)
    watchlist.add_symbol("RELIANCE.NS", "IN")
    scheduler = PredictionScheduler(
        prediction_service=PredictionService(db_path=db_path),
        evaluator=PredictionEvaluator(db_path=db_path),
        watchlist_service=watchlist,
    )

    run = scheduler.run_daily_prediction_job()
    outcomes = scheduler.run_evaluation_job()

    assert run.symbols_requested > 0
    assert isinstance(outcomes, list)
