from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime
import logging

# Configure advanced logging for telemetry tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QUANTUM_GRAV_DB")

# SQLite database file path with high-performance concurrency settings
SQLALCHEMY_DATABASE_URL = "sqlite:///./quantum_grav.db"

# Initialize SQLite engine with thread-safe connection arguments
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TelemetryLogModel(Base):
    """
    Advanced Telemetry Log Model for Project Quantum-Grav.
    Stores real-time flight telemetry, warp metrics, and system stability indexes.
    """
    __tablename__ = "telemetry_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phase_name = Column(String(50), index=True, nullable=False)
    voltage = Column(Float, nullable=False)
    warp_index = Column(Float, nullable=False)
    stability = Column(Float, nullable=False)
    cpu_load = Column(Float, default=0.0)
    core_temp = Column(Float, default=0.0)
    system_status = Column(String(20), default="SYNCED")
    payload_metadata = Column(Text, nullable=True)  # JSON or stringified diagnostics
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

def init_db() -> None:
    """
    Initializes and creates all database tables defined under declarative Base.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("[DATABASE] SQLite database 'quantum_grav.db' initialized successfully with advanced schemas.")
    except Exception as e:
        logger.error(f"[DATABASE_ERROR] Failed to initialize database: {e}")
        raise e

def get_db():
    """
    Dependency generator for FastAPI routes to manage database sessions securely.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()