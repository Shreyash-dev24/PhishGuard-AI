from backend.app.services.expert_system import evaluate_expert_rules


def test_ip_and_verification_rules():
    features = {
        "has_ip_address": 1,
        "has_at_symbol": 0,
        "is_shortened_url": 0,
        "has_suspicious_encoding": 0,
        "has_port": 0,
        "has_login_word": 0,
        "has_account_word": 1,
        "has_verification_word": 1,
        "has_security_word": 0,
        "num_suspicious_keywords": 2,
        "uses_https": 0,
        "url_length": 50,
        "num_subdirectories": 1,
    }

    result = evaluate_expert_rules(features)

    assert result["indicator_count"] == 5

    assert (
        "IP address used as hostname"
        in result["triggered_indicators"]
    )

    assert (
        "Account-related keyword detected"
        in result["triggered_indicators"]
    )

    assert (
        "Verification-related keyword detected"
        in result["triggered_indicators"]
    )

    assert (
        "HTTPS is not used"
        in result["triggered_indicators"]
    )