"""
Pydantic schemas for IoT entities
"""
from pydantic import BaseModel

class MachineResponse(BaseModel):
    id: int
    label: str
    location: str
    
    class Config:
        from_attributes = True

class WorkerResponse(BaseModel):
    id: int
    name: str
    designation: str
    
    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    total_bundles_today: int
    total_machines: int
    total_workers: int
    timestamp: str
    user: str
