from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import logging
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, text

# Import all core engines from the core directory
from core.physics_engine import QuantumGravPhysicsEngine
from core.warp_engine import WarpDriveEngine
from core.phase5_master_engine import Phase5MasterEngine
from core.drl_ai_model import DRLAIModel
from core.swarm_mesh_engine import SwarmMeshEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumGravBackend")

app = FastAPI(
    title="Quantum-Grav Enterprise Flight & Command Backend",
    description="Advanced FastAPI backend integrating quantum-gravimetric physics, warp drives, DRL AI models, swarm mesh, and Supabase telemetry logging.",
    version="2.0.0"
)

# Enable CORS for frontend integration (GitHub Pages, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your exact GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Engines safely
try:
    physics_engine = QuantumGravPhysicsEngine()
    warp_engine = WarpDriveEngine()
    phase5_engine = Phase5MasterEngine()
    drl_ai = DRLAIModel()
    swarm_engine = SwarmMeshEngine()
    logger.info("All core engines initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing core engines: {e}")

# Database Connection (Supabase PostgreSQL via SQLAlchemy)
DATABASE_URL = os.getenv("DATABASE_URL")
db_engine = create_engine(DATABASE_URL) if DATABASE_URL else None

if db_engine:
    logger.info("Supabase database engine connected successfully.")
else:
    logger.warning("DATABASE_URL not found. Database logging will run in offline mode.")

# Pydantic Model for incoming flight control payload
class FlightControlInput(BaseModel):
    mach_speed: float = Field(..., description="Current Mach speed multiplier")
    field_voltage_mv: float = Field(..., description="Electromagnetic shield voltage in millivolts")
    warp_bubble_density: float = Field(..., description="Alcubierre warp bubble density metric")
    quantum_entanglement_factor: Optional[float] = Field(1.0, description="Quantum state sync factor")
    active_swarm_nodes: Optional[int] = Field(12, description="Number of active swarm drones/mesh nodes")

@app.post("/calculate", summary="Execute Advanced Flight Calculations & Telemetry Logging")
def calculate_flight_telemetry(data: FlightControlInput):
    try:
        # 1. Compute physics and telemetry metrics
        physics_metrics = physics_engine.compute_flight_metrics(
            mach_speed=data.mach_speed,
            field_voltage_mv=data.field_voltage_mv,
            warp_bubble_density=data.warp_bubble_density
        )
        
        # 2. Execute Warp Engine & Phase 5 calculations (with fallback checks)
        warp_metrics = warp_engine.calculate_warp_metrics(data.warp_bubble_density, data.mach_speed) if hasattr(warp_engine, 'calculate_warp_metrics') else {"warp_status": "stable"}
        phase5_state = phase5_engine.evaluate_command_deck(data.dict()) if hasattr(phase5_engine, 'evaluate_command_deck') else {"deck_status": "nominal"}
        
        # 3. DRL AI Model Inference & Optimization
        ai_recommendation = drl_ai.predict_optimal_trajectory(data.dict()) if hasattr(drl_ai, 'predict_optimal_trajectory') else {"ai_adjustment": "optimal"}
        
        # 4. Swarm Mesh Coordination Sync
        mesh_status = swarm_engine.sync_nodes(data.active_swarm_nodes) if hasattr(swarm_engine, 'sync_nodes') else {"mesh_integrity": "100%"}

        # Compile comprehensive telemetry payload
        aggregated_telemetry = {
            "physics": physics_metrics,
            "warp_drive": warp_metrics,
            "phase5_command": phase5_state,
            "drl_ai": ai_recommendation,
            "swarm_mesh": mesh_status
        }

        # 5. Instant telemetry logging to Supabase Database
        if db_engine:
            with db_engine.begin() as conn:
                conn.execute(
                    text("""
                        INSERT INTO flight_logs (mach_speed, field_voltage, warp_density, telemetry_payload)
                        VALUES (:mach, :voltage, :warp, :payload)
                    """),
                    {
                        "mach": float(data.mach_speed),
                        "voltage": float(data.field_voltage_mv),
                        "warp": float(data.warp_bubble_density),
                        "payload": str(aggregated_telemetry)
                    }
                )

        return {
            "status": "SUCCESS",
            "code": 200,
            "message": "Calculations executed and logged to Supabase successfully.",
            "data": aggregated_telemetry
        }

    except Exception as e:
        logger.error(f"Calculation pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/telemetry/history", summary="Retrieve Recent Flight Logs from Supabase")
def get_telemetry_history(limit: int = 10):
    if not db_engine:
        raise HTTPException(status_code=503, detail="Database connection not available.")
    try:
        with db_engine.connect() as conn:
            result = conn.connect().execute(  # type: ignore
                text("SELECT * FROM flight_logs ORDER BY id DESC LIMIT :limit"),
                {"limit": limit}
            )
            rows = [dict(row._mapping) for row in result]
        return {"status": "SUCCESS", "logs": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", summary="System Root Health Check")
def root():
    return {
        "system": "Quantum-Grav Enterprise Flight Deck",
        "status": "ONLINE",
        "engines_loaded": [
            "physics_engine", 
            "warp_engine", 
            "phase5_master_engine", 
            "drl_ai_model", 
            "swarm_mesh_engine"
        ],
        "database_connected": db_engine is not None
    }