#include <WiFi.h>
#include <PubSubClient.h>
#include <HX711_ADC.h>
#include <EEPROM.h>

// WiFi & MQTT setup
const char* ssid = "Sara";
const char* password = "12345678";
const char* mqtt_server = "192.168.100.145";

WiFiClient espClient;
PubSubClient client(espClient);

// HX711_ADC pins
const int HX711_dout = 16; // DT
const int HX711_sck = 17;  // SCK
HX711_ADC LoadCell(HX711_dout, HX711_sck);

// EEPROM settings
const int calVal_eepromAdress = 0;
float calibrationValue;

// Button for tare and calibration
const int buttonPin = 4;
#define ledPin 2

bool requestWeight = false;
unsigned long lastPressTime = 0;

void blink_led(int times, int duration) {
  for (int i = 0; i < times; i++) {
    digitalWrite(ledPin, HIGH);
    delay(duration);
    digitalWrite(ledPin, LOW);
    delay(200);
  }
}

void setup_wifi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    blink_led(1, 200);
    if (++attempts > 10) {
      ESP.restart();
    }
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)message[i];

  Serial.print("Received [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(msg);

  if (String(topic) == "rpi/broadcast" && msg == "weight") {
    requestWeight = true;
  }
}

void connect_mqtt() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32_weight_client")) {
      Serial.println("connected");
      client.subscribe("rpi/broadcast");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 3 sec");
      blink_led(2, 200);
      delay(3000);
    }
  }
}

void calibrate() {
  Serial.println("*** Calibration Mode ***");
  Serial.println("Remove any object from scale, press 't' to tare.");

  bool tared = false;
  while (!tared) {
    LoadCell.update();
    if (Serial.available()) {
      if (Serial.read() == 't') {
        LoadCell.tareNoDelay();
        while (!LoadCell.getTareStatus()) LoadCell.update();
        Serial.println("Tare complete.");
        tared = true;
      }
    }
  }

  Serial.println("Now place a known weight and enter its value in grams (e.g., 230.0):");

  float known_mass = 0;
  while (known_mass == 0) {
    LoadCell.update();
    if (Serial.available()) {
      known_mass = Serial.parseFloat();
      if (known_mass > 0) {
        LoadCell.refreshDataSet();
        float newCal = LoadCell.getNewCalibration(known_mass);
        Serial.print("New calibration value: ");
        Serial.println(newCal);

        EEPROM.begin(512);
        EEPROM.put(calVal_eepromAdress, newCal);
        EEPROM.commit();
        EEPROM.end();

        LoadCell.setCalFactor(newCal);
        calibrationValue = newCal;
        Serial.println("Calibration saved.");
      }
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  LoadCell.begin();
  LoadCell.start(2000);
  LoadCell.setCalFactor(1.0); // temporary

  EEPROM.begin(512);
  EEPROM.get(calVal_eepromAdress, calibrationValue);
  if (calibrationValue == 0 || isnan(calibrationValue)) {
    Serial.println("No calibration found. Starting calibration.");
    calibrate();
  } else {
    Serial.print("Using saved calibration: ");
    Serial.println(calibrationValue);
    LoadCell.setCalFactor(calibrationValue);
  }
  EEPROM.end();
}

void loop() {
  if (!client.connected()) connect_mqtt();
  client.loop();
  LoadCell.update();

  // Tare & calibration button
  if (digitalRead(buttonPin) == LOW && millis() - lastPressTime > 2000) {
    lastPressTime = millis();
    Serial.println("Button pressed: Starting calibration...");
    calibrate();
    blink_led(3, 150);
  }

if (requestWeight) {
  float weight = LoadCell.getData();
  Serial.print("Measured weight: ");
  Serial.println(weight);

  char payload[32];
  snprintf(payload, sizeof(payload), "%.2f", weight);  // Ensures the weight is a string with 2 decimal places

  if (client.publish("esp32/sensor1", payload)) {
    Serial.println("Weight sent to MQTT.");
  } else {
    Serial.println("MQTT publish failed.");
  }

  blink_led(2, 150);
  requestWeight = false;
}

}

