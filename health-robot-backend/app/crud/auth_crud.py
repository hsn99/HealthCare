# routes/fingerprint_auth.py

import time
import serial
import adafruit_fingerprint

uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

is_logged_in = False
stop_scanning = False


def get_fingerprint():
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False

    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False

    return True


def fingerprint_loop(callback):
    global is_logged_in, stop_scanning
    while True:
        if stop_scanning or is_logged_in:
            time.sleep(1)
            continue

        if get_fingerprint():
            fingerprint_id = finger.finger_id
            callback(fingerprint_id)
