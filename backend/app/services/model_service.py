from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from ml.features.extractor import (
    FEATURE_NAMES,
    extract_feature_vector,
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[3]

MODELS_DIR = ROOT_DIR / "models"

RF_MODEL_PATH = MODELS_DIR / "random_forest.joblib"
ANN_MODEL_PATH = MODELS_DIR / "ann_model.keras"
SCALER_PATH = MODELS_DIR / "scaler.joblib"


# --------------------------------------------------
# Model service
# --------------------------------------------------

class ModelService:
    """
    Loads the trained Random Forest, ANN, and scaler.

    Inference pipeline:

        URL
         ↓
        shared extractor
         ↓
        27 raw features
         ├──→ Random Forest
         │
         └──→ StandardScaler → ANN
    """

    def __init__(self) -> None:
        self.random_forest = None
        self.ann_model = None
        self.scaler = None

        self._load_models()

    # --------------------------------------------------
    # Load models
    # --------------------------------------------------

    def _load_models(self) -> None:
        """
        Load all trained model artifacts.
        """

        if not RF_MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Random Forest model not found: {RF_MODEL_PATH}"
            )

        if not ANN_MODEL_PATH.exists():
            raise FileNotFoundError(
                f"ANN model not found: {ANN_MODEL_PATH}"
            )

        if not SCALER_PATH.exists():
            raise FileNotFoundError(
                f"Scaler not found: {SCALER_PATH}"
            )

        # Random Forest
        self.random_forest = joblib.load(
            RF_MODEL_PATH
        )

        # Scaler
        self.scaler = joblib.load(
            SCALER_PATH
        )

        # TensorFlow is loaded here so this module can still
        # be imported in environments where TensorFlow isn't
        # needed immediately.
        from tensorflow.keras.models import load_model

        self.ann_model = load_model(
            ANN_MODEL_PATH
        )

    # --------------------------------------------------
    # Extract features
    # --------------------------------------------------

    def _extract_features(
        self,
        url: str,
    ) -> dict[str, Any]:
        """
        Extract the shared 27-feature representation.

        Returns a dictionary so the expert system can
        inspect the same features.
        """

        feature_vector = extract_feature_vector(
            url
        )

        if len(feature_vector) != len(FEATURE_NAMES):
            raise ValueError(
                "Feature extractor returned an unexpected "
                f"number of features. Expected "
                f"{len(FEATURE_NAMES)}, got "
                f"{len(feature_vector)}."
            )

        return dict(
            zip(
                FEATURE_NAMES,
                feature_vector,
            )
        )

    # --------------------------------------------------
    # Predict
    # --------------------------------------------------

    def predict(
        self,
        url: str,
    ) -> dict[str, Any]:
        """
        Generate Random Forest and ANN phishing probabilities
        for a URL.
        """

        # ----------------------------------------------
        # Extract shared features
        # ----------------------------------------------

        features = self._extract_features(
            url
        )

        # ----------------------------------------------
        # Create feature DataFrame
        # ----------------------------------------------

        raw_vector = [
            features[name]
            for name in FEATURE_NAMES
        ]

        X_raw = pd.DataFrame(
            [raw_vector],
            columns=FEATURE_NAMES,
        )

        # ----------------------------------------------
        # Random Forest
        # ----------------------------------------------

        rf_probabilities = (
            self.random_forest.predict_proba(
                X_raw
            )[0]
        )

        # Find probability corresponding to class 1
        rf_classes = self.random_forest.classes_

        phishing_class_index = np.where(
            rf_classes == 1
        )[0]

        if len(phishing_class_index) == 0:
            raise ValueError(
                "Random Forest model does not contain "
                "class 1."
            )

        ml_probability_phishing = float(
            rf_probabilities[
                phishing_class_index[0]
            ]
        )

        # ----------------------------------------------
        # Scale features for ANN
        # ----------------------------------------------

        X_scaled = self.scaler.transform(
            X_raw
        )

        # ----------------------------------------------
        # ANN
        # ----------------------------------------------

        dl_probability_phishing = float(
            self.ann_model.predict(
                X_scaled,
                verbose=0,
            )[0][0]
        )

        # ----------------------------------------------
        # Return model results
        # ----------------------------------------------

        return {
            "features": features,
            "ml_probability_phishing": round(
                ml_probability_phishing,
                6,
            ),
            "dl_probability_phishing": round(
                dl_probability_phishing,
                6,
            ),
        }


# --------------------------------------------------
# Shared service instance
# --------------------------------------------------

_model_service = None


def get_model_service() -> ModelService:
    """
    Return a shared ModelService instance.

    Models are loaded only once.
    """

    global _model_service

    if _model_service is None:
        _model_service = ModelService()

    return _model_service