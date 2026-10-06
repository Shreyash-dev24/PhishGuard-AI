from backend.app.services.risk_engine import calculate_risk_score


def test_risk_score_without_indicators():
    result = calculate_risk_score(
        ml_probability_phishing=0.20,
        dl_probability_phishing=0.40,
        indicator_count=0,
    )

    # raw = (0.5 * 0.20) + (0.5 * 0.40)
    # raw = 0.30
    # boost = 0
    # final = 30

    assert result["raw_score"] == 0.30
    assert result["indicator_boost"] == 0.0
    assert result["final_score"] == 30
    assert result["classification"] == "legitimate"


def test_risk_score_with_indicators():
    result = calculate_risk_score(
        ml_probability_phishing=0.70,
        dl_probability_phishing=0.80,
        indicator_count=4,
    )

    # raw = (0.5 * 0.70) + (0.5 * 0.80)
    # raw = 0.75
    #
    # boost = 0.03 * 4
    # boost = 0.12
    #
    # final = 87

    assert result["raw_score"] == 0.75
    assert result["indicator_boost"] == 0.12
    assert result["final_score"] == 87
    assert result["classification"] == "potentially_phishing"


def test_indicator_boost_is_capped():
    result = calculate_risk_score(
        ml_probability_phishing=0.90,
        dl_probability_phishing=0.90,
        indicator_count=10,
    )

    # 0.03 * 10 = 0.30
    # But maximum allowed boost = 0.15

    assert result["indicator_boost"] == 0.15
    assert result["final_score"] == 100


def test_invalid_ml_probability():
    try:
        calculate_risk_score(
            ml_probability_phishing=1.5,
            dl_probability_phishing=0.5,
            indicator_count=0,
        )
        assert False
    except ValueError:
        assert True


def test_invalid_dl_probability():
    try:
        calculate_risk_score(
            ml_probability_phishing=0.5,
            dl_probability_phishing=-0.1,
            indicator_count=0,
        )
        assert False
    except ValueError:
        assert True