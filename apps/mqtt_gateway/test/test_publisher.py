import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# MQTT broker details
MQTT_BROKER = "localhost"       # Change to your broker address if needed
MQTT_PORT = 1883
MQTT_TOPIC = "bundle"

# Create MQTT client
client = mqtt.Client()

def get_iso_timestamp():
    # Return timestamp in 'YYYY-MM-DD HH:MM:SS.ffffff' format
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def publish_bundle(increment):
    payload = {
        "time": get_iso_timestamp(),
        "id": f"TB{increment}",
        "machineId": "TEST001",
        "employeeId": "EMP001"
    }
    result = client.publish(MQTT_TOPIC, json.dumps(payload))
    if result[0] == 0:
        print(f"Published: {payload}")
    else:
        print("Failed to publish message")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

client.on_connect = on_connect

if __name__ == "__main__":
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    try:
        increment = 10000000
        while True:
            publish_bundle(increment)
            increment += 1
            time.sleep(30)
    except KeyboardInterrupt:
        print("Exiting publisher.")
        client.loop_stop()
        client.disconnect()