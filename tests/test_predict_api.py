from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.predict import router


# --------------------------------------------------
# Test application
# --------------------------------------------------

app = FastAPI()

app.include_router(router)

client = TestClient(app)


# --------------------------------------------------
# API test
# --------------------------------------------------

def test_predict_endpoint():
    response = client.post(
        "/api/predict",
        json={
            "url": "https://www.google.com/"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["url"] == "https://www.google.com/"

    assert data["classification"] in [
        "legitimate",
        "potentially_phishing",
    ]

    assert 0 <= data["final_score"] <= 100

    assert 0.0 <= data[
        "ml_probability_phishing"
    ] <= 1.0

    assert 0.0 <= data[
        "dl_probability_phishing"
    ] <= 1.0

    assert data["indicator_count"] >= 0

    assert isinstance(
        data["triggered_indicators"],
        list,
    )