from backend.app.services.model_service import (
    get_model_service,
)


def test_model_service_prediction():
    service = get_model_service()

    result = service.predict(
        "https://www.google.com/"
    )

    assert "features" in result

    assert (
        len(result["features"]) == 27
    )

    assert (
        0.0
        <= result["ml_probability_phishing"]
        <= 1.0
    )

    assert (
        0.0
        <= result["dl_probability_phishing"]
        <= 1.0
    )