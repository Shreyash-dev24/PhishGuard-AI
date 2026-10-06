from typing import Any


def evaluate_expert_rules(features: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate rule-based phishing indicators.

    This expert system does not make a machine-learning prediction.
    It only checks explicit URL indicators extracted by the shared
    feature extractor.
    """

    triggered_indicators = []

    # --------------------------------------------------
    # Rule 1: IP address used instead of a domain
    # --------------------------------------------------

    if features.get("has_ip_address", 0) == 1:
        triggered_indicators.append(
            "IP address used as hostname"
        )

    # --------------------------------------------------
    # Rule 2: @ symbol in URL
    # --------------------------------------------------

    if features.get("has_at_symbol", 0) == 1:
        triggered_indicators.append(
            "@ symbol detected in URL"
        )

    # --------------------------------------------------
    # Rule 3: URL shortening service
    # --------------------------------------------------

    if features.get("is_shortened_url", 0) == 1:
        triggered_indicators.append(
            "URL shortening service detected"
        )

    # --------------------------------------------------
    # Rule 4: Suspicious percent encoding
    # --------------------------------------------------

    if features.get("has_suspicious_encoding", 0) == 1:
        triggered_indicators.append(
            "Suspicious URL encoding detected"
        )

    # --------------------------------------------------
    # Rule 5: Explicit port number
    # --------------------------------------------------

    if features.get("has_port", 0) == 1:
        triggered_indicators.append(
            "Explicit port number detected"
        )

    # --------------------------------------------------
    # Rule 6: Login keyword
    # --------------------------------------------------

    if features.get("has_login_word", 0) == 1:
        triggered_indicators.append(
            "Login-related keyword detected"
        )

    # --------------------------------------------------
    # Rule 7: Account keyword
    # --------------------------------------------------

    if features.get("has_account_word", 0) == 1:
        triggered_indicators.append(
            "Account-related keyword detected"
        )

    # --------------------------------------------------
    # Rule 8: Verification keyword
    # --------------------------------------------------

    if features.get("has_verification_word", 0) == 1:
        triggered_indicators.append(
            "Verification-related keyword detected"
        )

    # --------------------------------------------------
    # Rule 9: Security keyword
    # --------------------------------------------------

    if features.get("has_security_word", 0) == 1:
        triggered_indicators.append(
            "Security-related keyword detected"
        )

    # --------------------------------------------------
    # Rule 10: Multiple suspicious keywords
    # --------------------------------------------------

    suspicious_keyword_count = features.get(
        "num_suspicious_keywords",
        0,
    )

    if suspicious_keyword_count >= 2:
        triggered_indicators.append(
            "Multiple suspicious keywords detected"
        )

    # --------------------------------------------------
    # Rule 11: No HTTPS
    # --------------------------------------------------

    if features.get("uses_https", 0) == 0:
        triggered_indicators.append(
            "HTTPS is not used"
        )

    # --------------------------------------------------
    # Rule 12: Very long URL
    # --------------------------------------------------

    url_length = features.get(
        "url_length",
        0,
    )

    if url_length >= 100:
        triggered_indicators.append(
            "Unusually long URL detected"
        )

    # --------------------------------------------------
    # Rule 13: High number of subdirectories
    # --------------------------------------------------

    subdirectories = features.get(
        "num_subdirectories",
        0,
    )

    if subdirectories >= 4:
        triggered_indicators.append(
            "Deep URL path structure detected"
        )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    indicator_count = len(
        triggered_indicators
    )

    return {
        "triggered_indicators": triggered_indicators,
        "indicator_count": indicator_count,
    }