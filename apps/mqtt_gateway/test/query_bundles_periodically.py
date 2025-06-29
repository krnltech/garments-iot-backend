import psycopg2
import time
import json
from datetime import datetime

# Database connection parameters
DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "iot_database"
DB_USER = "iot_admin"
DB_PASS = "IoTdb_2024!"

LOG_FILE = "/root/garments-iot-backend/apps/mqtt_gateway/test/bundles_query_log.txt"

def query_bundles(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM bundles")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def log_results(results):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"--- Query at {timestamp} ---\n")
        for row in results:
            f.write(json.dumps(row, default=json_serial) + "\n")
        f.write("\n")


def main():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            results = query_bundles(conn)
            log_results(results)
            conn.close()
        except Exception as e:
            with open(LOG_FILE, "a") as f:
                f.write(f"Error at {datetime.now().isoformat()}: {e}\n")
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    main()