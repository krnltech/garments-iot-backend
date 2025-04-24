import paho.mqtt.client as mqtt
import psycopg2
import os
import json

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("employee")
    client.subscribe("bundle")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}")
    print(f"Message payload decode: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        
        # Connect to TimescaleDB
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=5433,
            dbname=os.getenv("TIMESCALE_DB"),
            user=os.getenv("TIMESCALE_USER"),
            password=os.getenv("TIMESCALE_PASSWORD")
        )
        print("Connected to TimescaleDB")
        cursor = conn.cursor()
        
        # Insert data into employees table
        if msg.topic == "employee":
            cursor.execute("""
                INSERT INTO employees (time, id, machine_id, name)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (data["time"], data["id"], data["machineId"], data["name"]))
            
            # Print the inserted data
            cursor.execute("""
                SELECT * FROM employees WHERE id = %s
            """, (data["id"],))
            result = cursor.fetchone()
            print(f"Inserted employee data: {result}")
            
        # Insert data into bundles table
        elif msg.topic == "bundle":
            cursor.execute("""
                INSERT INTO bundles (time, id, machine_id, employee_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (data["time"], data["id"], data["machineId"], data["employeeId"]))
            
            # Print the inserted data
            cursor.execute("""
                SELECT * FROM bundles WHERE id = %s
            """, (data["id"],))
            result = cursor.fetchone()
            print(f"Inserted bundle data: {result}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error processing message: {str(e)}")

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(os.getenv("MQTT_BROKER"), 1883, 60)

# Start the MQTT loop
client.loop_forever()
