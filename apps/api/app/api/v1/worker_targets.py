"""
Worker Targets API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging

from ...db.database import get_db
from ...schemas.iot import (
    WorkerTargetResponse, 
    WorkerTargetCreate, 
    WorkerTargetUpdate,
    WorkerWithTargetResponse
)
from ...crud import iot as iot_crud
from ...services.auth import get_current_active_user
from ...models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/worker-targets", response_model=List[WorkerTargetResponse])
async def get_worker_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all worker targets"""
    try:
        targets = iot_crud.get_worker_targets(db, skip=skip, limit=limit)
        return targets
    except Exception as e:
        logger.error(f"Error fetching worker targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/workers-with-targets", response_model=List[WorkerWithTargetResponse])
async def get_workers_with_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all workers with their targets"""
    try:
        workers = iot_crud.get_workers_with_targets(db, skip=skip, limit=limit)
        return workers
    except Exception as e:
        logger.error(f"Error fetching workers with targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/worker-targets/{worker_id}", response_model=WorkerTargetResponse)
async def get_worker_target(
    worker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get worker target by worker ID"""
    try:
        target = iot_crud.get_worker_target(db, worker_id=worker_id)
        if not target:
            raise HTTPException(status_code=404, detail="Worker target not found")
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/worker-targets", response_model=WorkerTargetResponse)
async def create_worker_target(
    worker_target: WorkerTargetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new worker target"""
    try:
        # Check if worker exists
        worker = db.query(iot_crud.Worker).filter(iot_crud.Worker.id == worker_target.id_worker).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        
        # Check if target already exists
        existing_target = iot_crud.get_worker_target(db, worker_id=worker_target.id_worker)
        if existing_target:
            raise HTTPException(status_code=400, detail="Worker target already exists")
        
        target = iot_crud.create_worker_target(db, worker_target=worker_target)
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/worker-targets/{worker_id}", response_model=WorkerTargetResponse)
async def update_worker_target(
    worker_id: int,
    worker_target: WorkerTargetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a worker target"""
    try:
        target = iot_crud.update_worker_target(db, worker_id=worker_id, worker_target=worker_target)
        if not target:
            raise HTTPException(status_code=404, detail="Worker target not found")
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/worker-targets/{worker_id}")
async def delete_worker_target(
    worker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a worker target"""
    try:
        success = iot_crud.delete_worker_target(db, worker_id=worker_id)
        if not success:
            raise HTTPException(status_code=404, detail="Worker target not found")
        return {"message": "Worker target deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
