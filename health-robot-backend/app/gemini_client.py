import requests
from app.models import PatientReadings

# Example Gemini API endpoint (you can change it later)
GEMINI_API_URL = "https://api.example.com/diagnose"

def send_to_gemini(data: PatientReadings):
    # Prepare the payload
    payload = {
        "patient_id": data.patient_id,
        "temperature": data.temperature,
        "weight": data.weight,
        "blood_pressure": data.blood_pressure,
        "pulse": data.pulse
    }
    
    try:
        # Simulate sending to Gemini API
        # response = requests.post(GEMINI_API_URL, json=payload)
        # return response.json()

        # 🚨 Temporary Fake Response (since real Gemini not connected yet)
        return {
            "diagnosis": "Normal",
            "department": "General Medicine",
            "estimated_wait_time": "15 minutes",
            "room": "Room 5"
        }
        
    except Exception as e:
        return {"error": str(e)}
