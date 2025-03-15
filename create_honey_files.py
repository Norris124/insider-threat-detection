import os

# Define the honey files directory
HONEY_FILES_DIR = "/Users/norrisr/Downloads/honeyfiles"

# Ensure the directory exists
if not os.path.exists(HONEY_FILES_DIR):
    os.makedirs(HONEY_FILES_DIR)

# Define fake sensitive files
honey_files = {
    "passwords.txt": "This is a confidential file. Do not modify.",
    "secrets.doc": "Top secret: Do not open this file!",
    "bank_info.csv": "Bank account details: (fake data here)",
    "config.ini": "[SECURITY]\nAPI_KEY=1234567890ABCDEF",
    "emails.txt": "Email credentials: username: admin@example.com, password: 1234",
}

# Create the honey files
for filename, content in honey_files.items():
    file_path = os.path.join(HONEY_FILES_DIR, filename)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"📝 Created honey file: {file_path}")

print("✅ Honey files have been successfully created!")
