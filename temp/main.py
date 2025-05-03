from fastapi import FastAPI
from app import database, models, gemini_client
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root path
@app.get("/")
def root():
    return {"message": "Healthcare robot is running!"}

# Route to get all patients
@app.get("/patients/")
async def get_patients():
    patients = database.get_all_patients()
    result = []
    for p in patients:
        result.append({
            "id": p[0],
            "patient_id": p[1],
            "temperature": p[2],
            "weight": p[3],
            "blood_pressure": p[4],
            "pulse": p[5],
            "created_at": p[6],
        })
    return result

# Route to submit patient readings
@app.post("/submit-readings/")
def submit_readings(reading: models.PatientReadings):
    database.save_patient(reading)
    return {"message": "Patient readings saved successfully"}

# Route to get latest weight from weight sensor
@app.get("/weight/")
async def read_latest_weight():
    weight = database.get_latest_weight()
    return {"latest_weight": weight}

# Diagnose patient (send to Gemini)
@app.post("/diagnose/")
async def diagnose(data: models.PatientReadings):
    response = gemini_client.send_to_gemini(data)
    return response
