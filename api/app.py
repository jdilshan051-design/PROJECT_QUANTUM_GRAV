from __future__ import annotations
import json, logging, os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from core.physics_engine import QuantumGravPhysicsEngine
from core.warp_engine import WarpCurvatureEngine
from core.phase5_master_engine import Phase5MasterEngine
from core.drl_ai_model import AdvancedDeepLearningPilot
from core.swarm_mesh_engine import SwarmMeshEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumGravBackend")
app = FastAPI(title="Project Quantum-Grav API", version="2.1.0")
origins = [x.strip() for x in os.getenv("FRONTEND_ORIGINS", "*").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])
physics_engine, warp_engine = QuantumGravPhysicsEngine(), WarpCurvatureEngine()
phase5_engine, drl_ai, swarm_engine = Phase5MasterEngine(), AdvancedDeepLearningPilot(), SwarmMeshEngine()

def normalize_database_url():
    url = os.getenv("DATABASE_URL", "").strip()
    if url.startswith("postgres://"): url = "postgresql+psycopg2://" + url[11:]
    elif url.startswith("postgresql://"): url = "postgresql+psycopg2://" + url[13:]
    if url and "sslmode=" not in url: url += "&sslmode=require" if "?" in url else "?sslmode=require"
    return url

# Database persistence is opt-in. A stale DATABASE_URL must not prevent API startup.
database_enabled = os.getenv("ENABLE_DATABASE", "false").strip().lower() in {"1", "true", "yes"}
_db_url = normalize_database_url() if database_enabled else ""
db_engine = create_engine(_db_url, pool_pre_ping=True, pool_recycle=300) if _db_url else None

@app.on_event("startup")
def create_tables():
    if db_engine:
        with db_engine.begin() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS flight_logs (id BIGSERIAL PRIMARY KEY, mach_speed DOUBLE PRECISION NOT NULL, field_voltage DOUBLE PRECISION NOT NULL, warp_density DOUBLE PRECISION NOT NULL, telemetry_payload JSONB NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())"))

class FlightControlInput(BaseModel):
    mach_speed: float = Field(..., ge=0, le=100)
    field_voltage_mv: float = Field(..., ge=0, le=100000)
    warp_bubble_density: float = Field(..., ge=0, le=1000)
    quantum_entanglement_factor: Optional[float] = 1.0
    active_swarm_nodes: Optional[int] = Field(12, ge=1, le=500)

def evaluate(data):
    vals = data.model_dump() if hasattr(data, "model_dump") else data.dict()
    payload = {
        "physics": physics_engine.compute_flight_metrics(data.mach_speed, data.field_voltage_mv, data.warp_bubble_density),
        "warp_drive": warp_engine.calculate_warp_field(data.warp_bubble_density, data.field_voltage_mv),
        "phase5_command": phase5_engine.compute_phase5_command(warp_index=data.warp_bubble_density, antigravity_voltage=data.field_voltage_mv, fleet_size=data.active_swarm_nodes or 1),
        "drl_ai": drl_ai.compute_deep_learning_step(data.mach_speed, data.field_voltage_mv, data.warp_bubble_density, swarm_active=(data.active_swarm_nodes or 0)>1),
        "swarm_mesh": swarm_engine.compute_fleet_swarm(fleet_size=data.active_swarm_nodes or 1, warp_index=data.warp_bubble_density)
    }
    if db_engine:
        with db_engine.begin() as conn:
            conn.execute(text("INSERT INTO flight_logs (mach_speed, field_voltage, warp_density, telemetry_payload) VALUES (:mach, :voltage, :warp, CAST(:payload AS JSONB))"), {"mach": vals["mach_speed"], "voltage": vals["field_voltage_mv"], "warp": vals["warp_bubble_density"], "payload": json.dumps(payload)})
    return payload

@app.get("/")
def root(): return {"system":"Project Quantum-Grav API", "status":"ONLINE", "database_connected":db_engine is not None}
@app.get("/health")
def health():
    if not db_engine:
        return {"status": "ok", "database_connected": False}
    try:
        with db_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(503, "Database connection failed") from exc
    return {"status": "ok", "database_connected": True}
@app.post("/calculate")
def calculate(data: FlightControlInput):
    try: return {"status":"SUCCESS", "data":evaluate(data)}
    except Exception as exc:
        logger.exception("Calculation pipeline failed")
        raise HTTPException(500, "Calculation or database logging failed") from exc
@app.get("/api/warp-calculate")
def warp_calculate(warp:float=7, voltage:float=1200, ai_active:bool=False, shockwave:bool=False, antigravity:bool=False):
    return warp_engine.calculate_warp_field(warp, voltage, ai_active, shockwave, antigravity)
@app.get("/api/swarm-calculate")
def swarm_calculate(fleet_size:int=Query(5,ge=1,le=100), sync_phase:float=0, warp:float=7, qenap:bool=True, formation:str="SPHERE", cooling:bool=False, antigravity:bool=True):
    return swarm_engine.compute_fleet_swarm(fleet_size, sync_phase, warp, qenap, formation, cooling, antigravity)
@app.get("/api/ai-pilot")
def ai_pilot(mach:float=13.6, voltage:float=1200, warp:float=7, swarm:bool=False):
    return drl_ai.compute_deep_learning_step(mach, voltage, warp, swarm)
@app.get("/telemetry/history")
def history(limit:int=Query(10,ge=1,le=100)):
    if not db_engine: raise HTTPException(503,"DATABASE_URL is not configured")
    try:
        with db_engine.connect() as conn:
            rows=conn.execute(text("SELECT * FROM flight_logs ORDER BY id DESC LIMIT :limit"), {"limit":limit})
            return {"status":"SUCCESS", "logs":[dict(row._mapping) for row in rows]}
    except Exception as exc: raise HTTPException(500,"Could not read telemetry history") from exc
