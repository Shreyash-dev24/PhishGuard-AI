from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from backend.app.db.database import get_db
from backend.app.models.prediction_history import PredictionHistory

from backend.app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)

from backend.app.services.expert_system import (
    evaluate_expert_rules,
)

from backend.app.services.model_service import (
    get_model_service,
)

from backend.app.services.risk_engine import (
    calculate_risk_score,
)

from backend.app.utils.url_validator import (
    validate_url,
)


# --------------------------------------------------
# Router
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Prediction"],
)


# --------------------------------------------------
# Prediction Endpoint
# --------------------------------------------------

@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------
    # Validate URL
    # --------------------------------------------------

    is_valid, validation_message = validate_url(
        request.url
    )

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=validation_message,
        )

    # --------------------------------------------------
    # Model Prediction
    # --------------------------------------------------

    try:

        model_service = get_model_service()

        prediction = model_service.predict(
            request.url
        )

        # --------------------------------------------------
        # Expert System
        # --------------------------------------------------

        expert_result = evaluate_expert_rules(
            prediction["features"]
        )

        # --------------------------------------------------
        # Risk Engine
        # --------------------------------------------------

        risk_result = calculate_risk_score(
            ml_probability_phishing=prediction[
                "ml_probability_phishing"
            ],
            dl_probability_phishing=prediction[
                "dl_probability_phishing"
            ],
            indicator_count=expert_result[
                "indicator_count"
            ],
        )

        # --------------------------------------------------
        # Save Prediction History
        # --------------------------------------------------

        history_record = PredictionHistory(
            url=request.url,
            classification=risk_result[
                "classification"
            ],
            final_score=risk_result[
                "final_score"
            ],
            ml_probability_phishing=prediction[
                "ml_probability_phishing"
            ],
            dl_probability_phishing=prediction[
                "dl_probability_phishing"
            ],
            raw_score=risk_result[
                "raw_score"
            ],
            indicator_count=expert_result[
                "indicator_count"
            ],
            indicator_boost=risk_result[
                "indicator_boost"
            ],
            triggered_indicators=json.dumps(
                expert_result[
                    "triggered_indicators"
                ]
            ),
        )

        db.add(history_record)
        db.commit()
        db.refresh(history_record)

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return PredictionResponse(
            url=request.url,
            classification=risk_result[
                "classification"
            ],
            final_score=risk_result[
                "final_score"
            ],
            ml_probability_phishing=prediction[
                "ml_probability_phishing"
            ],
            dl_probability_phishing=prediction[
                "dl_probability_phishing"
            ],
            raw_score=risk_result[
                "raw_score"
            ],
            indicator_count=expert_result[
                "indicator_count"
            ],
            indicator_boost=risk_result[
                "indicator_boost"
            ],
            triggered_indicators=expert_result[
                "triggered_indicators"
            ],
        )

    # --------------------------------------------------
    # Error Handling
    # --------------------------------------------------

    except ValueError as exc:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except FileNotFoundError:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Required model files are missing.",
        )

    except HTTPException:

        db.rollback()

        raise

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Prediction service failed.",
        )