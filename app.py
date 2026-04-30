from flask import Flask, render_template, request, jsonify
import csv
import os
from model import authenticate_user, train_model, FEATURE_ORDER, get_data_path

app = Flask(__name__)

"""
API Routing for the Keystroke Authentication System
Processes incoming raw feature data, manages the user dataset, and routes to ML models.
"""

@app.route("/")
def home():
    """Serve the primary application interface."""
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    """Handle incoming typing samples for either Training or Authentication."""
    data = request.get_json()
    mode = data.get("mode")
    username = data.get("username")
    features = data.get("features")

    if not username:
        return jsonify({"status": "error", "message": "Username is required."}), 400

    if not features:
        return jsonify({"status": "error", "message": "Keystroke features are missing."}), 400

    # Natural Rhythm Server-Side Validation: Ensure extreme outliers aren't dumped into training
    # For example, if someone holds down a key for 5 seconds or types 500 WPM, reject.
    if features.get('avg_dwell', 0) > 2000 or features.get('typing_speed', 0) > 15:
        return jsonify({"status": "error", "message": "Unnatural rhythm detected. Rejected."}), 400

    if mode == "train":
        data_path = get_data_path(username)
        
        # Purge legacy data with mismatched features
        if os.path.exists(data_path):
            wipe = False
            with open(data_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                try:
                    first_row = next(reader, None)
                    if first_row and len(first_row) != len(FEATURE_ORDER):
                        wipe = True
                except Exception:
                    wipe = True
            if wipe:
                os.remove(data_path)

        # Prepare the CSV row
        try:
            row = [features.get(f, 0.0) for f in FEATURE_ORDER]
        except (KeyError, TypeError) as e:
            return jsonify({"status": "error", "message": f"Malformed features: {str(e)}"}), 400

        # Append to user data
        with open(data_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        # Calculate sample count
        sample_count = 0
        if os.path.exists(data_path):
            with open(data_path, "r") as f:
                sample_count = sum(1 for _ in f)

        # Only train after the 10th sample
        if sample_count >= 10:
            train_result = train_model(username)
            return jsonify({
                "status": "success", 
                "message": f"Sample #{sample_count} saved. Enrollment Complete! {train_result.get('message', '')}",
                "sample_count": sample_count
            })
        else:
            return jsonify({
                "status": "success", 
                "message": f"Training sample #{sample_count} saved. {10 - sample_count} more needed.",
                "sample_count": sample_count
            })

    elif mode == "auth":
        result = authenticate_user(username, features)
        if result["status"] == "error":
            return jsonify(result), 401 # Unauthorized
        return jsonify(result), 200
        
    return jsonify({"status": "error", "message": "Invalid specific mode."}), 400

if __name__ == "__main__":
    app.run(debug=True)
