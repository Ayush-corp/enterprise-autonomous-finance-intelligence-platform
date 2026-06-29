from fastapi.testclient import TestClient

from app.main import app


def test_analyze_endpoint_returns_structured_graph_state():
    client = TestClient(app)

    response = client.post("/api/v1/analyze", json={"symbol": "RELIANCE.NS"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "RELIANCE.NS"
    assert payload["recommendation"]["action"] in {"BUY", "HOLD", "SELL"}
    assert "request_id" in payload["metadata"]
