"""
IoT data API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging

from ...db.database import get_db
from ...schemas.iot import MachineResponse, WorkerResponse, DashboardSummary, MachineStatusResponse
from ...crud import iot as iot_crud
from ...services.auth import get_current_active_user
from ...models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/machines", response_model=List[MachineResponse])
async def get_machines(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all machines (protected endpoint)"""
    try:
        machines = iot_crud.get_all_machines(db)
        return machines
    except Exception as e:
        logger.error(f"Error fetching machines: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/workers", response_model=List[WorkerResponse])
async def get_workers(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all workers (protected endpoint)"""
    try:
        workers = iot_crud.get_all_workers(db)
        return workers
    except Exception as e:
        logger.error(f"Error fetching workers: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get dashboard summary (protected endpoint)"""
    try:
        summary_data = iot_crud.get_dashboard_summary(db)
        summary_data["user"] = current_user.username
        return summary_data
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/machine-status", response_model=List[MachineStatusResponse])
async def get_machine_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get machine status with bundle analysis (protected endpoint)"""
    try:
        machine_status = iot_crud.get_machine_status(db)
        return machine_status
    except Exception as e:
        logger.error(f"Error fetching machine status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
