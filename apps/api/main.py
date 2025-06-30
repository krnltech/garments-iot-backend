from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, text, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
from contextlib import asynccontextmanager
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
DATABASE_URL = f"postgresql://{os.getenv('TIMESCALE_USER', 'postgres')}:{os.getenv('TIMESCALE_PASSWORD', 'password')}@{os.getenv('TIMESCALE_HOST', 'localhost')}:5432/{os.getenv('TIMESCALE_DB', 'metrics')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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

# Pydantic Models
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None

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

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (if needed)

# FastAPI app
app = FastAPI(
    title="Garments IoT Backend API",
    description="Backend API for IoT-integrated garments production tracking with OAuth2 authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if username already exists
        db_user = get_user(db, username=user.username)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
        
        # Check if email already exists
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=True,
            is_admin=False  # Default to non-admin
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.get("/auth/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

# Protected endpoints - require authentication
@app.get("/machines", response_model=List[MachineResponse])
async def get_machines(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all machines (protected endpoint)"""
    try:
        machines = db.query(Machine).all()
        return machines
    except Exception as e:
        logger.error(f"Error fetching machines: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/workers", response_model=List[WorkerResponse])
async def get_workers(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all workers (protected endpoint)"""
    try:
        workers = db.query(Worker).all()
        return workers
    except Exception as e:
        logger.error(f"Error fetching workers: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/dashboard/summary")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get dashboard summary (protected endpoint)"""
    try:
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
            "timestamp": now,
            "user": current_user.username
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Machine Target endpoints
@app.get("/machines-with-targets", response_model=List[MachineWithTargetResponse])
async def get_machines_with_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all machines with their targets"""
    try:
        machines = db.query(Machine).offset(skip).limit(limit).all()
        result = []
        for machine in machines:
            target = db.query(MachineTarget).filter(MachineTarget.id_machine == machine.id).first()
            machine_dict = {
                "id": machine.id,
                "label": machine.label,
                "location": machine.location,
                "machine_target": {
                    "id_machine": target.id_machine,
                    "target": target.target
                } if target else None
            }
            result.append(machine_dict)
        return result
    except Exception as e:
        logger.error(f"Error fetching machines with targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/machine-targets", response_model=List[MachineTargetResponse])
async def get_machine_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all machine targets"""
    try:
        targets = db.query(MachineTarget).offset(skip).limit(limit).all()
        return targets
    except Exception as e:
        logger.error(f"Error fetching machine targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/machine-targets/{machine_id}", response_model=MachineTargetResponse)
async def get_machine_target(
    machine_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get machine target by machine ID"""
    try:
        target = db.query(MachineTarget).filter(MachineTarget.id_machine == machine_id).first()
        if not target:
            raise HTTPException(status_code=404, detail="Machine target not found")
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/machine-targets", response_model=MachineTargetResponse)
async def create_machine_target(
    machine_target: MachineTargetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new machine target"""
    try:
        # Check if machine exists
        machine = db.query(Machine).filter(Machine.id == machine_target.id_machine).first()
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        
        # Check if target already exists
        existing_target = db.query(MachineTarget).filter(MachineTarget.id_machine == machine_target.id_machine).first()
        if existing_target:
            raise HTTPException(status_code=400, detail="Machine target already exists")
        
        db_target = MachineTarget(**machine_target.model_dump())
        db.add(db_target)
        db.commit()
        db.refresh(db_target)
        return db_target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/machine-targets/{machine_id}", response_model=MachineTargetResponse)
async def update_machine_target(
    machine_id: int,
    machine_target: MachineTargetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a machine target"""
    try:
        db_target = db.query(MachineTarget).filter(MachineTarget.id_machine == machine_id).first()
        if not db_target:
            raise HTTPException(status_code=404, detail="Machine target not found")
        
        for key, value in machine_target.model_dump(exclude_unset=True).items():
            setattr(db_target, key, value)
        db.commit()
        db.refresh(db_target)
        return db_target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/machine-targets/{machine_id}")
async def delete_machine_target(
    machine_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a machine target"""
    try:
        db_target = db.query(MachineTarget).filter(MachineTarget.id_machine == machine_id).first()
        if not db_target:
            raise HTTPException(status_code=404, detail="Machine target not found")
        
        db.delete(db_target)
        db.commit()
        return {"message": "Machine target deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting machine target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin-only endpoints
@app.get("/admin/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Worker Target endpoints
@app.get("/workers-with-targets", response_model=List[WorkerWithTargetResponse])
async def get_workers_with_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all workers with their targets"""
    try:
        workers = db.query(Worker).offset(skip).limit(limit).all()
        result = []
        for worker in workers:
            target = db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker.id).first()
            worker_dict = {
                "id": worker.id,
                "name": worker.name,
                "designation": worker.designation,
                "worker_target": {
                    "id_worker": target.id_worker,
                    "target": target.target
                } if target else None
            }
            result.append(worker_dict)
        return result
    except Exception as e:
        logger.error(f"Error fetching workers with targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/worker-targets", response_model=List[WorkerTargetResponse])
async def get_worker_targets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all worker targets"""
    try:
        targets = db.query(WorkerTarget).offset(skip).limit(limit).all()
        return targets
    except Exception as e:
        logger.error(f"Error fetching worker targets: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/worker-targets/{worker_id}", response_model=WorkerTargetResponse)
async def get_worker_target(
    worker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get worker target by worker ID"""
    try:
        target = db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker_id).first()
        if not target:
            raise HTTPException(status_code=404, detail="Worker target not found")
        return target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/worker-targets", response_model=WorkerTargetResponse)
async def create_worker_target(
    worker_target: WorkerTargetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new worker target"""
    try:
        # Check if worker exists
        worker = db.query(Worker).filter(Worker.id == worker_target.id_worker).first()
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        
        # Check if target already exists
        existing_target = db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker_target.id_worker).first()
        if existing_target:
            raise HTTPException(status_code=400, detail="Worker target already exists")
        
        db_target = WorkerTarget(**worker_target.model_dump())
        db.add(db_target)
        db.commit()
        db.refresh(db_target)
        return db_target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/worker-targets/{worker_id}", response_model=WorkerTargetResponse)
async def update_worker_target(
    worker_id: int,
    worker_target: WorkerTargetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a worker target"""
    try:
        db_target = db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker_id).first()
        if not db_target:
            raise HTTPException(status_code=404, detail="Worker target not found")
        
        for key, value in worker_target.model_dump(exclude_unset=True).items():
            setattr(db_target, key, value)
        db.commit()
        db.refresh(db_target)
        return db_target
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/worker-targets/{worker_id}")
async def delete_worker_target(
    worker_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a worker target"""
    try:
        db_target = db.query(WorkerTarget).filter(WorkerTarget.id_worker == worker_id).first()
        if not db_target:
            raise HTTPException(status_code=404, detail="Worker target not found")
        
        db.delete(db_target)
        db.commit()
        return {"message": "Worker target deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting worker target: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
