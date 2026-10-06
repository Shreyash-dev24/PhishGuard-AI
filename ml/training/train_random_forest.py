from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

MODELS_DIR = ROOT_DIR / "models"

MODELS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load RAW feature data
# --------------------------------------------------

print("Loading raw feature data...")

X_train = pd.read_csv(
    MODELS_DIR / "X_train_raw.csv"
)

X_val = pd.read_csv(
    MODELS_DIR / "X_val_raw.csv"
)

X_test = pd.read_csv(
    MODELS_DIR / "X_test_raw.csv"
)


# --------------------------------------------------
# Load labels
# --------------------------------------------------

y_train = pd.read_csv(
    MODELS_DIR / "y_train.csv"
).values.ravel()

y_val = pd.read_csv(
    MODELS_DIR / "y_val.csv"
).values.ravel()

y_test = pd.read_csv(
    MODELS_DIR / "y_test.csv"
).values.ravel()


# --------------------------------------------------
# Verify feature dimensions
# --------------------------------------------------

print(f"Training features:   {X_train.shape}")
print(f"Validation features: {X_val.shape}")
print(f"Test features:       {X_test.shape}")

if X_train.shape[1] != 27:
    raise ValueError(
        f"Expected 27 features, found {X_train.shape[1]}"
    )


# --------------------------------------------------
# Create Random Forest
# --------------------------------------------------

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced",
)


# --------------------------------------------------
# Train
# --------------------------------------------------

print("Training Random Forest...")

model.fit(
    X_train,
    y_train,
)

print("Training completed.")


# --------------------------------------------------
# Evaluation function
# --------------------------------------------------

def evaluate_model(
    model,
    X,
    y,
    dataset_name,
):
    """
    Evaluate the Random Forest model on a dataset.
    """

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)[:, 1]

    accuracy = accuracy_score(
        y,
        predictions,
    )

    precision = precision_score(
        y,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y,
        probabilities,
    )

    confusion = confusion_matrix(
        y,
        predictions,
    )

    print("\n" + "=" * 60)
    print(f"{dataset_name} RESULTS")
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
            y,
            predictions,
            target_names=[
                "legitimate",
                "potentially_phishing",
            ],
            zero_division=0,
        )
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "confusion_matrix": confusion.tolist(),
    }


# --------------------------------------------------
# Validation evaluation
# --------------------------------------------------

validation_results = evaluate_model(
    model,
    X_val,
    y_val,
    "VALIDATION",
)


# --------------------------------------------------
# Test evaluation
# --------------------------------------------------

test_results = evaluate_model(
    model,
    X_test,
    y_test,
    "TEST",
)


# --------------------------------------------------
# Feature importance
# --------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

feature_importance = pd.DataFrame(
    {
        "feature": X_train.columns,
        "importance": model.feature_importances_,
    }
).sort_values(
    by="importance",
    ascending=False,
)


print(feature_importance.to_string(index=False))


# --------------------------------------------------
# Save feature importance
# --------------------------------------------------

feature_importance.to_csv(
    MODELS_DIR / "random_forest_feature_importance.csv",
    index=False,
)


# --------------------------------------------------
# Save model
# --------------------------------------------------

MODEL_PATH = MODELS_DIR / "random_forest.joblib"

joblib.dump(
    model,
    MODEL_PATH,
)


# --------------------------------------------------
# Final summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("RANDOM FOREST TRAINING COMPLETE")
print("=" * 60)

print(f"\nModel saved to:")
print(MODEL_PATH)

print("\nTest Metrics:")
print(
    f"Accuracy : {test_results['accuracy']:.4f}"
)

print(
    f"Precision: {test_results['precision']:.4f}"
)

print(
    f"Recall   : {test_results['recall']:.4f}"
)

print(
    f"F1 Score : {test_results['f1']:.4f}"
)

print(
    f"ROC-AUC  : {test_results['roc_auc']:.4f}"
)