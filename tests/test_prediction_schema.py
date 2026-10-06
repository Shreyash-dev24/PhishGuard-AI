from pydantic import ValidationError

from backend.app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)


def test_prediction_request():
    request = PredictionRequest(
        url="https://example.com"
    )

    assert request.url == "https://example.com"


def test_prediction_request_rejects_empty_url():
    try:
        PredictionRequest(url="")
        assert False
    except ValidationError:
        assert True


def test_prediction_response():
    response = PredictionResponse(
        url="https://example.com",
        classification="legitimate",
        final_score=25,
        ml_probability_phishing=0.20,
        dl_probability_phishing=0.30,
        raw_score=0.25,
        indicator_count=0,
        indicator_boost=0.0,
        triggered_indicators=[],
    )

    assert response.final_score == 25
    assert response.classification == "legitimate"


def test_prediction_response_rejects_invalid_score():
    try:
        PredictionResponse(
            url="https://example.com",
            classification="legitimate",
            final_score=120,
            ml_probability_phishing=0.20,
            dl_probability_phishing=0.30,
            raw_score=0.25,
            indicator_count=0,
            indicator_boost=0.0,
            triggered_indicators=[],
        )

        assert False

    except ValidationError:
        assert True