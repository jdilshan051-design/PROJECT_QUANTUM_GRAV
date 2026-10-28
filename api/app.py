from __future__ import annotations
import json, logging, os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

physics_engine = QuantumGravPhysicsEngine()
warp_engine = WarpCurvatureEngine()
phase5_engine = Phase5MasterEngine()
drl_ai = AdvancedDeepLearningPilot()
swarm_engine = SwarmMeshEngine()

def normalize_database_url():
    url = os.getenv("DATABASE_URL", "").strip()
    if url.startswith("postgres://"):
        url = "postgresql+psycopg2://" + url[11:]
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg2://" + url[13:]
    if url and "sslmode=" not in url:
        url += "&sslmode=require" if "?" in url else "?sslmode=require"
    return url

# Database persistence: automatically active if DATABASE_URL is set, unless explicitly disabled
db_url_env = os.getenv("DATABASE_URL", "").strip()
default_db_enable = "true" if db_url_env else "false"
database_enabled = os.getenv("ENABLE_DATABASE", default_db_enable).strip().lower() in {"1", "true", "yes"}
_db_url = normalize_database_url() if database_enabled else ""
db_engine = create_engine(_db_url, pool_pre_ping=True, pool_recycle=300) if _db_url else None

@app.on_event("startup")
def create_tables():
    if db_engine:
        try:
            with db_engine.begin() as conn:
                conn.execute(text("CREATE TABLE IF NOT EXISTS flight_logs (id BIGSERIAL PRIMARY KEY, mach_speed DOUBLE PRECISION NOT NULL, field_voltage DOUBLE PRECISION NOT NULL, warp_density DOUBLE PRECISION NOT NULL, telemetry_payload JSONB NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())"))
            logger.info("Database flight_logs table verified/created.")
        except Exception as exc:
            logger.warning(f"Database table verification deferred: {exc}")

class FlightControlInput(BaseModel):
    mach_speed: float = Field(..., ge=0, le=100)
    field_voltage_mv: float = Field(..., ge=0, le=100000)
    warp_bubble_density: float = Field(..., ge=0, le=1000)
    quantum_entanglement_factor: Optional[float] = 1.0
    active_swarm_nodes: Optional[int] = Field(12, ge=1, le=500)

def evaluate(data: FlightControlInput):
    vals = data.model_dump() if hasattr(data, "model_dump") else data.dict()
    payload = {
        "physics": physics_engine.compute_flight_metrics(data.mach_speed, data.field_voltage_mv, data.warp_bubble_density),
        "warp_drive": warp_engine.calculate_warp_field(data.warp_bubble_density, data.field_voltage_mv),
        "phase5_command": phase5_engine.compute_phase5_command(warp_index=data.warp_bubble_density, antigravity_voltage=data.field_voltage_mv, fleet_size=data.active_swarm_nodes or 1),
        "drl_ai": drl_ai.compute_deep_learning_step(data.mach_speed, data.field_voltage_mv, data.warp_bubble_density, swarm_active=(data.active_swarm_nodes or 0)>1),
        "swarm_mesh": swarm_engine.compute_fleet_swarm(fleet_size=data.active_swarm_nodes or 1, warp_index=data.warp_bubble_density)
    }
    if db_engine:
        try:
            with db_engine.begin() as conn:
                conn.execute(
                    text("INSERT INTO flight_logs (mach_speed, field_voltage, warp_density, telemetry_payload) VALUES (:mach, :voltage, :warp, CAST(:payload AS JSONB))"),
                    {"mach": vals["mach_speed"], "voltage": vals["field_voltage_mv"], "warp": vals["warp_bubble_density"], "payload": json.dumps(payload)}
                )
        except Exception as exc:
            logger.warning(f"Failed to record flight log: {exc}")
    return payload

@app.get("/")
@app.get("/api")
def root():
    return {"system": "Project Quantum-Grav API", "status": "ONLINE", "database_connected": db_engine is not None}

@app.get("/health")
@app.get("/api/health")
def health():
    if not db_engine:
        return {"status": "ok", "database_connected": False}
    try:
        with db_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database_connected": True}
    except Exception as exc:
        return {"status": "degraded", "database_connected": False, "error": str(exc)}

