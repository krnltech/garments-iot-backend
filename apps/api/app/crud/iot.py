"""
CRUD operations for IoT entities
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.iot import Machine, Worker, Bundle
from datetime import datetime
from typing import List, Dict, Any

def get_all_machines(db: Session) -> List[Machine]:
    """Get all machines"""
    return db.query(Machine).all()

def get_all_workers(db: Session) -> List[Worker]:
    """Get all workers"""
    return db.query(Worker).all()

def get_dashboard_summary(db: Session) -> Dict[str, Any]:
    """Get dashboard summary data"""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Total bundles today
    total_bundles_today = db.execute(text("""
        SELECT COUNT(*) FROM bundle WHERE time >= :today_start
    """), {"today_start": today_start}).scalar()
    
    # Total machines
    total_machines = db.execute(text("""
        SELECT COUNT(*) FROM machine
    """)).scalar()
    
    # Total workers
    total_workers = db.execute(text("""
        SELECT COUNT(*) FROM worker
    """)).scalar()
    
    return {
        "total_bundles_today": total_bundles_today or 0,
        "total_machines": total_machines or 0,
        "total_workers": total_workers or 0,
        "timestamp": now.isoformat(),
    }
