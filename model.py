import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os

"""
Machine Learning Core for Keystroke Dynamics Authentication
Contains feature definitions, caching mechanisms, and the IsolationForest pipeline.
"""

FEATURE_ORDER = [
    "avg_dwell", "std_dwell", "median_dwell", 
    "avg_flight", "std_flight", "median_flight", 
    "typing_speed", "error_rate",
    "L_th", "L_he", "L_qu", "L_ic", "L_ck", "L_br", "L_ro", "L_ow", "L_wn", 
    "L_fo", "L_ox", "L_ju", "L_um", "L_mp", "L_ps", "L_ov", "L_ve", "L_er", 
    "L_la", "L_az", "L_zy", "L_do", "L_og"
]

# In-memory cache for models
models_cache = {}

def get_data_path(username):
    """Return the absolute path to the user's training data file."""
    os.makedirs('data', exist_ok=True)
    return f"data/{username}_training_data.csv"

def get_model_path(username):
    """Return the absolute path to the user's serialized ML model."""
    os.makedirs('models', exist_ok=True)
    return f"models/{username}_model.pkl"

def get_model(username):
    """Load the model from the cache or disk."""
    if username in models_cache:
        return models_cache[username]
    
    model_path = get_model_path(username)
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        models_cache[username] = model
        return model
    return None

def train_model(username):
    """
    Train an IsolationForest model on the user's dataset.
    Requires at least 10 samples to produce a standard normal rhythm profile.
    """
    data_path = get_data_path(username)
    if not os.path.exists(data_path):
        return {"status": "error", "message": "Training data file not found"}

    try:
        data = pd.read_csv(data_path, header=None, names=FEATURE_ORDER, on_bad_lines='skip')
    except Exception as e:
        return {"status": "error", "message": f"Failed to parse training data: {str(e)}"}

    # Safety checks
    if data.empty or len(data) < 10:
        return {"status": "error", "message": f"Not enough data to train. Need at least 10 samples, got {len(data)}."}

    # Extract our ordered features
    X = data[FEATURE_ORDER].values

    # ML Pipeline:
    # 1. StandardScaler: Normalizes features to (mean=0, std=1) so ms timing vs speed scale appropriately.
    # 2. IsolationForest: Identifies anomalies. Contamination is set low expecting tight typing rhythms.
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('iforest', IsolationForest(
            n_estimators=200,
            contamination=0.10,
            random_state=42
        ))
    ])

    try:
        pipeline.fit(X)
    except Exception as e:
        # If there's an internal numpy error due to bad shapes/strings, wipe corrupt data
        try:
            os.remove(data_path)
        except OSError:
            pass
        return {"status": "error", "message": f"Dataset corrupted. Purged old data. Please re-enroll. Error snippet: {str(e)}"}

    # Save model to disk and cache
    model_path = get_model_path(username)
    joblib.dump(pipeline, model_path)
    models_cache[username] = pipeline

    return {"status": "success", "message": "Model trained successfully."}

def authenticate_user(username, features):
    """
    Authenticates a typing sample against the user's trained IsolationForest.
    Calculates a Match Probability (%) using the decision_function.
    """
    model = get_model(username)
    if model is None:
        return {"status": "error", "message": "Model not trained yet for this user. Please complete enrollment."}

    try:
        # Reshape for single prediction
        x = np.array([features.get(f, 0.0) for f in FEATURE_ORDER]).reshape(1, -1)
    except KeyError:
        return {"status": "error", "message": "Invalid feature set sent from client."}

    prediction = model.predict(x)
    score = model.decision_function(x)[0]
    
    # The decision_function returns positive values for normal (inliers) and negative for anomalies (outliers).
    # Typical range is [-0.3, 0.3]. We normalize this to a [0, 100] percentage probability.
    prob = 50 + (score * 250) 
    prob = max(0.0, min(100.0, prob))
    match_probability = round(prob, 2)

    # -1 implies an anomaly
    if prediction[0] == -1 or match_probability < 50.0:
        return {
            "status": "error", 
            "message": "IMPOSTOR DETECTED. Rhythm did not match.",
            "probability": match_probability
        }
        
    return {
        "status": "success", 
        "message": "AUTHENTIC USER. Access Granted.",
        "probability": match_probability
    }
