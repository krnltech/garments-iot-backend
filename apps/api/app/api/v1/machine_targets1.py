"""
Machine Targets API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging

from ...db.database import get_db
from ...schemas.iot import (
    MachineTargetResponse, 
    MachineTargetCreate, 
    MachineTargetUpdate,
    MachineWithTargetResponse
)
from ...crud import iot as iot_crud
from ...services.auth import get_current_active_user
from ...models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/machine-targets", response_model=List[MachineTargetResponse])
async def get_machine_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all machine targets"""
    try:
        targets = iot_crud.get_machine_targets(db, skip=skip, limit=limit)
        return targets
    except Exception as e:
        logger.error(f"Error fetching machine targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/machines-with-targets", response_model=List[MachineWithTargetResponse])
async def get_machines_with_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all machines with their targets"""
    try:
        machines = iot_crud.get_machines_with_targets(db, skip=skip, limit=limit)
        return machines
    except Exception as e:
        logger.error(f"Error fetching machines with targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/machine-targets/{machine_id}", response_model=MachineTargetResponse)
async def get_machine_target(
    machine_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get machine target by machine ID"""
    try:
        target = iot_crud.get_machine_target(db, machine_id=machine_id)
        if not target:
            raise HTTPException(status_code=404, detail="Machine target not found")
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/machine-targets", response_model=MachineTargetResponse)
async def create_machine_target(
    machine_target: MachineTargetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new machine target"""
    try:
        # Check if machine exists
        machine = db.query(iot_crud.Machine).filter(iot_crud.Machine.id == machine_target.id_machine).first()
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        
        # Check if target already exists
        existing_target = iot_crud.get_machine_target(db, machine_id=machine_target.id_machine)
        if existing_target:
            raise HTTPException(status_code=400, detail="Machine target already exists")
        
        target = iot_crud.create_machine_target(db, machine_target=machine_target)
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/machine-targets/{machine_id}", response_model=MachineTargetResponse)
async def update_machine_target(
    machine_id: int,
    machine_target: MachineTargetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a machine target"""
    try:
        target = iot_crud.update_machine_target(db, machine_id=machine_id, machine_target=machine_target)
        if not target:
            raise HTTPException(status_code=404, detail="Machine target not found")
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/machine-targets/{machine_id}")
async def delete_machine_target(
    machine_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a machine target"""
    try:
        success = iot_crud.delete_machine_target(db, machine_id=machine_id)
        if not success:
            raise HTTPException(status_code=404, detail="Machine target not found")
        return {"message": "Machine target deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
