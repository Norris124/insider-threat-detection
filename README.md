# Honey File Security System

## Overview
The **Honey File Security System** is an AI-driven cybersecurity solution designed to detect unauthorized access and malicious activities on sensitive files. It utilizes honey files as bait to lure attackers, monitors file interactions, and triggers real-time alerts via Telegram.

## Features
- **Honey Files Creation**: Generates decoy files to attract attackers.
- **File Access Monitoring**: Tracks read, write, and deletion activities.
- **Database Logging**: Stores access logs in MongoDB for further analysis.
- **Real-Time Alerts**: Sends instant notifications via Telegram when unauthorized access is detected.
- **Automated Log Analysis**: Leverages Google Gemini API for intelligent anomaly detection and predictive threat analysis.

## Tech Stack
- **Python**: Core scripting language.
- **MongoDB**: NoSQL database for scalable log storage.
- **Flask**: Web interface for log visualization.
- **Google Gemini API**: AI-powered analysis and anomaly detection.
- **Telegram API**: Sends real-time alerts to administrators.

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- MongoDB

### Clone the Repository
```sh
git clone https://github.com/your-username/honeyfile-security.git
cd honeyfile-security
```

### Create Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file and add your API keys and database connection string:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
MONGO_URI=your_mongodb_connection_string
GEMINI_API_KEY=your_google_gemini_api_key
```

### Run the Application
```sh
python app.py
```

## Usage
- The system generates honey files in a designated directory.
- Monitors access events and logs activities to MongoDB.
- Sends Telegram alerts when an unauthorized user interacts with a honey file.
- Uses Google Gemini API for AI-driven threat analysis and anomaly detection.
- Admins can review logs via the Flask web interface.

## File Structure
```
├── app.py                  # Main application file
├── file_monitor.py         # Monitors file interactions
├── create_honey_files.py   # Generates honey files
├── check_logs.py           # Retrieves logs from MongoDB
├── db_handler.py           # Handles database operations
├── telegram_alerts.py      # Sends alerts via Telegram API
├── gemini_analysis.py      # AI-powered anomaly detection using Google Gemini API
├── templates/              # HTML templates for Flask web app
├── .env                    # Environment variables (ignored in Git)
├── requirements.txt        # List of dependencies
```

## Future Enhancements
- Advanced AI-powered threat detection using Google Gemini API.
- Cloud-based log storage with MongoDB Atlas.
- Enhanced dashboard with real-time threat visualization.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.



