from flask import Flask, render_template, request, jsonify
import csv
from model import authenticate_user

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    mode = data["mode"]
    features = data["features"]

    FEATURE_ORDER = ["avg_dwell", "avg_flight", "typing_speed"]

    if mode == "train":
        with open("data/training_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([features[f] for f in FEATURE_ORDER])

        from model import train_model
        train_model()

        return jsonify({"message": "Training sample saved."})

    else:
        result = authenticate_user(features)
        return jsonify({"message": result})


if __name__ == "__main__":
    app.run(debug=True)
