import requests
import time
import os

# API Configuration
GLUROO_API = os.getenv("G2N_GLUROO_API_URL")
NIGHTSCOUT_API = os.getenv("G2N_NIGHTSCOUT_URL")
TOKEN = os.getenv("G2N_TOKEN")

print(f"G2N_GLUROO_API_URL: {G2N_GLUROO_API_URL}")
print(f"G2N_NIGHTSCOUT_URL: {G2N_NIGHTSCOUT_URL}")
print(f"G2N_TOKEN: {G2N_TOKEN}")

# Error message mapping
ERROR_MESSAGES = {
    400: "Error 400: Bad request (check data format). ❌",
    401: "Error 401: Unauthorized (check token). ❌",
    403: "Error 403: Forbidden (invalid token?). ❌",
    404: "Error 404: Resource not found (check API URL). ❌",
    500: "Error 500: Nightscout server issue. ❌"
}

def fetch_glucose_data():
    """Fetches data from Gluroo"""
    try:
        response = requests.get(GLUROO_API)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return None

def send_to_nightscout(data):
    """Sends glucose data to Nightscout"""
    try:
        response = requests.post(NIGHTSCOUT_API, json=data, headers={"api-secret": TOKEN})
        
        if response.status_code == 200:
            print(f"Sent data: {data['sgv']} mg/dL ✔️")
        else:
            error_message = ERROR_MESSAGES.get(response.status_code, f"Error {response.status_code}: {response.text}")
            print(error_message)
    
    except requests.RequestException as e:
        print(f"Connection error with Nightscout: {e}")

def main():
    while True:
        print("\n📡 Fetching data from Gluroo...")
        data = fetch_glucose_data()
        
        if data and isinstance(data, list):
            latest_entry = data[0]  # Most recent entry
            nightscout_data = {
                "sgv": latest_entry["sgv"],
                "date": latest_entry["date"],
                "dateString": latest_entry["dateString"],
                "device": "Gluroo"
            }
            print("📤 Sending data to Nightscout...")
            send_to_nightscout(nightscout_data)
        else:
            print("❌ No valid data to send.")

        print("⏳ Waiting 1 minute...")
        time.sleep(60)

if __name__ == "__main__":
    main()
