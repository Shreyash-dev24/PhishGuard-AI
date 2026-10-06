from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.prediction_history import PredictionHistory
from backend.app.schemas.history import PredictionHistoryResponse
import json


router = APIRouter(
    prefix="/api",
    tags=["History"],
)


@router.get(
    "/history",
    response_model=list[PredictionHistoryResponse],
)
def get_prediction_history(
    db: Session = Depends(get_db),
):
    records = (
        db.query(PredictionHistory)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )

    return [
        PredictionHistoryResponse(
            id=record.id,
            url=record.url,
            classification=record.classification,
            final_score=record.final_score,
            ml_probability_phishing=record.ml_probability_phishing,
            dl_probability_phishing=record.dl_probability_phishing,
            raw_score=record.raw_score,
            indicator_count=record.indicator_count,
            indicator_boost=record.indicator_boost,
            triggered_indicators=json.loads(
                record.triggered_indicators
            ),
            created_at=record.created_at,
        )
        for record in records
    ]