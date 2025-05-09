import time
import board
import busio
import numpy as np
import adafruit_mlx90640
import google.generativeai as genai
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from app.models.questionnaire import Questionnaire
from app.schemas.questionnaire_schema import QuestionnaireCreate
from ..models import Doctor


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
        "- Blue (Resuscitation)\n"
        "- Red (Emergency)\n"
        "- Yellow (Urgent)\n"
        "- Green (Semi-urgent)\n"
        "- White (Non-urgent)\n\n"
        "Do NOT explain. Only return the color.\n\n"
        f"id: {data['id']}\n"
        f"Age: {data['age']}\n"
        f"Temperature: {data['temperature']} Â°C\n"
        f"Weight: {data['weight']} kg\n"
        f"SpO2: {data['spo2']} %\n"
        f"Heart Rate: {data['heart_rate']} bpm\n"
        f"Blood Pressure: {data['blood_pressure']}\n\n"
        "ABCDE Triage Questions:\n"
        f"A - Difficulty breathing or swallowing: {'Yes' if data['questions']['A_airway_difficulty_breathing_swallowing'] else 'No'}\n"
        f"B - Shortness of breath: {'Yes' if data['questions']['B_shortness_of_breath'] else 'No'}\n"
        f"D - Confusion or numbness: {'Yes' if data['questions']['D_confused_or_numbness'] else 'No'}\n"
    )
    return prompt


def Geamini(message):
    convo.send_message(message)
    return convo.last.text.strip()


def analyse_questions(db: Session, data: Dict):
    answers = data.get("answers", [])

    patient_data = {
        "id": "1",
        "age": 20,
        "temperature": answers[2],  # From MLX90640
        "weight": 61.5,  # From HX711
        "spo2": 70,  # From MAX30102
        "heart_rate": 116,  # From MAX30102
        "blood_pressure": "125/90",  # From manual or sensor
        # ABCDE Questions (answers from touchscreen input)
        "questions": {
            "A_airway_difficulty_breathing_swallowing": answers[0],
            "B_shortness_of_breath": answers[1],
            "D_confused_or_numbness": answers[3],
        },
    }

    prompt = build_gemini_prompt(patient_data)
    response = Geamini(prompt)
    print(response)
    # condition = ""
    # if "yes" in answers[:2]:
    #     condition = "emergency"
    # elif len(answers) > 2 and ("BP" in answers[2] or "Pulse" in answers[2]):
    #     condition = "cardiology"
    # elif len(answers) > 4 and "Temperature" in answers[4]:
    #     condition = "infection"
    # else:
    #     condition = "general"

    # doctor = db.query(Doctor).filter(Doctor.specialization == condition).first()

    # if not doctor:
    #     raise HTTPException(status_code=404, detail="No doctor found for condition")

    # room = db.query(Room).filter(Room.id == doctor.room_id).first()

    # return {
    #     "assigned_doctor": doctor.name,
    #     "assigned_room": room.room_number if room else None,
    #     "waiting_time": room.waiting_time if room else None,
    # }

    return {"response": response, "assigned_doctor": None, "assigned_room": None}


def circulation_test():
    systolic = 120
    diastolic = 80
    status = "Normal"
    return {"res": systolic}


def get_max_thermal_temperature(duration_seconds=5):
    i2c = busio.I2C(board.SCL, board.SDA)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

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
    return {"res": thermal_data}
