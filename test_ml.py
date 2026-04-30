import requests
import json
import time

url = "http://127.0.0.1:5000/submit"

def generate_features(impostor=False):
    if not impostor:
        return {
            "avg_dwell": 120.5, "std_dwell": 5.2, "median_dwell": 120.0,
            "avg_flight": 90.2, "std_flight": 8.1, "median_flight": 89.5,
            "typing_speed": 4.5, "error_rate": 0.05
        }
    else:
        # A completely different typing style (faster, erratic, high errors)
        return {
            "avg_dwell": 80.0, "std_dwell": 25.5, "median_dwell": 75.0,
            "avg_flight": 60.2, "std_flight": 30.1, "median_flight": 55.5,
            "typing_speed": 7.5, "error_rate": 0.25
        }

def test_training():
    print("Sending 10 training samples (User 'admin')...")
    for i in range(10):
        # Add slight variations to simulate natural typing
        f = generate_features(impostor=False)
        f["avg_dwell"] += (i - 5) * 1.5
        f["std_dwell"] += (i % 3) * 0.5
        
        payload = {
            "mode": "train",
            "username": "admin",
            "features": f
        }
        res = requests.post(url, json=payload)
        print(f"Train {i+1}: {res.json()}")

def test_auth():
    print("\n--- Testing Authentication ---")
    
    # Test True Identity
    payload_true = {
        "mode": "auth",
        "username": "admin",
        "features": generate_features(impostor=False)
    }
    res = requests.post(url, json=payload_true)
    print(f"Auth (True Identity): {res.json()}")

    # Test Impostor Identity
    payload_fake = {
        "mode": "auth",
        "username": "admin",
        "features": generate_features(impostor=True)
    }
    res = requests.post(url, json=payload_fake)
    print(f"Auth (Impostor): {res.json()}")

if __name__ == "__main__":
    time.sleep(2) # Wait for server
    test_training()
    test_auth()
