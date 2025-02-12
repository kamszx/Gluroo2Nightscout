import os
import requests
import time

# Load environment variables
GLUROO_API_URL = os.getenv("GLUROO_API_URL")
NIGHTSCOUT_URL = os.getenv("NIGHTSCOUT_URL")
GLUROO_TOKEN = os.getenv("GLUROO_TOKEN")

def fetch_glucose_data():
    """Fetch glucose data from Gluroo API."""
    try:
        response = requests.get(GLUROO_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data from Gluroo: {e}")
        return None

def send_to_nightscout(data):
    """Send data to Nightscout."""
    if not data:
        print("⚠️ No data to send.")
        return False

    headers = {"Authorization": f"Token {GLUROO_TOKEN}", "Content-Type": "application/json"}

    try:
        response = requests.post(NIGHTSCOUT_URL, json=data, headers=headers)
        if response.status_code == 200:
            print("✅ Data successfully sent to Nightscout.")
            return True
        else:
            print(f"❌ Failed to send data. Status code: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending data to Nightscout: {e}")
        return False

def main():
    """Main loop to fetch and send glucose data every minute."""
    while True:
        print("📡 Fetching data from Gluroo...")
        data = fetch_glucose_data()
        
        if data:
            print("📤 Sending data to Nightscout...")
            send_to_nightscout(data)

        print("⏳ Waiting 1 minute before next update...\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
