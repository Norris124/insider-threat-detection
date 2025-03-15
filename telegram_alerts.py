import requests
import os
from dotenv import load_dotenv
from db_handler import get_latest_logs  # Ensure function exists

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Ensure the variables are loaded
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ ERROR: Telegram Bot Token or Chat ID is missing!")
    exit(1)

def send_alert():
    """Send the latest 5 alerts to Telegram & Debug Errors"""
    logs = get_latest_logs()  # Get the last 5 alerts from MongoDB

    if not logs:
        print("⚠ No recent threats to notify.")
        return

    message = "🚨 *Security Alert: Latest Risks Detected!*\n\n"
    for log in logs:
        message += f"📁 *File:* {log['filename']}\n"
        message += f"⚠ *Event:* {log['event']}\n"
        message += f"🔍 *AI Assessment:* {log['ai_assessment']}\n"
        message += f"🕒 *Time:* {log['timestamp']}\n\n"

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            print("✅ Telegram Alert Sent Successfully!")
        else:
            print(f"❌ Telegram Alert Failed! Response: {response.text}")
    except Exception as e:
        print(f"❌ Telegram API Error: {e}")

# 🔹 Test Sending Alert
if __name__ == "__main__":
    send_alert()
