"""
Pydantic schemas for IoT entities
"""
from pydantic import BaseModel
from typing import Optional

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

class MachineTargetBase(BaseModel):
    target: int

class MachineTargetCreate(MachineTargetBase):
    id_machine: int

class MachineTargetUpdate(MachineTargetBase):
    pass

class MachineTargetResponse(MachineTargetBase):
    id_machine: int
    machine: Optional[MachineResponse] = None
    
    class Config:
        from_attributes = True

class MachineWithTargetResponse(MachineResponse):
    machine_target: Optional[MachineTargetResponse] = None
    
    class Config:
        from_attributes = True
