from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from ml.features.extractor import FEATURE_NAMES, extract_feature_vector


# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT_DIR / "ml" / "data" / "raw" / "url_phish.csv"
MODELS_DIR = ROOT_DIR / "models"

MODELS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Original rows: {len(df)}")


# --------------------------------------------------
# Basic cleaning
# --------------------------------------------------

df = df.dropna(subset=["url", "label"])

df = df.drop_duplicates(subset=["url"])

df["label"] = pd.to_numeric(df["label"], errors="coerce")

df = df.dropna(subset=["label"])

df["label"] = df["label"].astype(int)


# --------------------------------------------------
# Validate labels
# --------------------------------------------------

valid_labels = {0, 1}

if not set(df["label"].unique()).issubset(valid_labels):
    raise ValueError("Dataset contains labels other than 0 and 1.")


print(f"Rows after cleaning: {len(df)}")

print("\nLabel distribution:")
print(df["label"].value_counts())


# --------------------------------------------------
# Feature extraction
# --------------------------------------------------

print("\nExtracting 27 features...")

feature_rows = []

for url in df["url"]:
    feature_rows.append(extract_feature_vector(url))


X = pd.DataFrame(feature_rows, columns=FEATURE_NAMES)

y = df["label"].reset_index(drop=True)


print(f"Feature matrix shape: {X.shape}")


# --------------------------------------------------
# Train / Validation / Test split
# --------------------------------------------------

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42,
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    stratify=y_temp,
    random_state=42,
)


print("\nDataset split:")
print(f"Training samples:   {len(X_train)}")
print(f"Validation samples: {len(X_val)}")
print(f"Test samples:       {len(X_test)}")


# --------------------------------------------------
# Save RAW features
# --------------------------------------------------

print("\nSaving raw features...")

X_train.to_csv(MODELS_DIR / "X_train_raw.csv", index=False)
X_val.to_csv(MODELS_DIR / "X_val_raw.csv", index=False)
X_test.to_csv(MODELS_DIR / "X_test_raw.csv", index=False)


# --------------------------------------------------
# Scaling for ANN
# --------------------------------------------------

print("\nScaling features for ANN...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_val_scaled = scaler.transform(X_val)

X_test_scaled = scaler.transform(X_test)


# --------------------------------------------------
# Save scaled features
# --------------------------------------------------

X_train_scaled_df = pd.DataFrame(
    X_train_scaled,
    columns=FEATURE_NAMES,
)

X_val_scaled_df = pd.DataFrame(
    X_val_scaled,
    columns=FEATURE_NAMES,
)

X_test_scaled_df = pd.DataFrame(
    X_test_scaled,
    columns=FEATURE_NAMES,
)


X_train_scaled_df.to_csv(
    MODELS_DIR / "X_train_scaled.csv",
    index=False,
)

X_val_scaled_df.to_csv(
    MODELS_DIR / "X_val_scaled.csv",
    index=False,
)

X_test_scaled_df.to_csv(
    MODELS_DIR / "X_test_scaled.csv",
    index=False,
)


# --------------------------------------------------
# Save labels
# --------------------------------------------------

y_train.to_csv(
    MODELS_DIR / "y_train.csv",
    index=False,
)

y_val.to_csv(
    MODELS_DIR / "y_val.csv",
    index=False,
)

y_test.to_csv(
    MODELS_DIR / "y_test.csv",
    index=False,
)


# --------------------------------------------------
# Save scaler
# --------------------------------------------------

joblib.dump(
    scaler,
    MODELS_DIR / "scaler.joblib",
)


print("\nPreprocessing completed successfully.")

print("\nSaved files:")
print("  X_train_raw.csv")
print("  X_val_raw.csv")
print("  X_test_raw.csv")
print("  X_train_scaled.csv")
print("  X_val_scaled.csv")
print("  X_test_scaled.csv")
print("  y_train.csv")
print("  y_val.csv")
print("  y_test.csv")
print("  scaler.joblib")