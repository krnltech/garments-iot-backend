"""
CRUD operations for IoT entities
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from ..models.iot import Machine, Worker, Bundle, MachineTarget, WorkerTarget
from ..schemas.iot import MachineTargetCreate, MachineTargetUpdate, WorkerTargetCreate, WorkerTargetUpdate
from datetime import datetime
from typing import List, Dict, Any, Optional

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

# Machine Target CRUD operations
def get_machine_targets(db: Session, skip: int = 0, limit: int = 100) -> List[MachineTarget]:
    """Get all machine targets with pagination"""
    return db.query(MachineTarget).options(joinedload(MachineTarget.machine)).offset(skip).limit(limit).all()

def get_machines_with_targets(db: Session, skip: int = 0, limit: int = 100) -> List[Machine]:
    """Get all machines with their targets loaded"""
    return db.query(Machine).options(joinedload(Machine.target)).offset(skip).limit(limit).all()

def get_machine_target(db: Session, machine_id: int) -> Optional[MachineTarget]:
    """Get machine target by machine ID"""
    return db.query(MachineTarget).filter(MachineTarget.id_machine == machine_id).first()

def create_machine_target(db: Session, machine_target: MachineTargetCreate) -> MachineTarget:
    """Create a new machine target"""
    db_target = MachineTarget(**machine_target.model_dump())
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target

def update_machine_target(db: Session, machine_id: int, machine_target: MachineTargetUpdate) -> Optional[MachineTarget]:
    """Update an existing machine target"""
    db_target = db.query(MachineTarget).filter(MachineTarget.id_machine == machine_id).first()
    if db_target:
        for key, value in machine_target.model_dump(exclude_unset=True).items():
            setattr(db_target, key, value)
        db.commit()
        db.refresh(db_target)
    return db_target

def delete_machine_target(db: Session, machine_id: int) -> bool:
    """Delete a machine target"""
    db_target = db.query(MachineTarget).filter(MachineTarget.id_machine == machine_id).first()
    if db_target:
        db.delete(db_target)
        db.commit()
        return True
    return False

# Worker Target CRUD operations
def get_worker_targets(db: Session, skip: int = 0, limit: int = 100) -> List[WorkerTarget]:
    """Get all worker targets with pagination"""
    return db.query(WorkerTarget).options(joinedload(WorkerTarget.worker)).offset(skip).limit(limit).all()

def get_workers_with_targets(db: Session, skip: int = 0, limit: int = 100) -> List[Worker]:
    """Get all workers with their targets loaded"""
    return db.query(Worker).options(joinedload(Worker.target)).offset(skip).limit(limit).all()

def get_worker_target(db: Session, worker_id: int) -> Optional[WorkerTarget]:
    """Get worker target by worker ID"""
    return db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker_id).first()

def create_worker_target(db: Session, worker_target: WorkerTargetCreate) -> WorkerTarget:
    """Create a new worker target"""
    db_target = WorkerTarget(**worker_target.model_dump())
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target

def update_worker_target(db: Session, worker_id: int, worker_target: WorkerTargetUpdate) -> Optional[WorkerTarget]:
    """Update an existing worker target"""
    db_target = db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker_id).first()
    if db_target:
        for key, value in worker_target.model_dump(exclude_unset=True).items():
            setattr(db_target, key, value)
        db.commit()
        db.refresh(db_target)
    return db_target

def delete_worker_target(db: Session, worker_id: int) -> bool:
    """Delete a worker target"""
    db_target = db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker_id).first()
    if db_target:
        db.delete(db_target)
        db.commit()
        return True
    return False
