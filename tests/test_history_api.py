from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_history_endpoint():
    response = client.get("/api/history")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        record = data[0]

        assert "id" in record
        assert "url" in record
        assert "classification" in record
        assert "final_score" in record
        assert "ml_probability_phishing" in record
        assert "dl_probability_phishing" in record
        assert "raw_score" in record
        assert "indicator_count" in record
        assert "indicator_boost" in record
        assert "triggered_indicators" in record
        assert "created_at" in record