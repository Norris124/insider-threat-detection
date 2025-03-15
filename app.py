from flask import Flask, render_template, jsonify
from db_handler import get_latest_logs, get_risk_summary, get_all_logs  # ✅ Use `db_handler` instead of `database`

app = Flask(__name__)

@app.route("/")
def home():
    """Render Home Page (Dashboard)"""
    return render_template("dashboard.html")

@app.route("/logs")
def logs():
    """Retrieve latest 5 logs for real-time display"""
    return jsonify(get_latest_logs() or [])

@app.route("/all-logs")
def all_logs():
    """Retrieve all logs for the control panel"""
    return jsonify(get_all_logs() or [])

@app.route("/risk-summary")
def risk_summary():
    """Retrieve risk data for the circle chart"""
    return jsonify(get_risk_summary() or {"low": 0, "medium": 0, "high": 0})

if __name__ == "__main__":
    print("🚀 Flask Dashboard Running...")
    app.run(debug=True, threaded=True)
