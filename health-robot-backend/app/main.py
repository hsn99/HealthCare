import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine, Base
from app.routes import (
    patient_routes,
    doctor_route,
    questionnaire_route,
    room_route,
    login_route,
)
from .crud.auth_crud import fingerprint_loop

# Create the DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Check DB connection and print DB path
try:
    with engine.connect() as conn:
        print("✅ Connected to the database successfully.")
        print(f"📁 Database path: {engine.url.database}")
except Exception as e:
    print("❌ Failed to connect to the database:", e)


app.include_router(patient_routes.router)
app.include_router(doctor_route.router)
app.include_router(questionnaire_route.router)
app.include_router(room_route.router)
app.include_router(login_route.router)


# scanner_thread = threading.Thread(target=fingerprint_loop, daemon=True)
# scanner_thread.start()
