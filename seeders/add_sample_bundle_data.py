#!/usr/bin/env python3
"""
Add sample bundle data to the database for testing machine status functionality.
"""

import os
import sys
from datetime import datetime, timedelta
import random
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = f"postgresql://{os.getenv('TIMESCALE_USER', 'postgres')}:{os.getenv('TIMESCALE_PASSWORD', 'password')}@{os.getenv('TIMESCALE_HOST', 'localhost')}:5432/{os.getenv('TIMESCALE_DB', 'metrics')}"

print(f"Connecting to database: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def add_sample_bundles():
        """Add sample bundle data for testing"""
        db = SessionLocal()
        
        try:
            # First, let's add some sample machines if they don't exist
            machines_query = text("""
                INSERT INTO machine (label, location) VALUES 
                ('M001', 'Floor-A'),
                ('M002', 'Floor-A'),
                ('M003', 'Floor-B'),
                ('M004', 'Floor-B'),
                ('M005', 'Floor-C')
                ON CONFLICT (label) DO NOTHING;
            """)
            db.execute(machines_query)
            
            # Get current time
            now = datetime.now()
            today_start = now.replace(hour=6, minute=0, second=0, microsecond=0)  # Start at 6 AM
            
            # Sample machine IDs
            machine_ids = ['M001', 'M002', 'M003', 'M004', 'M005']
            employee_ids = ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005', 'EMP006', 'EMP007', 'EMP008']
            
            bundles_data = []
            
            # Generate bundles for today with different patterns for each machine
            for machine_id in machine_ids:
                machine_start_time = today_start
                
                if machine_id == 'M001':
                    # Active machine - consistent production
                    for i in range(25):  # 25 bundles
                        bundle_time = machine_start_time + timedelta(minutes=random.randint(8, 15))
                        bundles_data.append({
                            'time': bundle_time,
                            'id': str(uuid.uuid4()),
                            'machine_id': machine_id,
                            'employee_id': random.choice(employee_ids)
                        })
                        machine_start_time = bundle_time
                
                elif machine_id == 'M002':
                    # Slow machine - longer intervals
                    for i in range(12):  # 12 bundles
                        bundle_time = machine_start_time + timedelta(minutes=random.randint(20, 35))
                        bundles_data.append({
                            'time': bundle_time,
                            'id': str(uuid.uuid4()),
                            'machine_id': machine_id,
                            'employee_id': random.choice(employee_ids)
                        })
                        machine_start_time = bundle_time
                
                elif machine_id == 'M003':
                    # Machine that stopped recently
                    for i in range(18):  # 18 bundles
                        if i < 15:
                            # Normal production in the morning
                            bundle_time = machine_start_time + timedelta(minutes=random.randint(10, 18))
                        else:
                            # Stopped 2 hours ago
                            bundle_time = machine_start_time + timedelta(hours=2)
                        
                        bundles_data.append({
                            'time': bundle_time,
                            'id': str(uuid.uuid4()),
                            'machine_id': machine_id,
                            'employee_id': random.choice(employee_ids)
                        })
                        machine_start_time = bundle_time
                
                elif machine_id == 'M004':
                    # Single bundle machine
                    bundle_time = today_start + timedelta(hours=2)
                    bundles_data.append({
                        'time': bundle_time,
                        'id': str(uuid.uuid4()),
                        'machine_id': machine_id,
                        'employee_id': random.choice(employee_ids)
                    })
                
                # M005 - No bundles today (inactive)
            
            # Insert bundle data
            print(f"Inserting {len(bundles_data)} bundle records...")
            
            for bundle in bundles_data:
                insert_query = text("""
                    INSERT INTO bundle (time, id, machine_id, employee_id) 
                    VALUES (:time, :id, :machine_id, :employee_id)
                    ON CONFLICT (machine_id, time) DO NOTHING;
                """)
                db.execute(insert_query, bundle)
            
            # Add some bundles from yesterday for comparison
            yesterday_start = (now - timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
            
            for machine_id in machine_ids[:3]:  # Only first 3 machines had production yesterday
                machine_start_time = yesterday_start
                bundles_count = random.randint(15, 30)
                
                for i in range(bundles_count):
                    bundle_time = machine_start_time + timedelta(minutes=random.randint(8, 20))
                    insert_query = text("""
                        INSERT INTO bundle (time, id, machine_id, employee_id) 
                        VALUES (:time, :id, :machine_id, :employee_id)
                        ON CONFLICT (machine_id, time) DO NOTHING;
                    """)
                    db.execute(insert_query, {
                        'time': bundle_time,
                        'id': str(uuid.uuid4()),
                        'machine_id': machine_id,
                        'employee_id': random.choice(employee_ids)
                    })
                    machine_start_time = bundle_time
            
            db.commit()
            print("✅ Sample bundle data added successfully!")
            
            # Show summary
            summary_query = text("""
                SELECT 
                    machine_id,
                    COUNT(*) as bundle_count,
                    MIN(time) as first_bundle,
                    MAX(time) as last_bundle
                FROM bundle 
                WHERE DATE(time) = CURRENT_DATE
                GROUP BY machine_id
                ORDER BY machine_id;
            """)
            
            result = db.execute(summary_query)
            print("\n📊 Today's Bundle Summary:")
            print("Machine ID | Bundles | First Bundle | Last Bundle")
            print("-" * 60)
            
            for row in result:
                print(f"{row.machine_id:>9} | {row.bundle_count:>7} | {row.first_bundle.strftime('%H:%M:%S')} | {row.last_bundle.strftime('%H:%M:%S')}")
            
            # Show overall summary
            total_query = text("SELECT COUNT(*) as total FROM bundle WHERE DATE(time) = CURRENT_DATE")
            total_result = db.execute(total_query).scalar()
            print(f"\n📈 Total bundles today: {total_result}")
            
        except Exception as e:
            print(f"❌ Error adding sample data: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()
    
    if __name__ == "__main__":
        print("🔄 Adding sample bundle data...")
        add_sample_bundles()
        print("✅ Done!")

except Exception as e:
    print(f"❌ Database connection failed: {str(e)}")
    sys.exit(1)
