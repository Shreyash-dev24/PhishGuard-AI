from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.database import Base


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    classification: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    final_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    ml_probability_phishing: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    dl_probability_phishing: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    raw_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    indicator_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    indicator_boost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    triggered_indicators: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )