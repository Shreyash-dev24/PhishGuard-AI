from datetime import datetime

from pydantic import BaseModel


class PredictionHistoryResponse(BaseModel):
    id: int
    url: str
    classification: str
    final_score: int
    ml_probability_phishing: float
    dl_probability_phishing: float
    raw_score: float
    indicator_count: int
    indicator_boost: float
    triggered_indicators: list[str]
    created_at: datetime