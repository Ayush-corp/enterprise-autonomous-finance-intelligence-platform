from datetime import date, datetime, timedelta

from domain.prediction import PredictionHorizon, PredictionRecord, PredictionStatus
from repositories.db import initialize_database
from repositories.prediction_repository import PredictionRepository


def test_db_table_creation(tmp_path):
    db_path = tmp_path / "investoros.sqlite3"

    initialize_database(db_path)

    assert db_path.exists()


def test_save_and_retrieve_latest_prediction(tmp_path):
    repo = PredictionRepository(tmp_path / "investoros.sqlite3")
    prediction = PredictionRecord(
        id="prediction-1",
        run_id=None,
        symbol="RELIANCE.NS",
        country="IN",
        horizon=PredictionHorizon.ONE_DAY,
        prediction_date=date.today(),
        evaluation_due_date=date.today() + timedelta(days=1),
        entry_price=100.0,
        predicted_price=105.0,
        predicted_return_pct=5.0,
        recommendation="BUY",
        confidence=0.7,
        risk_level="medium",
        reasoning_summary="Test prediction",
        graph_state={"metadata": {"benchmark_entry_price": 100.0}},
        created_at=datetime.utcnow(),
        status=PredictionStatus.OPEN,
    )

    repo.save_prediction(prediction)

    latest = repo.latest_predictions("RELIANCE.NS")
    assert len(latest) == 1
    assert latest[0].id == "prediction-1"
    assert latest[0].response_metadata["disclaimer"]
