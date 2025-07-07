# Database Backup and Restore Guide

This document provides comprehensive instructions for backing up and restoring the TimescaleDB database in the Garments IoT Backend project.

## Overview

The database uses Docker volumes for persistence, ensuring data survives container restarts and system reboots. However, regular backups are essential for data safety and disaster recovery.

## Current Database Configuration

- **Database Engine**: TimescaleDB (PostgreSQL-based)
- **Container Name**: `timescaledb`
- **Volume Name**: `garments-iot-backend_timescaledbdata`
- **Database Name**: `yourdatabase`
- **Username**: `youruser`
- **Data Location**: `/var/lib/postgresql/data` (inside container)

## Backup Methods

### 1. SQL Dump Backup (Recommended for Regular Backups)

#### Create a Backup
```bash
# Navigate to the backend directory
cd /home/rkz/krnltech/garments-iot-backend

# Create a timestamped backup
docker exec timescaledb pg_dump -U youruser yourdatabase > backup_$(date +%Y%m%d_%H%M%S).sql

# Create a compressed backup (saves space)
docker exec timescaledb pg_dump -U youruser yourdatabase | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### Restore from SQL Backup
```bash
# Restore from uncompressed backup
docker exec -i timescaledb psql -U youruser yourdatabase < backup_file.sql

# Restore from compressed backup
gunzip -c backup_file.sql.gz | docker exec -i timescaledb psql -U youruser yourdatabase
```

### 2. Volume Backup (Complete Data Directory Backup)

#### Create Volume Backup
```bash
# Create a complete backup of the database volume
docker run --rm \
  -v garments-iot-backend_timescaledbdata:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/db_volume_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

#### Restore from Volume Backup
```bash
# Stop the database service first
docker compose stop timescaledb

# Remove the existing volume (WARNING: This deletes all current data!)
docker volume rm garments-iot-backend_timescaledbdata

# Recreate the volume
docker volume create garments-iot-backend_timescaledbdata

# Restore the data
docker run --rm \
  -v garments-iot-backend_timescaledbdata:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/db_volume_backup_YYYYMMDD_HHMMSS.tar.gz -C /data

# Restart the database service
docker compose up timescaledb -d
```

## Automated Backup Scripts

### Daily Backup Script

Create a script for automated daily backups:

```bash
#!/bin/bash
# File: daily_backup.sh

BACKUP_DIR="/path/to/your/backups"
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Navigate to project directory
cd /home/rkz/krnltech/garments-iot-backend

# Create SQL dump backup
BACKUP_FILE="$BACKUP_DIR/garments_db_$(date +%Y%m%d_%H%M%S).sql.gz"
docker exec timescaledb pg_dump -U youruser yourdatabase | gzip > "$BACKUP_FILE"

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup created successfully: $BACKUP_FILE"
    
    # Clean up old backups (older than retention period)
    find "$BACKUP_DIR" -name "garments_db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "Old backups cleaned up (kept last $RETENTION_DAYS days)"
else
    echo "Backup failed!"
    exit 1
fi
```

Make the script executable:
```bash
chmod +x daily_backup.sh
```

### Cron Job Setup

Add to crontab for daily backups at 2 AM:
```bash
# Edit crontab
crontab -e

# Add this line for daily backup at 2 AM
0 2 * * * /path/to/your/daily_backup.sh >> /var/log/garments_backup.log 2>&1
```

## Backup Verification

### Verify SQL Backup
```bash
# Check if backup file is not empty
ls -lh backup_file.sql

# Test restore in a temporary database
docker exec timescaledb createdb -U youruser test_restore
docker exec -i timescaledb psql -U youruser test_restore < backup_file.sql
docker exec timescaledb dropdb -U youruser test_restore
```

### Verify Volume Backup
```bash
# Check backup file size
ls -lh db_volume_backup_*.tar.gz

# List contents of backup
docker run --rm -v $(pwd):/backup alpine tar tzf /backup/db_volume_backup_file.tar.gz
```

## Disaster Recovery Procedures

### Complete Database Recovery

1. **Stop all services**:
   ```bash
   docker compose down
   ```

2. **Remove corrupted volume**:
   ```bash
   docker volume rm garments-iot-backend_timescaledbdata
   ```

3. **Recreate and restore**:
   ```bash
   # From volume backup
   docker volume create garments-iot-backend_timescaledbdata
   docker run --rm -v garments-iot-backend_timescaledbdata:/data -v $(pwd):/backup alpine tar xzf /backup/latest_backup.tar.gz -C /data
   
   # OR from SQL backup
   docker compose up timescaledb -d
   # Wait for database to be ready, then:
   docker exec -i timescaledb psql -U youruser yourdatabase < latest_backup.sql
   ```

4. **Restart all services**:
   ```bash
   docker compose up -d
   ```

## Best Practices

### Backup Frequency
- **SQL Dumps**: Daily or after significant data changes
- **Volume Backups**: Weekly or before major system changes
- **Before Updates**: Always backup before updating containers or code

### Storage Recommendations
- Store backups on a different physical device/location
- Use cloud storage for off-site backups
- Test restore procedures regularly
- Keep multiple backup versions (implement rotation)

### Monitoring
- Monitor backup script execution
- Check backup file sizes for anomalies
- Verify backup integrity periodically
- Set up alerts for backup failures

## Troubleshooting

### Common Issues

1. **Permission Denied**:
   ```bash
   # Ensure proper permissions
   sudo chown -R $USER:$USER /path/to/backup/directory
   ```

2. **Database Connection Issues**:
   ```bash
   # Check if database is running
   docker compose ps timescaledb
   
   # Check database logs
   docker compose logs timescaledb
   ```

3. **Insufficient Disk Space**:
   ```bash
   # Check available space
   df -h
   
   # Clean up old backups
   find /backup/path -name "*.sql.gz" -mtime +30 -delete
   ```

### Recovery Testing

Regularly test your backup and recovery procedures:

1. Create a test environment
2. Restore from backup
3. Verify data integrity
4. Document any issues found

## Important Notes

- **Always test backups** before relying on them
- **Database volume persistence** is already configured and working
- **User data persists** through container restarts (confirmed working)
- **Regular backups** are additional safety measures
- **Volume backups** capture the complete database state
- **SQL dumps** are more portable and easier to inspect

## Emergency Contacts

In case of data loss or corruption:
1. Stop making changes immediately
2. Document what happened
3. Check for recent backups
4. Follow disaster recovery procedures
5. Contact system administrator if needed
