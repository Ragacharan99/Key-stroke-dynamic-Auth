import urllib.request
import json
import time

url = "http://127.0.0.1:5000/submit"

def generate_features():
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
            "username": "admin",
            "features": generate_features()
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            print(f"Sample {i+1}: {res}")

def test_auth(is_impostor=False):
    print(f"Testing Auth (Impostor={is_impostor})...")
    features = generate_features()
    if is_impostor:
        features["avg_dwell"] = 300.0  # Make it distinctly different

    payload = {
        "mode": "auth",
        "username": "admin",
        "features": features
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        print(f"Auth Result: {res}")

if __name__ == "__main__":
    test_training()
    time.sleep(1)
    test_auth(is_impostor=False)
    test_auth(is_impostor=True)
