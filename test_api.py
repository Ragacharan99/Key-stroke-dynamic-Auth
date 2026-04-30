import requests
import json
import time

url = "http://127.0.0.1:5000/submit"

def generate_features():
    # simulate some reasonable keystroke dynamics
    return {
        "avg_dwell": 120.5,
        "avg_flight": 90.2,
        "typing_speed": 4.5
    }

def test_training():
    print("Sending 10 training samples...")
    for i in range(10):
        payload = {
            "mode": "train",
            "username": "test_user",
            "features": generate_features()
        }
        res = requests.post(url, json=payload)
        print(f"Sample {i+1}: {res.json()}")

def test_auth(is_impostor=False):
    print("Testing Authentication...")
    features = generate_features()
    if is_impostor:
        features["avg_dwell"] = 300.0  # Make it distinctly different

    payload = {
        "mode": "auth",
        "username": "test_user",
        "features": features
    }
    res = requests.post(url, json=payload)
    print(f"Auth Result: {res.json()}")

if __name__ == "__main__":
    test_training()
    time.sleep(1)
    test_auth(is_impostor=False)
    test_auth(is_impostor=True)
