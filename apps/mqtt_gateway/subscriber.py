import paho.mqtt.client as mqtt
import psycopg2
import os
import json

def ensure_bundles_table(conn):
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bundles (
            time TIMESTAMPTZ NOT NULL,
            id VARCHAR(36) NOT NULL,
            machine_id VARCHAR(36) NOT NULL,
            employee_id VARCHAR(36) NOT NULL
        );
    """)
    # Create hypertable if not already created
    cursor.execute("""
        SELECT create_hypertable('bundles', 'time', if_not_exists => TRUE);
    """)
    conn.commit()
    cursor.close()

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
            host="timescaledb",
            port=5432,
            dbname=os.getenv("TIMESCALE_DB"),
            user=os.getenv("TIMESCALE_USER"),
            password=os.getenv("TIMESCALE_PASSWORD")
        )
        print("Connected to TimescaleDB")
        cursor = conn.cursor()
        
        # Ensure bundles table exists if topic is 'bundle'
        if msg.topic == "bundle":
            ensure_bundles_table(conn)
            cursor = conn.cursor()  # Refresh cursor after DDL

        # Insert data into employees table
        if msg.topic == "employee":
            cursor.execute("""
                INSERT INTO employees (time, id, machine_id, name)
                VALUES (%s, %s, %s, %s)
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