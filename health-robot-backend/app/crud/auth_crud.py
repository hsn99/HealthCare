# routes/fingerprint_auth.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
import time
import serial
import adafruit_fingerprint
from app.schemas.patient_schema import PatientCreate, PatientOut
from app.models.patient import Patient


# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

is_logged_in = False
stop_scanning = False


def get_fingerprint() -> int | None:
    """Scan for a fingerprint and return True if matched."""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return None

    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return None

    return finger.finger_id


def fingerprint_loop():

    global is_logged_in, stop_scanning
    while True:
        if stop_scanning or is_logged_in:
            time.sleep(1)
            continue

        if get_fingerprint():
            fingerprint_id = finger.finger_id
            # callback(fingerprint_id)


def get_next_free_id():
    for i in range(1, 128):  # Assuming 127 is max
        if finger.load_model(i) != adafruit_fingerprint.OK:
            return i
    return None


def enroll_finger(location: int) -> bool:
    for fingerimg in range(1, 3):
        print(
            (
                "Place finger on sensor..."
                if fingerimg == 1
                else "Place same finger again..."
            ),
            end="",
        )
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
                time.sleep(0.5)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            print("Templating error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while finger.get_image() != adafruit_fingerprint.NOFINGER:
                pass

    print("Creating model...", end="")
    if finger.create_model() != adafruit_fingerprint.OK:
        print("Model creation failed")
        return False

    print("Storing model #%d..." % location, end="")
    if finger.store_model(location) != adafruit_fingerprint.OK:
        print("Storage failed")
        return False

    print("Stored successfully")
    return True


def enroll_new_user(db: Session):
    location = get_next_free_id()

    success = enroll_finger(location)
    if not success:
        raise HTTPException(status_code=500, detail="Fingerprint enrollment failed")

    return {
        "message": f"Fingerprint enrolled and saved",
        "fingerprint_id": location,
    }
