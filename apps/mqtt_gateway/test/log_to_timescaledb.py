import psycopg2
import json


# Database connection parameters
DB_HOST = "localhost"  # Use "localhost" if running outside Docker
DB_PORT = 5433
DB_NAME = "iot_database"
DB_USER = "iot_admin"
DB_PASS = "IoTdb_2024!"

def insert_bundle(conn, data):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO bundles (time, id, machine_id, employee_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (data["time"], data["id"], data["machineId"], data["employeeId"]))
    conn.commit()

def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    with open("/root/LOGS_REAL_DATA/log_data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            insert_bundle(conn, data)
            print(f"Inserted: {data}")
    conn.close()

if __name__ == "__main__":
    main()