import pymongo
import os
import certifi
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv



# Load environment variables
load_dotenv()

# MongoDB Connection
MONGODB_URI = os.getenv("MONGODB_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: Google Gemini API key not found. Check your .env file.")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

def analyze_activity(filename, event):
    """Use AI to analyze file activity and determine risk level"""
    prompt = f"Analyze the security risk of modifying or accessing the file '{filename}' in a cybersecurity context."

    try:
        response = genai.generate_content(prompt)
        ai_assessment = response.text.lower()

        if "high risk" in ai_assessment:
            risk_score = 3  # High Risk
        elif "medium risk" in ai_assessment:
            risk_score = 2  # Medium Risk
        else:
            risk_score = 1  # Low Risk

        return ai_assessment, risk_score

    except Exception as e:
        print(f"❌ AI Analysis Failed: {e}")
        return "AI Analysis Unavailable", 1  

# Connect to MongoDB
try:
    client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
    db = client.honeyfile_logs
    collection = db.threat_logs
    print("✅ MongoDB Connected!")

except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"❌ MongoDB Connection Error: {e}")
    exit(1)

# Function to retrieve latest 5 logs
def get_latest_logs():
    """Retrieve latest 5 logs from MongoDB"""
    try:
        logs = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(5))  # Fetch latest 5 logs
        if not logs:
            print("⚠ No logs found in the database!")
        return logs
    except Exception as e:
        print(f"❌ Error fetching logs: {e}")
        return []

# Function to retrieve all logs
def get_all_logs():
    """Retrieve all logs from MongoDB"""
    try:
        logs = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
        return logs
    except Exception as e:
        print(f"❌ Error fetching all logs: {e}")
        return []

# Function to get risk summary
def get_risk_summary():
    """Retrieve risk distribution for visualization"""
    try:
        risk_counts = {"low": 0, "medium": 0, "high": 0}
        risks = collection.find({}, {"risk_score": 1, "_id": 0})

        for entry in risks:
            if "risk_score" in entry:
                if entry["risk_score"] == 1:
                    risk_counts["low"] += 1
                elif entry["risk_score"] == 2:
                    risk_counts["medium"] += 1
                elif entry["risk_score"] == 3:
                    risk_counts["high"] += 1
            else:
                print(f"⚠ Skipping record without risk_score: {entry}")

        print(f"📊 Risk Summary: {risk_counts}")  # ✅ Debugging Output
        return risk_counts
    except Exception as e:
        print(f"❌ Error fetching risk summary: {e}")
        return {"low": 0, "medium": 0, "high": 0}

# Function to log threats into MongoDB
def log_threat(filename, event):
    """Log detected threats into MongoDB and send a Telegram alert"""
    try:
        # Assign risk score based on file type and event
        if any(keyword in filename.lower() for keyword in ["password", "bank", "credit", "finance"]):
            risk_score = 3  # High Risk
        elif any(keyword in filename.lower() for keyword in ["email", "confidential", "private"]):
            risk_score = 2  # Medium Risk
        else:
            risk_score = 1  # Low Risk

        log_entry = {
            "filename": filename,
            "event": event,
            "timestamp": datetime.utcnow(),
            "ai_assessment": "Pending AI Analysis",
            "risk_score": risk_score
        }
        collection.insert_one(log_entry)
        print(f"✅ Log inserted in MongoDB: {filename} - {event} (Risk Level: {risk_score})")

        # Send an instant Telegram alert
        alert_message = f"🚨 ALERT: {event} detected!\n📂 File: {filename}\n🛑 Risk Level: {['Low', 'Medium', 'High'][risk_score-1]}\n🕒 Time: {log_entry['timestamp']}"
        send_telegram_alert(alert_message)

    except Exception as e:
        print(f"❌ Error inserting log: {e}")
