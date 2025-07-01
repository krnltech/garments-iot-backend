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

class WorkerTargetBase(BaseModel):
    target: int

class WorkerTargetCreate(WorkerTargetBase):
    id_worker: int

class WorkerTargetUpdate(WorkerTargetBase):
    pass

class WorkerTargetResponse(WorkerTargetBase):
    id_worker: int
    worker: Optional[WorkerResponse] = None
    
    class Config:
        from_attributes = True

class WorkerWithTargetResponse(WorkerResponse):
    worker_target: Optional[WorkerTargetResponse] = None
    
    class Config:
        from_attributes = True

class MachineStatusResponse(BaseModel):
    machine_id: str
    bundle_count: int
    bundles_per_minute: Optional[float]
    last_bundle_time_seconds: Optional[float]
    
    class Config:
        from_attributes = True
