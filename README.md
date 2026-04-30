# 🔐 Biometric Keystroke Dynamics System

A high-performance, behavioral biometric authentication system that identifies users based on their unique typing rhythms. Built with a modern **Cyber Glassmorphism** aesthetic and powered by advanced **Anomaly Detection** machine learning.

![UI Preview](file:///C:/Users/admin/.gemini/antigravity/brain/a983a6f3-0d74-43a3-9c7b-4c918ae0c725/.system_generated/click_feedback/click_feedback_1777462555329.png)

## 🚀 Key Features

### 🧠 Advanced ML Core
- **N-Graph (Digraph) Latency Analysis**: Captures specific timing between common character pairs (e.g., 'th', 'he', 'in') for high-precision matching.
- **Isolation Forest Algorithm**: Uses an anomaly detection approach to build a unique "rhythm profile" for each user.
- **Match Probability (%)**: Converts complex ML decision boundaries into a human-readable match percentage.

### 🛡️ Security & Robustness
- **Natural Rhythm Filter**: Prevents bot-based attacks and unnatural inputs by analyzing typing speed (KPS) and maximum flight-time gaps.
- **Automatic Data Migration**: Gracefully handles legacy datasets by detecting parameter mismatches and purging corrupted data structures.

### 🎨 Premium UI/UX
- **Cyber Glassmorphism**: A stunning dark-themed interface utilizing `backdrop-filter` blurs and ambient neon gradients.
- **Real-time Rhythm Visualizer**: An HTML5 Canvas that visualizes your typing rhythm as you type.
- **Progress Tracking**: An interactive SVG progress ring for the 10-sample enrollment phase.

---

## 🛠️ Technology Stack
- **Backend**: Python (Flask)
- **Machine Learning**: Scikit-Learn (Isolation Forest, StandardScaler), NumPy, Pandas
- **Frontend**: Vanilla JS (High-precision performance.now() API), CSS3 (Glassmorphism), HTML5 Canvas
- **Data Storage**: CSV (Raw features), Joblib (Serialized models)

---

## 🏁 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/Key-stroke-dynamic-Auth.git
cd Key-stroke-dynamic-Auth

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 📖 Usage
1.  **Enrollment**: Select **Training Mode**, enter a username, and type the target sentence 10 times to build your profile.
2.  **Authentication**: Select **Authentication Mode** and type the sentence. The system will calculate your match probability.

---

## 🔬 Math & Logic
The system extracts **31 distinct features** per sample:
- **Dwell Time**: Duration a key is held down (Mean, StdDev, Median).
- **Flight Time**: Interval between key releases and next key presses.
- **Digraph Latencies**: 23 specific sequential pairs extracted for rhythm precision.
- **Typing Velocity**: Calculated keys-per-second (KPS).

Developed by the Antigravity AI Engineering Team.