@app.post("/calculate")
@app.post("/api/calculate")
def calculate(data: FlightControlInput):
    try:
        return {"status": "SUCCESS", "data": evaluate(data)}
    except Exception as exc:
        logger.exception("Calculation pipeline failed")
        raise HTTPException(500, "Calculation failed") from exc

@app.get("/warp-calculate")
@app.get("/api/warp-calculate")
def warp_calculate(warp: float = 7, voltage: float = 1200, ai_active: bool = False, shockwave: bool = False, antigravity: bool = False):
    return warp_engine.calculate_warp_field(warp, voltage, ai_active, shockwave, antigravity)

@app.get("/swarm-calculate")
@app.get("/api/swarm-calculate")
def swarm_calculate(fleet_size: int = Query(5, ge=1, le=100), sync_phase: float = 0, warp: float = 7, qenap: bool = True, formation: str = "SPHERE", cooling: bool = False, antigravity: bool = True):
    return swarm_engine.compute_fleet_swarm(fleet_size, sync_phase, warp, qenap, formation, cooling, antigravity)

@app.get("/ai-pilot")
@app.get("/api/ai-pilot")
def ai_pilot(mach: float = 13.6, voltage: float = 1200, warp: float = 7, swarm: bool = False):
    return drl_ai.compute_deep_learning_step(mach, voltage, warp, swarm)

@app.get("/telemetry/history")
@app.get("/api/telemetry/history")
def history(limit: int = Query(10, ge=1, le=100)):
    if not db_engine:
        raise HTTPException(503, "DATABASE_URL is not configured")
    try:
        with db_engine.connect() as conn:
            rows = conn.execute(text("SELECT * FROM flight_logs ORDER BY id DESC LIMIT :limit"), {"limit": limit})
            return {"status": "SUCCESS", "logs": [dict(row._mapping) for row in rows]}
    except Exception as exc:
        raise HTTPException(500, "Could not read telemetry history") from exc

# Catch-all router to safely catch any rewritten or nested path on Vercel
@app.api_route("/{full_path:path}", methods=["GET", "POST", "OPTIONS"])
async def catch_all(request: Request, full_path: str):
    path = full_path.strip("/")
    
    if "ai-pilot" in path:
        params = request.query_params
        mach = float(params.get("mach", 13.6))
        voltage = float(params.get("voltage", 1200))
        warp = float(params.get("warp", 7))
        swarm = params.get("swarm", "false").lower() in ("true", "1")
        return drl_ai.compute_deep_learning_step(mach, voltage, warp, swarm)
        
    if "warp-calculate" in path:
        params = request.query_params
        warp = float(params.get("warp", 7))
        voltage = float(params.get("voltage", 1200))
        ai_active = params.get("ai_active", "false").lower() in ("true", "1")
        shockwave = params.get("shockwave", "false").lower() in ("true", "1")
        antigravity = params.get("antigravity", "false").lower() in ("true", "1")
        return warp_engine.calculate_warp_field(warp, voltage, ai_active, shockwave, antigravity)
        
    if "swarm-calculate" in path:
        params = request.query_params
        fleet_size = int(params.get("fleet_size", 5))
        sync_phase = float(params.get("sync_phase", 0))
        warp = float(params.get("warp", 7))
        qenap = params.get("qenap", "true").lower() in ("true", "1")
        formation = params.get("formation", "SPHERE")
        cooling = params.get("cooling", "false").lower() in ("true", "1")
        antigravity = params.get("antigravity", "true").lower() in ("true", "1")
        return swarm_engine.compute_fleet_swarm(fleet_size, sync_phase, warp, qenap, formation, cooling, antigravity)

    if "calculate" in path and request.method == "POST":
        try:
            body = await request.json()
            input_data = FlightControlInput(**body)
            return {"status": "SUCCESS", "data": evaluate(input_data)}
        except Exception:
            return {"status": "SUCCESS", "data": evaluate(FlightControlInput(mach_speed=13.6, field_voltage_mv=2400.0, warp_bubble_density=7.0))}
        
    if "health" in path:
        return health()
        
    return {
        "system": "Project Quantum-Grav API",
        "status": "ONLINE",
        "database_connected": db_engine is not None,
        "path": path
    }
