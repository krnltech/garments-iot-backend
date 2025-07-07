# Seeders

This folder contains database seeding scripts for the Garments IoT Backend system.

## Seeder Files

### 🌱 Database Initialization
- **[seed_database.py](seed_database.py)** - Initialize database with base data (machines, workers, users)
- **[add_sample_data.py](add_sample_data.py)** - Add sample machines, workers, and targets
- **[add_sample_bundle_data.py](add_sample_bundle_data.py)** - Add sample bundle production data for testing status monitoring

## Usage

### Initial Database Setup
Run seeders in this order for a fresh database:

```bash
# 1. Initialize database with base structure and sample data
python seeders/seed_database.py

# 2. Add additional sample data
python seeders/add_sample_data.py

# 3. Add bundle production data for status monitoring
python seeders/add_sample_bundle_data.py
```

### Individual Seeders

#### Seed Database
```bash
python seeders/seed_database.py
```
- Creates sample machines and workers
- Sets up initial user accounts
- Establishes basic data relationships

#### Add Sample Data
```bash
python seeders/add_sample_data.py
```
- Adds more machines and workers
- Creates machine and worker targets
- Provides diverse sample data for testing

#### Add Bundle Data
```bash
python seeders/add_sample_bundle_data.py
```
- Creates realistic bundle production records
- Generates time-series data for today
- Enables testing of status monitoring features

## What Gets Seeded

### Machines
- Sample production machines with labels and locations
- Example: MACHINE001, MACHINE002, etc.
- Various floor locations (Floor A, Floor B, etc.)

### Workers
- Sample factory workers with names and designations
- Various roles: Operator, Supervisor, Quality Controller
- Diverse workforce for testing

### Users
- Admin user account
- Regular user accounts
- Proper authentication setup

### Targets
- Machine performance targets
- Worker productivity targets
- Realistic target values for testing

### Bundle Data
- Production records with timestamps
- Machine and worker associations
- Time-series data for analytics

## Database Configuration

Seeders use the same database configuration as the main application:

```python
DATABASE_URL = f"postgresql://{os.getenv('TIMESCALE_USER', 'postgres')}:{os.getenv('TIMESCALE_PASSWORD', 'password')}@{os.getenv('TIMESCALE_HOST', 'localhost')}:5432/{os.getenv('TIMESCALE_DB', 'metrics')}"
```

### Environment Variables
- `TIMESCALE_USER`: PostgreSQL username (default: postgres)
- `TIMESCALE_PASSWORD`: PostgreSQL password (default: password)
- `TIMESCALE_HOST`: PostgreSQL host (default: localhost)
- `TIMESCALE_DB`: Database name (default: metrics)

## Prerequisites

Before running seeders:

1. **Database Server Running**
   ```bash
   docker-compose up -d
   ```

2. **Database Tables Created**
   - Tables should be created by the application
   - Or run the init.sql script manually

3. **Dependencies Installed**
   ```bash
   pip install psycopg2-binary python-dotenv
   ```

## Seeder Details

### seed_database.py
- **Purpose**: Initialize database with essential data
- **Tables Affected**: machine, worker, users
- **Data Volume**: ~10 machines, ~20 workers, 2 users
- **Safe to Re-run**: Yes (uses INSERT OR IGNORE equivalent)

### add_sample_data.py
- **Purpose**: Add comprehensive sample data
- **Tables Affected**: machine, worker, machine_target, worker_target
- **Data Volume**: Additional machines, workers, and targets
- **Safe to Re-run**: May create duplicates

### add_sample_bundle_data.py
- **Purpose**: Generate realistic production data
- **Tables Affected**: bundle
- **Data Volume**: ~200 bundle records for today
- **Time Span**: Current day with realistic timing
- **Safe to Re-run**: May create duplicates

## Development

### Adding New Seeders

When creating new seeders:

1. **Follow Naming Convention**: `add_<feature>_data.py`
2. **Include Error Handling**: Proper exception handling
3. **Make Idempotent**: Safe to run multiple times
4. **Add Documentation**: Clear purpose and usage
5. **Use Environment Variables**: For database configuration

### Seeder Template
```python
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = f"postgresql://{os.getenv('TIMESCALE_USER', 'postgres')}:{os.getenv('TIMESCALE_PASSWORD', 'password')}@{os.getenv('TIMESCALE_HOST', 'localhost')}:5432/{os.getenv('TIMESCALE_DB', 'metrics')}"

def add_feature_data():
    """Add sample data for new feature"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Insert sample data
        cursor.execute("""
            INSERT INTO table_name (column1, column2) 
            VALUES (%s, %s)
        """, (value1, value2))
        
        conn.commit()
        print("✅ Feature data added successfully")
        
    except Exception as e:
        print(f"❌ Error adding feature data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_feature_data()
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   ```
   Error: could not connect to server
   ```
   - Ensure PostgreSQL is running
   - Check environment variables
   - Verify database exists

2. **Permission Errors**
   ```
   Error: permission denied for table
   ```
   - Check database user permissions
   - Ensure user has INSERT privileges

3. **Duplicate Key Errors**
   ```
   Error: duplicate key value violates unique constraint
   ```
   - Some seeders create duplicates if run multiple times
   - Clear relevant tables before re-running

### Clearing Data

To reset seeded data:

```sql
-- Clear bundle data
DELETE FROM bundle;

-- Clear targets
DELETE FROM machine_target;
DELETE FROM worker_target;

-- Clear machines and workers (if needed)
DELETE FROM machine WHERE id > 0;
DELETE FROM worker WHERE id > 0;
```

---

**Last Updated**: July 1, 2025
