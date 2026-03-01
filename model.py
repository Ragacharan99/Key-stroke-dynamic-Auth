import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = "typing_model.pkl"
DATA_PATH = "data/training_data.csv"

FEATURE_ORDER = ["avg_dwell", "avg_flight", "typing_speed"]


def train_model():
    # Check if training data exists
    if not os.path.exists(DATA_PATH):
        return "Training data file not found"

    data = pd.read_csv(DATA_PATH)

    # Safety checks
    if data.empty or len(data) < 10:
        return "Not enough data to train (need at least 10 samples)"

    # Ensure correct feature order
    X = data[FEATURE_ORDER].values

    # Isolation Forest model
    model = IsolationForest(
        n_estimators=200,
        contamination=0.15,   # stricter than default
        random_state=42
    )

    model.fit(X)

    # Save model
    joblib.dump(model, MODEL_PATH)

    return "Model trained successfully"


def authenticate_user(features):
    if not os.path.exists(MODEL_PATH):
        return "Model not trained yet"

    # Load model
    model = joblib.load(MODEL_PATH)

    try:
        x = np.array([features[f] for f in FEATURE_ORDER]).reshape(1, -1)
    except KeyError:
        return "Invalid feature set"

    prediction = model.predict(x)
    # IsolationForest returns:
    #  1  → normal
    # -1  → anomaly

    return "AUTHENTIC USER" if prediction[0] == 1 else "IMPOSTOR"
