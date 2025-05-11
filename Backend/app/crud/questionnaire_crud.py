import time
import board
import busio
import numpy as np
import random
import adafruit_mlx90640
import google.generativeai as genai
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from app.models.questionnaire import Questionnaire
from app.models.patient import Patient
from app.schemas.questionnaire_schema import QuestionnaireCreate
from ..models import Doctor
from ..sensors import heartrate_monitor, max30102
from ..sensors.max30102 import MAX30102
from ..sensors.heartrate_monitor import HeartRateMonitor

# 1. Configure Gemini API
genai.configure(
    api_key="AIzaSyBNbDylH8OYAYAduDWzCK4YzVoeeAIGnY0"
)  # Replace with your actual API key

# 2. Define Gemini model setup
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 0,
    "max_output_tokens": 50,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

convo = model.start_chat(history=[])


def build_gemini_prompt(data):
    prompt = (
        "Based on this patient information and answers to ABCDE triage questions, respond with ONLY one color "
        "from this list:\n"
        "- Red (Emergency)\n"
        "- Yellow (Urgent)\n"
        "- Green (Semi-urgent)\n"
        "- White (Non-urgent)\n\n"
        "Do NOT explain. Only return the color.\n\n"
        f"id: {data['id']}\n"
        f"Age: {data['age']}\n"
        f"Temperature: {data['temperature']} Â°C\n"
        f"Weight: {data['weight']} kg\n"
        f"Heart Rate: {data['spo2']} bpm\n"
        f"Blood Pressure: {data['blood_pressure']}\n\n"
        "ABCDE Triage Questions:\n"
        f"A - Difficulty breathing or swallowing: {data['questions']['A_airway_difficulty_breathing_swallowing']}\n"
        f"B - Shortness of breath: {data['questions']['B_shortness_of_breath']}\n"
        f"D - Confusion or numbness: {data['questions']['D_confused_or_numbness']}\n"
    )
    return prompt


def Geamini(message):
    convo.send_message(message)
    return convo.last.text.strip()


def analyse_questions(db: Session, data: Dict):
    answers = data.get("answers", [])
    patient = db.query(Patient).filter(Patient.id == data["patient_id"]).first()
    print(answers)
    patient_data = {
        "id": patient.id,
        "age": patient.age,
        "temperature": answers[5],  # From MLX90640
        "weight": patient.weight,  # From HX711
        "spo2": answers[3],  # From MAX30102
        "blood_pressure": answers[2],  # From manual or sensor
        "questions": {
            "A_airway_difficulty_breathing_swallowing": answers[0],
            "B_shortness_of_breath": answers[1],
            "D_confused_or_numbness": answers[4],
        },
    }

    print(patient_data)

    prompt = build_gemini_prompt(patient_data)
    response = Geamini(prompt)
    print(response)

    if response == "Red":
        waiting_time = "15 minutes"
    elif response == "Yellow":
        waiting_time = "30 minutes"
    elif response == "Green":
        waiting_time = "45 minutes"
    elif response == "White":
        waiting_time = "Aound 1.5 hours"

    doctor_list = db.query(Doctor).all()
    print(doctor_list)

    if not doctor_list:
        raise HTTPException(status_code=404, detail="No doctor found for condition")

    assigned_doctor = random.choice(doctor_list)
    return {
        "assigned_doctor": assigned_doctor.name,
        "assigned_room": assigned_doctor.room_id if assigned_doctor else None,
        "waiting_time": waiting_time,
    }


def circulation_test():
    hrm = HeartRateMonitor()
    hrm.start_sensor()

    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, exiting...")

    hrm.stop_sensor()

    heart_rate = hrm.spo2
    return {"res": heart_rate}


def get_max_thermal_temperature(duration_seconds=5):
    i2c = busio.I2C(board.SCL, board.SDA)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    frame = np.zeros((24 * 32,))  # Array for 768 temperature readings
    end_time = time.time() + duration_seconds
    last_max_temp_c = None

    while time.time() < end_time:
        try:
            mlx.getFrame(frame)  # Capture frame from MLX90640
            last_max_temp_c = np.max(frame) + 1
            time.sleep(0.5)  # Adjust as needed

        except ValueError as e:
            print(f"Failed to read temperature, retrying. Error: {str(e)}")
            time.sleep(0.5)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    if last_max_temp_c is None:
        raise RuntimeError("No valid thermal readings were captured.")

    return {"max_temperature": round(last_max_temp_c, 1)}


def exposure_test():
    thermal_data = get_max_thermal_temperature()
    print(thermal_data)
    return {"res": thermal_data["max_temperature"]}
