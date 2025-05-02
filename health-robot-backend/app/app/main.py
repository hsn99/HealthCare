from fastapi import FastAPI
from app import mqtt_listener, database, models, gemini_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    database.init_db()
    mqtt_listener.start_mqtt()

@app.post("/submit-readings/")
async def submit_readings(data: models.PatientReadings):
    database.save_reading(data)
    return {"status": "received"}

@app.post("/diagnose/")
async def diagnose(data: models.PatientReadings):
    response = gemini_client.send_to_gemini(data)
    return response
