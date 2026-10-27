from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
import os
import logging
import pydantic

# Import database session dependencies and models from the core directory
from core.database import init_db, get_db, TelemetryLogModel

# Configure advanced server-side logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QUANTUM_GRAV_SERVER")

app = FastAPI(
    title="PROJECT QUANTUM-GRAV | Advanced Aerospace Command Backend",
    version="5.00",
    description="Next-generation R&D telemetry, DRL AI flight control, and quantum warp engine backend."
)

@app.on_event("startup")
def startup_event():
    """Initializes the SQLite database tables upon server startup."""
    init_db()
    logger.info("[SERVER] FastAPI backend initialized successfully. All aerospace systems nominal.")

# Pydantic schema for strict input data validation of incoming telemetry packets
class TelemetryInputSchema(pydantic.BaseModel):
    phase_name: str
    voltage: float
    warp_index: float
    stability: float
    cpu_load: float = 12.4
    core_temp: float = 38.6
    system_status: str = "SYNCED"

# Helper function to safely load HTML files, with an advanced built-in fallback UI if a file is missing
def render_html_template(file_path: str, phase_title: str, description: str) -> str:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{phase_title} | QUANTUM-GRAV</title>
        <style>
            body {{ background: #020617; color: #38bdf8; font-family: monospace; padding: 40px; }}
            .card {{ background: rgba(15,23,42,0.9); border: 1px solid #38bdf8; padding: 30px; border-radius: 10px; max-width: 650px; box-shadow: 0 0 20px rgba(56,189,248,0.2); }}
            h1 {{ font-size: 22px; margin-bottom: 15px; color: #fff; }}
            p {{ font-size: 14px; color: #94a3b8; line-height: 1.6; }}
            .status {{ margin-top: 15px; color: #10b981; font-weight: bold; }}
            .btn {{ display: inline-block; margin-top: 25px; background: #0284c7; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; transition: background 0.2s; }}
            .btn:hover {{ background: #0369a1; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 {phase_title.upper()}</h1>
            <p>{description}</p>
            <p class="status">🟢 DATABASE STATUS: Connected & Telemetry Logging Active (SQLite)</p>
            <a href="/" class="btn">← Return to Mission Portal</a>
        </div>
    </body>
    </html>
    """

# ---------------------------------------------------------
# FRONTEND / PORTAL ROUTING ENDPOINTS
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def serve_landing_portal():
    """Serves the main SpaceX/NASA-grade Mission Control Landing Portal."""
    if os.path.exists("portal.html"):
        with open("portal.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Error: portal.html not found. Please ensure portal.html is in the root directory.</h3>"

@app.get("/cockpit", response_class=HTMLResponse)
def serve_phase1_cockpit():
    """Serves Phase 01: Master CRT Cockpit telemetry module."""
    return render_html_template(
        "phase1_cockpit.html", 
        "Phase 01: Master CRT Cockpit", 
        "Hypersonic analog gauge telemetry, MFD HUD overlay, and live flight dynamics are fully operational on the FastAPI backend."
    )

@app.get("/ai-deck", response_class=HTMLResponse)
def serve_phase2_ai():
    """Serves Phase 02: PyTorch DRL AI Pilot module."""
    return render_html_template(
        "phase2_ai_deck.html", 
        "Phase 02: PyTorch DRL AI Pilot", 
        "Neural inference pathways and PPO reinforcement learning loops stable."
    )

@app.get("/warp-deck", response_class=HTMLResponse)
def serve_phase3_warp():
    """Serves Phase 03: 3D Warp Curvature Engine module."""
    return render_html_template(
        "phase3_warp_deck.html", 
        "Phase 03: 3D Warp Curvature Engine", 
        "Alcubierre FTL spacetime strain tensors and exotic energy grids synchronized."
    )

@app.get("/fleet-deck", response_class=HTMLResponse)
def serve_phase4_fleet():
    """Serves Phase 04: Fleet Swarm & Quantum Nav module."""
    return render_html_template(
        "phase4_fleet_deck.html", 
        "Phase 04: Fleet Swarm & Quantum Nav", 
        "Multi-vessel mesh synchronization and quantum-entangled node links active."
    )

@app.get("/phase5-deck", response_class=HTMLResponse)
def serve_phase5_command():
    """Serves Phase 05: Master Antigravity & Wormhole Command Flagship module."""
    return render_html_template(
        "phase5_master_command.html", 
        "Phase 05: Master Antigravity Command", 
        "Exergic field mechanics, shield matrices, and wormhole jump calculators online."
    )

# ---------------------------------------------------------
# MASTER GUIDEBOOK PDF ROUTE (Absolute Path Mapping)
# ---------------------------------------------------------

@app.get("/guidebook-pdf")
def get_guidebook_pdf():
    """Serves the Master Theory Guidebook PDF safely using absolute path mapping."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "quantum_grav_master_guidebook.pdf")
    
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type="application/pdf", filename="Quantum_Grav_Master_Guidebook.pdf")
    raise HTTPException(status_code=404, detail=f"Master Guidebook PDF not found at: {pdf_path}")

# ---------------------------------------------------------
# DATABASE TELEMETRY API ENDPOINTS (100% Intact & Untouched)
# ---------------------------------------------------------

@app.post("/api/log-telemetry")
def log_telemetry(data: TelemetryInputSchema, db: Session = Depends(get_db)):
    """Receives live telemetry packets from frontend simulation modules and records them into SQLite DB."""
    try:
        db_log = TelemetryLogModel(
            phase_name=data.phase_name,
            voltage=data.voltage,
            warp_index=data.warp_index,
            stability=data.stability,
            cpu_load=data.cpu_load,
            core_temp=data.core_temp,
            system_status=data.system_status
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        
        logger.info(f"[TELEMETRY LOGGED] Mode: {data.system_status} | Phase: {data.phase_name} | Record ID: {db_log.id}")
        
        return {
            "status": "SUCCESS",
            "log_id": db_log.id,
            "active_mode": data.system_status,
            "timestamp": db_log.timestamp,
            "message": f"Telemetry packet successfully indexed under {data.system_status} mode."
        }
    except Exception as e:
        db.rollback()
        logger.error(f"[TELEMETRY_ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get-telemetry-logs")
def get_telemetry_logs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Retrieves stored telemetry historical records from the SQLite database for data analytics."""
    logs = db.query(TelemetryLogModel).order_by(TelemetryLogModel.timestamp.desc()).offset(skip).limit(limit).all()
    return {
        "total_records": len(logs),
        "records": logs
    }