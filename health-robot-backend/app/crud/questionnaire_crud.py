from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.questionnaire import Questionnaire
from app.schemas.questionnaire_schema import QuestionnaireCreate
import json
from ..models import Doctor, Room


def analyse_questions(db: Session, questions_data: QuestionnaireCreate):
    data = questions_data.model_dump()
    answers = data.get("answers", [])

    condition = ""
    if "yes" in answers[:2]:
        condition = "emergency"
    elif "BP" in answers[2] or "Pulse" in answers[2]:
        condition = "cardiology"
    elif "Temperature" in answers[4]:
        condition = "infection"
    else:
        condition = "general"

    # Fetch matching doctor
    doctor = db.query(Doctor).filter(Doctor.specialization == condition).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="No doctor found for condition")

    room = db.query(Room).filter(Room.id == doctor.room_id).first()

    return {
        "answers": answers,
        "assigned_doctor": doctor.name,
        "assigned_room": room.room_number if room else None,
        "waiting_time": room.waiting_time if room else None,
    }
