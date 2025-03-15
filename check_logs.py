import pymongo
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client.honeyfile_logs

logs = list(db.threat_logs.find({}, {"_id": 0}))

if logs:
    print("📡 Live Logs from MongoDB:")
    for log in logs:
        print(log)
else:
    print("❌ No logs found! Is file_monitor.py running?")
