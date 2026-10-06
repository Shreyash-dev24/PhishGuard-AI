from typing import Any


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """
    Keep a value inside the specified range.
    """

    return max(minimum, min(value, maximum))


def calculate_risk_score(
    ml_probability_phishing: float,
    dl_probability_phishing: float,
    indicator_count: int,
) -> dict[str, Any]:
    """
    Calculate the final PhishGuard AI risk score.

    Formula:

        raw =
            0.5 * ML probability
          + 0.5 * DL probability

        indicator_boost =
            min(0.15, 0.03 * indicator_count)

        final_score =
            round(
                100 * clamp(
                    raw + indicator_boost,
                    0,
                    1
                )
            )
    """

    # --------------------------------------------------
    # Validate inputs
    # --------------------------------------------------

    if not 0.0 <= ml_probability_phishing <= 1.0:
        raise ValueError(
            "ML probability must be between 0 and 1."
        )

    if not 0.0 <= dl_probability_phishing <= 1.0:
        raise ValueError(
            "DL probability must be between 0 and 1."
        )

    if indicator_count < 0:
        raise ValueError(
            "Indicator count cannot be negative."
        )

    # --------------------------------------------------
    # ML + DL combined probability
    # --------------------------------------------------

    raw = (
        0.5 * ml_probability_phishing
        + 0.5 * dl_probability_phishing
    )

    # --------------------------------------------------
    # Expert-system indicator boost
    # --------------------------------------------------

    indicator_boost = min(
        0.15,
        0.03 * indicator_count,
    )

    # --------------------------------------------------
    # Final score
    # --------------------------------------------------

    combined_score = raw + indicator_boost

    final_score = round(
        100 * clamp(combined_score)
    )

    # --------------------------------------------------
    # Final classification
    # --------------------------------------------------

    if final_score >= 50:
        classification = "potentially_phishing"
    else:
        classification = "legitimate"

    return {
        "ml_probability_phishing": round(
            ml_probability_phishing,
            6,
        ),
        "dl_probability_phishing": round(
            dl_probability_phishing,
            6,
        ),
        "raw_score": round(
            raw,
            6,
        ),
        "indicator_count": indicator_count,
        "indicator_boost": round(
            indicator_boost,
            6,
        ),
        "final_score": final_score,
        "classification": classification,
    }