from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

from tensorflow.keras.models import load_model


# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

MODELS_DIR = ROOT_DIR / "models"

RF_MODEL_PATH = MODELS_DIR / "random_forest.joblib"
ANN_MODEL_PATH = MODELS_DIR / "ann_model.keras"

X_TEST_RAW_PATH = MODELS_DIR / "X_test_raw.csv"
X_TEST_SCALED_PATH = MODELS_DIR / "X_test_scaled.csv"
Y_TEST_PATH = MODELS_DIR / "y_test.csv"

OUTPUT_PATH = MODELS_DIR / "evaluation_metrics.json"


# --------------------------------------------------
# Load test data
# --------------------------------------------------

print("Loading test datasets...")

X_test_raw = pd.read_csv(X_TEST_RAW_PATH)

X_test_scaled = pd.read_csv(X_TEST_SCALED_PATH)

y_test = pd.read_csv(Y_TEST_PATH).values.ravel()


print(f"Raw test features:    {X_test_raw.shape}")
print(f"Scaled test features: {X_test_scaled.shape}")
print(f"Test labels:          {y_test.shape}")


# --------------------------------------------------
# Verify feature dimensions
# --------------------------------------------------

if X_test_raw.shape[1] != 27:
    raise ValueError(
        f"Expected 27 raw features, found {X_test_raw.shape[1]}"
    )

if X_test_scaled.shape[1] != 27:
    raise ValueError(
        f"Expected 27 scaled features, found {X_test_scaled.shape[1]}"
    )


# --------------------------------------------------
# Evaluation helper
# --------------------------------------------------

def evaluate_model(model_name, y_true, y_pred, y_probability):
    """
    Calculate standard binary classification metrics.
    """

    accuracy = accuracy_score(
        y_true,
        y_pred,
    )

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_true,
        y_probability,
    )

    confusion = confusion_matrix(
        y_true,
        y_pred,
    )

    print("\n" + "=" * 60)
    print(f"{model_name} EVALUATION")
    print("=" * 60)

    print(f"Accuracy :  {accuracy:.4f}")
    print(f"Precision:  {precision:.4f}")
    print(f"Recall   :  {recall:.4f}")
    print(f"F1 Score :  {f1:.4f}")
    print(f"ROC-AUC  :  {roc_auc:.4f}")

    print("\nConfusion Matrix:")
    print(confusion)

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            y_pred,
            target_names=[
                "legitimate",
                "potentially_phishing",
            ],
            zero_division=0,
        )
    )

    return {
        "accuracy": round(float(accuracy), 6),
        "precision": round(float(precision), 6),
        "recall": round(float(recall), 6),
        "f1": round(float(f1), 6),
        "roc_auc": round(float(roc_auc), 6),
        "confusion_matrix": confusion.tolist(),
    }


# --------------------------------------------------
# Random Forest
# --------------------------------------------------

print("\nLoading Random Forest model...")

rf_model = joblib.load(
    RF_MODEL_PATH
)

print("Random Forest loaded successfully.")


print("\nGenerating Random Forest predictions...")

rf_predictions = rf_model.predict(
    X_test_raw
)

rf_probabilities = rf_model.predict_proba(
    X_test_raw
)[:, 1]


rf_results = evaluate_model(
    "RANDOM FOREST",
    y_test,
    rf_predictions,
    rf_probabilities,
)


# --------------------------------------------------
# ANN
# --------------------------------------------------

print("\nLoading ANN model...")

ann_model = load_model(
    ANN_MODEL_PATH
)

print("ANN loaded successfully.")


print("\nGenerating ANN predictions...")

ann_probability_array = ann_model.predict(
    X_test_scaled,
    verbose=0,
)

ann_probabilities = ann_probability_array.ravel()

ann_predictions = (
    ann_probabilities >= 0.5
).astype(int)


ann_results = evaluate_model(
    "ANN",
    y_test,
    ann_predictions,
    ann_probabilities,
)


# --------------------------------------------------
# Combined results
# --------------------------------------------------

results = {
    "dataset": {
        "test_samples": int(len(y_test)),
        "features": 27,
        "positive_class": "potentially_phishing",
        "negative_class": "legitimate",
    },
    "random_forest": rf_results,
    "ann": ann_results,
}


# --------------------------------------------------
# Save JSON report
# --------------------------------------------------

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        results,
        file,
        indent=4,
    )


# --------------------------------------------------
# Final summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("MODEL EVALUATION COMPLETE")
print("=" * 60)

print("\nResults saved to:")

print(
    OUTPUT_PATH
)

print("\nEvaluation includes:")
print("  - Accuracy")
print("  - Precision")
print("  - Recall")
print("  - F1 Score")
print("  - ROC-AUC")
print("  - Confusion Matrix")