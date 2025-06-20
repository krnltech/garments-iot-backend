#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>

// WiFi credentials
const char* ssid = "wsn";
const char* password = "StrongP@ss";

// MQTT broker
const char* mqtt_server = "134.209.109.140";
const int mqtt_port = 1883;

// Define your machine ID here
#define MACHINE_ID "M020"

// MQTT and WiFi setup
WiFiClient espClient;
PubSubClient client(espClient);

// LED pins
#define RED_LED D3
#define YELLOW_LED D1
#define GREEN_LED D2

// Buzzer pin
#define BUZZER D0

// RFID pins
#define SS_PIN  D8
#define RST_PIN D4

MFRC522 rfid(SS_PIN, RST_PIN);

// NTP and time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 0, 60000); // UTC, 60s update

#define CURRENT_READ_INTERVAL 500
#define CURRENT_READINGS_PER_MIN (60000 / CURRENT_READ_INTERVAL)
short currentReadings[CURRENT_READINGS_PER_MIN];
short currentIndex = 0;
unsigned long lastCurrentRead = 0;
unsigned long lastCurrentPublish = 0;

String loggedInEmployeeId = "";

void buzzerBeep(short buzzerDuration = 300) {
  digitalWrite(BUZZER, HIGH);
  delay(buzzerDuration);
  digitalWrite(BUZZER, LOW);
}

void setup() {
  Serial.begin(9600);
  initLEDs();
  initBuzzer();
  digitalWrite(RED_LED, HIGH);
  digitalWrite(YELLOW_LED, HIGH);

  setup_wifi();
  digitalWrite(RED_LED, LOW);
  buzzerBeep();
  client.setServer(mqtt_server, mqtt_port);

  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Tap an RFID/NFC tag on the reader");

  timeClient.begin();
  timeClient.update();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  timeClient.update();

  // --- Current Sense Logic ---
  unsigned long now = millis();
  if (now - lastCurrentRead >= CURRENT_READ_INTERVAL) {
    lastCurrentRead = now;
    if (currentIndex < CURRENT_READINGS_PER_MIN) {
      short current_sensor_value = analogRead(A0);
      currentReadings[currentIndex++] = current_sensor_value;
      Serial.println(current_sensor_value);
    }
  }

  if (now - lastCurrentPublish >= 60000) { // 1 minute
    lastCurrentPublish = now;
    String timestamp = getTimestamp();
    publishCurrentArray(timestamp.c_str(), MACHINE_ID, loggedInEmployeeId.c_str());
    currentIndex = 0; // reset for next minute
  }
  // --- End Current Sense Logic ---

  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    flashGreenLED();
    buzzerBeep(200);
    String cardID = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
      if (rfid.uid.uidByte[i] < 0x10) cardID += "0";
      cardID += String(rfid.uid.uidByte[i], HEX);
    }
    cardID.toUpperCase();

    Serial.print("Card ID (Hex): ");
    Serial.println(cardID);

    // Store employee ID if it starts with 'E'
    if (cardID.startsWith("E")) {
      loggedInEmployeeId = cardID;
      Serial.println("Logged in employee: " + loggedInEmployeeId);
    }
    else{
      String timestamp = getTimestamp();

      publishBundle(timestamp.c_str(), cardID.c_str(), MACHINE_ID, MACHINE_ID);
    }

    

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.printf("Connecting to %s\n", ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
}

void reconnect() {
  while (!client.connected()) {
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(RED_LED, HIGH);

    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);
  buzzerBeep(600);
}

void publishBundle(const char* timestamp, const char* id, const char* machineId, const char* employeeId) {
  StaticJsonDocument<256> doc;
  doc["time"] = timestamp;
  doc["id"] = id;
  doc["machineId"] = machineId;
  doc["employeeId"] = employeeId;

  char buffer[256];
  serializeJson(doc, buffer);
  client.publish("bundle", buffer);
  Serial.println("Published to bundle: " + String(buffer));
}

void publishCurrentArray(const char* timestamp, const char* machineId, const char* employeeId) {
  StaticJsonDocument<2048> doc; // Sufficient for 120 readings

  doc["timestamp"] = timestamp;
  doc["machineId"] = machineId;
  doc["employeeId"] = employeeId;

  JsonArray arr = doc.createNestedArray("current");
  for (int i = 0; i < currentIndex; i++) {
    arr.add(currentReadings[i]);
  }

  char buffer[2048];
  size_t n = serializeJson(doc, buffer, sizeof(buffer));
  client.publish("CurrentSense", buffer, n);
  Serial.println("Published to CurrentSense: " + String(buffer));
}

void initLEDs() {
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  for (int i = 0; i < 3; i++) {
    digitalWrite(RED_LED, HIGH);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(GREEN_LED, HIGH);
    delay(100);
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(GREEN_LED, LOW);
    delay(100);
  }
}

void initBuzzer() {
  pinMode(BUZZER, OUTPUT);

  for (int i = 0; i < 3; i++) {
    digitalWrite(BUZZER, HIGH);
    delay(100);
    digitalWrite(BUZZER, LOW);
    delay(100);
  }
}

// Helper to zero-pad integers
String twoDigits(int number) {
  if (number < 10) return "0" + String(number);
  return String(number);
}

String getTimestamp() {
  time_t rawTime = timeClient.getEpochTime();
  struct tm * timeinfo = gmtime(&rawTime);

  // Estimate microseconds from micros()
  unsigned long micro = micros() % 1000000;

  char timestamp[32];
  snprintf(timestamp, sizeof(timestamp), "%04d-%02d-%02d %02d:%02d:%02d.%06lu",
           timeinfo->tm_year + 1900,
           timeinfo->tm_mon + 1,
           timeinfo->tm_mday,
           timeinfo->tm_hour,
           timeinfo->tm_min,
           timeinfo->tm_sec,
           micro);

  return String(timestamp);
}

void flashGreenLED() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(GREEN_LED, HIGH);
    delay(80);
    digitalWrite(GREEN_LED, LOW);
    delay(80);
  }
}
