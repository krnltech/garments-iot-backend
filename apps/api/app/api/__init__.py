"""
Main API router
"""
from fastapi import APIRouter
from .v1 import api_router as api_v1_router

router = APIRouter()
router.include_router(api_v1_router, prefix="/v1")
