"""
PhishGuard AI
Artificial Neural Network Training

Phase 5 - Deep Learning
"""

import os

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

RANDOM_STATE = 42

np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

MODELS_DIR = os.path.join(
    PROJECT_ROOT,
    "models"
)


# ============================================================
# DATA PATHS
# ============================================================

X_TRAIN_PATH = os.path.join(
    MODELS_DIR,
    "X_train.csv"
)

X_VAL_PATH = os.path.join(
    MODELS_DIR,
    "X_val.csv"
)

X_TEST_PATH = os.path.join(
    MODELS_DIR,
    "X_test.csv"
)

Y_TRAIN_PATH = os.path.join(
    MODELS_DIR,
    "y_train.csv"
)

Y_VAL_PATH = os.path.join(
    MODELS_DIR,
    "y_val.csv"
)

Y_TEST_PATH = os.path.join(
    MODELS_DIR,
    "y_test.csv"
)


# ============================================================
# MODEL PATH
# ============================================================

ANN_MODEL_PATH = os.path.join(
    MODELS_DIR,
    "ann_model.keras"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    print("Loading ANN datasets...")

    X_train = pd.read_csv(
        X_TRAIN_PATH
    ).values.astype("float32")

    X_val = pd.read_csv(
        X_VAL_PATH
    ).values.astype("float32")

    X_test = pd.read_csv(
        X_TEST_PATH
    ).values.astype("float32")

    y_train = pd.read_csv(
        Y_TRAIN_PATH
    )["label"].values.astype("float32")

    y_val = pd.read_csv(
        Y_VAL_PATH
    )["label"].values.astype("float32")

    y_test = pd.read_csv(
        Y_TEST_PATH
    )["label"].values.astype("float32")

    print()
    print("Training:", X_train.shape)
    print("Validation:", X_val.shape)
    print("Test:", X_test.shape)

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test
    )


# ============================================================
# BUILD ANN
# ============================================================

def build_model(input_features):

    print()
    print("=" * 60)
    print("BUILDING ARTIFICIAL NEURAL NETWORK")
    print("=" * 60)

    model = tf.keras.Sequential([

        # Input layer
        tf.keras.layers.Input(
            shape=(input_features,)
        ),

        # Hidden layer 1
        tf.keras.layers.Dense(
            64,
            activation="relu"
        ),

        # Dropout
        tf.keras.layers.Dropout(
            0.30
        ),

        # Hidden layer 2
        tf.keras.layers.Dense(
            32,
            activation="relu"
        ),

        # Dropout
        tf.keras.layers.Dropout(
            0.20
        ),

        # Output layer
        tf.keras.layers.Dense(
            1,
            activation="sigmoid"
        )
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="binary_crossentropy",
        metrics=[
            "accuracy"
        ]
    )

    model.summary()

    return model


# ============================================================
# TRAIN ANN
# ============================================================

def train_model(
    model,
    X_train,
    y_train,
    X_val,
    y_val
):

    print()
    print("=" * 60)
    print("TRAINING ANN")
    print("=" * 60)

    # Stop training when validation loss stops improving
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    # Handle class imbalance
    class_weights = {
        0: 1.0,
        1: len(y_train[y_train == 0])
        / len(y_train[y_train == 1])
    }

    print()
    print("Class weights:")
    print(class_weights)

    history = model.fit(
        X_train,
        y_train,

        validation_data=(
            X_val,
            y_val
        ),

        epochs=50,

        batch_size=256,

        class_weight=class_weights,

        callbacks=[
            early_stopping
        ],

        verbose=1
    )

    print()
    print("ANN training complete.")

    print(
        f"Epochs actually trained: "
        f"{len(history.history['loss'])}"
    )

    return model, history


# ============================================================
# EVALUATE
# ============================================================

def evaluate_model(
    model,
    X,
    y,
    dataset_name
):

    print()
    print("=" * 60)
    print(
        f"EVALUATION: {dataset_name}"
    )
    print("=" * 60)

    # ANN outputs probability
    probabilities = model.predict(
        X,
        verbose=0
    ).ravel()

    # Convert probability to class
    predictions = (
        probabilities >= 0.5
    ).astype(int)

    accuracy = accuracy_score(
        y,
        predictions
    )

    precision = precision_score(
        y,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y,
        probabilities
    )

    matrix = confusion_matrix(
        y,
        predictions
    )

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )

    print()
    print("Confusion Matrix:")

    print(matrix)

    print()
    print("Classification Report:")

    print(
        classification_report(
            y,
            predictions,
            target_names=[
                "legitimate",
                "potentially_phishing"
            ],
            zero_division=0
        )
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "confusion_matrix": matrix
    }


# ============================================================
# SAVE MODEL
# ============================================================

def save_model(model):

    model.save(
        ANN_MODEL_PATH
    )

    print()
    print("ANN model saved successfully:")

    print(
        ANN_MODEL_PATH
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PHISHGUARD AI - ANN TRAINING")
    print("=" * 60)

    # Load
    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test
    ) = load_data()

    # Build
    model = build_model(
        X_train.shape[1]
    )

    # Train
    model, history = train_model(
        model,
        X_train,
        y_train,
        X_val,
        y_val
    )

    # Validation
    evaluate_model(
        model,
        X_val,
        y_val,
        "VALIDATION SET"
    )

    # Test
    evaluate_model(
        model,
        X_test,
        y_test,
        "TEST SET"
    )

    # Save
    save_model(
        model
    )

    print()
    print("=" * 60)
    print("ANN PHASE COMPLETE")
    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()