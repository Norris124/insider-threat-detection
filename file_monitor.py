import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from db_handler import log_threat  # ✅ Use `db_handler.py`
import requests

# Path to Monitor
HONEYFILES_DIR = "/Users/norrisr/Downloads/honeyfiles"

# Flask Server URL (Ensures logs update in UI)
FLASK_SERVER_URL = "http://127.0.0.1:5000/logs"

class FileMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            filename = event.src_path
            log_threat(filename, "Modified")
            notify_flask_server()

    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path
            log_threat(filename, "Created")
            notify_flask_server()

def notify_flask_server():
    """Notify Flask to refresh logs"""
    try:
        requests.get(FLASK_SERVER_URL)
        print("✅ Flask Notified to Update Logs")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Could not notify Flask: {e}")

if __name__ == "__main__":
    print(f"📡 Monitoring started on: {HONEYFILES_DIR}")
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, HONEYFILES_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 Monitoring stopped.")

    observer.join()
