import paho.mqtt.client as mqtt
from app.database import save_weight
import json

MQTT_BROKER = "localhost"
MQTT_TOPIC = "WightSensor"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        weight = payload.get("weight")
        if weight:
            save_weight(weight)
    except Exception as e:
        print(f"MQTT Error: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
