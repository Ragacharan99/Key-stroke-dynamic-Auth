import urllib.request
import json
import time

url = "http://127.0.0.1:5000/submit"

payload = {
    "mode": "train",
    "username": "admin",
    "features": {"avg_dwell": 120.5, "avg_flight": 90.2, "typing_speed": 4.5}
}

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        print("Response:", json.loads(response.read().decode()), flush=True)
except Exception as e:
    print("Error:", str(e), flush=True)
