import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM
import joblib
import os

MODEL_PATH = "typing_model.pkl"

def train_model():
    data = pd.read_csv("data/training_data.csv")

    # safety checks
    if data.empty or len(data) < 5:
        return "Not enough data to train"

    X = data.values

    model = OneClassSVM(kernel="rbf", gamma="scale", nu=0.1)
    model.fit(X)

    joblib.dump(model, MODEL_PATH)
    return "Model trained"

def authenticate_user(features):
    if not os.path.exists(MODEL_PATH):
        return "Model not trained yet"

    model = joblib.load(MODEL_PATH)
    FEATURE_ORDER = ["avg_dwell", "avg_flight", "typing_speed"]
    x = np.array([features[f] for f in FEATURE_ORDER]).reshape(1, -1)

    prediction = model.predict(x)
    return "AUTHENTIC USER" if prediction[0] == 1 else "IMPOSTOR"
