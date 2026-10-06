from pydantic import BaseModel, Field


# --------------------------------------------------
# Prediction Request
# --------------------------------------------------

class PredictionRequest(BaseModel):
    """
    Data sent by the frontend to the prediction API.
    """

    url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="URL to analyze for phishing indicators.",
    )


# --------------------------------------------------
# Prediction Response
# --------------------------------------------------

class PredictionResponse(BaseModel):
    """
    Final response returned by the prediction API.
    """

    url: str

    classification: str

    final_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    ml_probability_phishing: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    dl_probability_phishing: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    raw_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    indicator_count: int = Field(
        ...,
        ge=0,
    )

    indicator_boost: float = Field(
        ...,
        ge=0.0,
        le=0.15,
    )

    triggered_indicators: list[str]