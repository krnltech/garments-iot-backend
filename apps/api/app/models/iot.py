"""
Database models for IoT entities
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base

class WorkerScan(Base):
    __tablename__ = "worker_scan"
    
    time = Column(DateTime, primary_key=True)
    id = Column(String(36), nullable=False)
    machine_id = Column(String(36), primary_key=True)
    name = Column(String, nullable=False)

class Bundle(Base):
    __tablename__ = "bundle"
    
    time = Column(DateTime, primary_key=True)
    id = Column(String(36), nullable=False)
    machine_id = Column(String(36), primary_key=True)
    employee_id = Column(String(36), nullable=False)

class Machine(Base):
    __tablename__ = "machine"
    
    id = Column(Integer, primary_key=True)
    label = Column(String(36), nullable=False, unique=True)
    location = Column(String(36), nullable=False)

class Worker(Base):
    __tablename__ = "worker"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(36), nullable=False)
    designation = Column(String(36), nullable=False)

class MachineTarget(Base):
    __tablename__ = "machine_target"
    
    id_machine = Column(Integer, ForeignKey("machine.id"), primary_key=True)
    target = Column(Integer, nullable=False)
    
    # Relationship to get machine details
    machine = relationship("Machine", backref="target")

class WorkerTarget(Base):
    __tablename__ = "worker_target"
    
    id_worker = Column(Integer, ForeignKey("worker.id"), primary_key=True)
    target = Column(Integer, nullable=False)
    
    # Relationship to get worker details
    worker = relationship("Worker", backref="target")
