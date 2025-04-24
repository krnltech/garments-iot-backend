import paho.mqtt.client as mqtt
import uuid
import time
import random
import threading
import json

# Configuration
MQTT_BROKER = "localhost"
NUM_MACHINES = 20

class Machine:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        
        # Updated client initialization for v2.1.0
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,  # Use VERSION2 for new API
            client_id=f"machine-{machine_id}"
        )
        
        self.client.connect(MQTT_BROKER)
        self.client.loop_start()
        
        # Start publishing threads
        threading.Thread(target=self.publish_employee, daemon=True).start()
        threading.Thread(target=self.publish_bundle, daemon=True).start()

    def publish_employee(self):
        """Publish employee data with random interval 5-10 seconds"""
        while True:
            data = {
                "id": str(uuid.uuid4()),
                "machineId": self.machine_id,
                "name": f"Employee-{random.choice(["John","Jane","Bob","Alice"])}",
                "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }
            self.client.publish("employee", json.dumps(data))
            print(f"Machine {self.machine_id} published employee: {data['id']}")
            time.sleep(random.uniform(2000, 10000))

    def publish_bundle(self):
        """Publish bundle data with random interval 30-60 seconds"""
        while True:
            data = {
                "id": str(uuid.uuid4()),
                "machineId": self.machine_id,
                "employeeId": str(uuid.uuid4()),
                "time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }
            self.client.publish("bundle", json.dumps(data))
            print(f"Machine {self.machine_id} published bundle: {data['id']}")
            time.sleep(random.uniform(1000, 3000))

if __name__ == "__main__":
    # Create 20 machine instances
    machines = [Machine(i+1) for i in range(NUM_MACHINES)]
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping simulation...")
