"""
API v1 router
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .iot import router as iot_router
from .admin import router as admin_router
from .machine_targets import router as machine_targets_router
from .worker_targets import router as worker_targets_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(iot_router, tags=["iot"])
api_router.include_router(machine_targets_router, tags=["machine-targets"])
api_router.include_router(worker_targets_router, tags=["worker-targets"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
