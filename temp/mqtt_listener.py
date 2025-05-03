import paho.mqtt.client as mqtt
from app.database import store_weight

MQTT_BROKER = "localhost"  # Broker IP
MQTT_TOPIC = "WightSensor"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    weight = msg.payload.decode()
    print(f"Received weight: {weight}")
    store_weight(weight)

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
