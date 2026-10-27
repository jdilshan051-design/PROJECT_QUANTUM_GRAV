import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import datetime
import os
from sqlalchemy import create_engine, text
from core.physics_engine import QuantumGravPhysicsEngine

# Page Layout & Config
st.set_page_config(
    page_title="Next-Gen Hypersonic Cockpit Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Authentic Military CRT Green Cockpit CSS matching the exact reference UI
st.markdown("""
    <style>
    .stApp {
        background-color: #020608;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace;
    }
    .crt-panel {
        background: rgba(3, 15, 8, 0.95);
        border: 1px solid #00ff66;
        box-shadow: inset 0 0 15px rgba(0, 255, 102, 0.15), 0 0 20px rgba(0, 255, 102, 0.1);
        border-radius: 4px;
        padding: 12px;
        margin-bottom: 12px;
    }
    .top-strip {
        background: #010c04;
        border: 1px solid #00aa44;
        color: #00ff66;
        padding: 6px 12px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 1px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    div.stSlider > div[data-baseweb="slider"] {
        color: #00ff66;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Physics Engine
@st.cache_resource
def get_engine():
    return QuantumGravPhysicsEngine()

engine = get_engine()

# Initialize Supabase Database Connection if DATABASE_URL is available
@st.cache_resource
def get_db_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return None
    try:
        return create_engine(db_url)
    except Exception:
        return None

db_engine = get_db_engine()

# --- TOP MASTER STATUS STRIP ---
current_zulu = datetime.datetime.utcnow().strftime("%H:%M:%S Z")
db_status_text = "● SUPABASE LINK SECURE" if db_engine else "○ OFFLINE SIMULATION MODE"
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 12px; font-family: 'Courier New', monospace;">
        <div style="color: #00ff66; font-weight: bold;">Next-Gen Hypersonic Cockpit Dashboard</div>
        <div style="color: #888888; font-size: 11px;">☁️ 🔄 📥 ⚙️ ↗️</div>
    </div>
    <div class="top-strip">
        <div><span style="background: #110; border: 1px solid #f33; color: #f33; padding: 2px 6px;">SYS ALARM: OFF</span> &nbsp;&nbsp;|&nbsp;&nbsp; ⚠️ FLUX OVERHEAT [OK] &nbsp;|&nbsp; HTSC CRYOGENIC PUMP [ACTIVE] &nbsp;|&nbsp; TAJMAR G-DAMPENER [LOCKED]</div>
        <div>ZULU TIME: <b>{current_zulu}</b> &nbsp;&nbsp;|&nbsp;&nbsp; <span style="color: #00ffaa; border: 1px solid #00ffaa; padding: 2px 6px;">{db_status_text}</span></div>
    </div>
""", unsafe_allow_html=True)

# --- LAYOUT: LEFT CONTROL PANEL & RIGHT MFD COCKPIT GRID ---
col_ctrl, col_mfd = st.columns([0.28, 0.72])

with col_ctrl:
    st.markdown("""
        <div class="crt-panel">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:12px; color:#00ff66; font-weight:bold;">🕹️ FLIGHT THROTTLE CONTROLS</span>
                <span style="background:#010c04; border:1px solid #00aa44; font-size:9px; padding:2px 6px; color:#00ff66;">MANUAL / DRL</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    mach_input = st.slider("Airspeed Velocity (Mach)", min_value=1.0, max_value=20.0, value=12.10, step=0.01)
    st.markdown("<div style='display:flex; justify-content:space-between; font-size:10px; color:#44aa66; margin-top:-10px; margin-bottom:10px;'><span>Mach 1.0 (Subsonic)</span><span>Mach 20.0 (Hypersonic)</span></div>", unsafe_allow_html=True)

    voltage_input = st.slider("Gravimetric Field Voltage (MV)", min_value=0.0, max_value=2000.0, value=525.00, step=0.1)
    st.markdown("<div style='display:flex; justify-content:space-between; font-size:10px; color:#44aa66; margin-top:-10px; margin-bottom:10px;'><span>0 MV</span><span>2000 MV</span></div>", unsafe_allow_html=True)

    warp_density_input = st.slider("Warp Field Density Index", min_value=0.0, max_value=10.0, value=5.80, step=0.01)
    st.markdown("<div style='display:flex; justify-content:space-between; font-size:10px; color:#44aa66; margin-top:-10px; margin-bottom:15px;'><span>0.0</span><span>10.0</span></div>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:11px; color:#00ff66; margin-bottom:2px;'>🤖 Autonomous AI Pilot</p>", unsafe_allow_html=True)
    ai_mode = st.selectbox("AI Mode", ["Manual Override", "PyTorch DRL Autonomous v2", "Relativistic Auto-Sync"], label_visibility="collapsed")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    emergency_btn = st.button("🚨 EMERGENCY FLUX DUMP", use_container_width=True)

    if emergency_btn:
        voltage_input = 0.0
        warp_density_input = 0.0
        st.error("WARNING: FIELD COLLAPSED")
    
    st.markdown("<br><div style='font-size:10px; color:#00aa44; letter-spacing:1px;'>SECURE AVIONICS SUB v4.82</div>", unsafe_allow_html=True)

# Compute Live Telemetry
telemetry = engine.compute_flight_metrics(
    mach_speed=mach_input,
    field_voltage_mv=voltage_input,
    warp_bubble_density=warp_density_input
)

rel_time = telemetry['Relativistic_Time_Dilation']
warp_metrics = telemetry['Warp_Metrics']
cryo_temp_k = round(77.0 + (voltage_input * 0.025) + (warp_density_input * 0.4), 2)
g_force_cabin = round(max(1.0, 14.0 * (voltage_input * 0.009)), 2)

# Push telemetry to Supabase DB if connected and fetch recent live logs
db_logs_html = ""
if db_engine:
    try:
        with db_engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO starship_telemetry (cpu_tensor_core, aring_bus_rate, reactor_core_temp, subspace_distortion)
                    VALUES (:cpu, :bus, :temp, :dist)
                """),
                {
                    "cpu": float(mach_input * 4.2),
                    "bus": float(voltage_input * 1.5),
                    "temp": float(cryo_temp_k),
                    "dist": float(warp_density_input * 0.001)
                }
            )
        with db_engine.connect() as conn:
            recent_rows = conn.execute(text("SELECT timestamp, cpu_tensor_core, reactor_core_temp FROM starship_telemetry ORDER BY timestamp DESC LIMIT 4;")).fetchall()
            for r in recent_rows:
                db_logs_html += f"[DB_SYNC] {str(r[0])[11:19]} | CPU: {r[1]:.1f}% | Temp: {r[2]}K<br>"
    except Exception as e:
        db_logs_html = f"[DB_WARN] Sync active error: {str(e)[:35]}<br>"

with col_mfd:
    # Top Row Metrics & Analog Needle Gauges
    top_m1, top_m2, top_m3, top_m4, top_m5 = st.columns(5)
    
    with top_m1:
        st.markdown(f"""
            <div class="crt-panel" style="padding:8px;">
                <span style="font-size:9px; color:#44aa66;">CABIN PRESSURE</span><br>
                <strong style="font-size:15px; color:#00ff66;">98.9 kPa</strong><br>
                <span style="font-size:9px; color:#00aa44;">STABLE</span>
            </div>
        """, unsafe_allow_html=True)
    with top_m2:
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge", value=g_force_cabin,
            gauge={'axis': {'range': [0, 15], 'tickcolor': "#00ff66"}, 'bar': {'color': "#ff3333"}, 'bgcolor': "rgba(0,0,0,0)"}
        ))
        fig_g1.update_layout(paper_bgcolor='rgba(3,15,8,0.95)', height=68, margin=dict(l=10, r=10, t=5, b=5), font={'color': "#00ff66"})
        st.plotly_chart(fig_g1, use_container_width=True)
    with top_m3:
        st.markdown(f"""
            <div class="crt-panel" style="padding:8px;">
                <span style="font-size:9px; color:#44aa66;">HTSC CRYO TEMP</span><br>
                <strong style="font-size:15px; color:#00ff66;">{cryo_temp_k} K</strong><br>
                <span style="font-size:9px; color:#00aa44;">LIQUID NITROGEN</span>
            </div>
        """, unsafe_allow_html=True)
    with top_m4:
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge", value=cryo_temp_k,
            gauge={'axis': {'range': [0, 300], 'tickcolor': "#00ff66"}, 'bar': {'color': "#00ff66"}, 'bgcolor': "rgba(0,0,0,0)"}
        ))
        fig_g2.update_layout(paper_bgcolor='rgba(3,15,8,0.95)', height=68, margin=dict(l=10, r=10, t=5, b=5), font={'color': "#00ff66"})
        st.plotly_chart(fig_g2, use_container_width=True)
    with top_m5:
        st.markdown(f"""
            <div class="crt-panel" style="padding:8px; font-size:10px;">
                <span style="color:#44aa66; font-size:8px;">Lorentz Gamma (γ)</span><br>
                <strong style="color:#00ff66; font-size:13px;">{rel_time['Lorentz_Gamma']:.4f}</strong><br>
                <span style="color:#44aa66; font-size:8px;">Velocity Factor: OK</span>
            </div>
        """, unsafe_allow_html=True)

    # Row 1 MFDs: PFD HUD & Relativistic Curve
    mfd_hud, mfd_curve = st.columns([1, 1])

    with mfd_hud:
        st.markdown("""
            <div class="crt-panel">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#00ff66; border-bottom:1px solid #00aa44; padding-bottom:4px; margin-bottom:8px;">
                    <span>🟢 MFD-1: PRIMARY FLIGHT DISPLAY (CRT HUD)</span>
                    <span style="font-size:10px;">MODE: Manual Override</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        fig_hud = go.Figure()
        pitch_y = (mach_input - 8.5) * 1.5
        fig_hud.add_trace(go.Scatter(x=[-50, 50], y=[pitch_y, pitch_y], mode='lines', line=dict(color='#00ff66', width=2), showlegend=False))
        fig_hud.add_trace(go.Scatter(x=[-25, -10], y=[pitch_y + 10, pitch_y + 10], mode='lines', line=dict(color='#00ff66', width=1.5), showlegend=False))
        fig_hud.add_trace(go.Scatter(x=[10, 25], y=[pitch_y + 10, pitch_y + 10], mode='lines', line=dict(color='#00ff66', width=1.5), showlegend=False))
        fig_hud.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=14, color='#ff3333', symbol='circle-open', line=dict(width=2)), showlegend=False))
        fig_hud.add_trace(go.Scatter(x=[-6, 6], y=[0, 0], mode='lines', line=dict(color='#ff3333', width=2), showlegend=False))
        
        fig_hud.add_annotation(x=-45, y=28, text=f"SPEED: MACH {mach_input:.2f}", showarrow=False, font=dict(color="#00ff66", size=10, family="monospace"))
        fig_hud.add_annotation(x=45, y=28, text="ALT: 92,500 FT", showarrow=False, font=dict(color="#00ff66", size=10, family="monospace"))
        fig_hud.add_annotation(x=45, y=-28, text=f"SONIC: {telemetry['Sonic_Boom_Level_dB']:.1f} dB", showarrow=False, font=dict(color="#00ff66", size=10, family="monospace"))

        fig_hud.update_layout(
            paper_bgcolor='rgba(3,15,8,0.95)', plot_bgcolor='rgba(3,15,8,0.95)',
            xaxis=dict(range=[-60, 60], visible=False), yaxis=dict(range=[-35, 35], visible=False),
            height=190, margin=dict(l=5, r=5, t=5, b=5)
        )
        st.plotly_chart(fig_hud, use_container_width=True)

    with mfd_curve:
        st.markdown("""
            <div class="crt-panel">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#00ff66; border-bottom:1px solid #00aa44; padding-bottom:4px; margin-bottom:8px;">
                    <span>🟢 MFD-2: RELATIVISTIC TIME SLIP vs VELOCITY</span>
                    <span style="font-size:10px;">CH-2 LIVE</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        x_smooth = np.linspace(1, 20, 100)
        y_smooth = [(engine.calculate_relativistic_time_dilation(m, warp_density_input)['Time_Slip_Microseconds']) for m in x_smooth]
        
        fig_c = go.Figure()
        fig_c.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', line=dict(color='#00ff66', width=2, shape='spline')))
        fig_c.add_vline(x=mach_input, line_dash="dash", line_color="#ff3333")
        
        fig_c.update_layout(
            paper_bgcolor='rgba(3,15,8,0.95)', plot_bgcolor='rgba(3,15,8,0.95)',
            font={'color': "#00ff66"}, height=190, margin=dict(l=10, r=10, t=5, b=5),
            xaxis=dict(gridcolor='#003311', tickvals=[2, 5, 8, 11, 14, 17, 20]),
            yaxis=dict(gridcolor='#003311', range=[0, 750])
        )
        st.plotly_chart(fig_c, use_container_width=True)

    # Row 2 MFDs: Drag Suppression Gauge, 3D Warp, and AVIONICS LOG
    mfd_g, mfd_w, mfd_l = st.columns([1, 1, 1])

    with mfd_g:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=telemetry['Drag_Reduction_Percent'],
            number={'suffix': "%", 'font': {'color': "#00ff66"}},
            title={'text': "🟢 MFD-3: DRAG SUPPRESSION", 'font': {'color': "#00ff66", 'size': 11}},
            gauge={'axis': {'range': [0, 100], 'tickcolor': "#00ff66"}, 'bar': {'color': "#00ff66"}, 'bgcolor': "rgba(0,0,0,0)", 'bordercolor': "#00aa44"}
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(3,15,8,0.95)', plot_bgcolor='rgba(3,15,8,0.95)', font={'color': "#00ff66"}, height=175, margin=dict(l=10, r=10, t=25, b=5))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with mfd_w:
        st.markdown("""
            <div class="crt-panel" style="padding:6px;">
                <span style="font-size:11px; color:#00ff66;">🟢 MFD-4: 3D WARP CURVATURE</span>
            </div>
        """, unsafe_allow_html=True)
        x_s = np.linspace(-4, 4, 25)
        y_s = np.linspace(-4, 4, 25)
        X, Y = np.meshgrid(x_s, y_s)
        Z = -warp_density_input * np.exp(-(X**2 + Y**2) / 4.0)
        fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Greens')])
        fig_3d.update_layout(
            paper_bgcolor='rgba(3,15,8,0.95)', plot_bgcolor='rgba(3,15,8,0.95)', font={'color': "#00ff66"},
            height=140, margin=dict(l=0, r=0, t=0, b=0),
            scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False))
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with mfd_l:
        log_content = f"""
            [SYS] CRT High-Precision avionics link active.<br>
            [AI_PILOT] Sensor fusion matrix verified.<br>
            [WARP] T00 tensor responsive to fine throttle.<br>
            [TELEMETRY] Mach {mach_input:.2f} | Voltage {voltage_input}MV | T00 Stable.<br>
            {db_logs_html}
            [STATUS] All cockpit MFD channels operational.
        """
        st.markdown(f"""
            <div class="crt-panel">
                <div style="display:flex; justify-content:space-between; font-size:10px; color:#00ff66; border-bottom:1px solid #00aa44; padding-bottom:3px; margin-bottom:5px;">
                    <span>🟢 MFD-5: AVIONICS LOG & SUPABASE</span>
                    <span style="font-size:9px;">SECURE</span>
                </div>
                <div style="background: #010803; color: #00ff66; padding: 6px; border-radius: 2px; font-size: 10px; height: 115px; overflow-y: auto; line-height: 1.3;">
                    {log_content}
                </div>
            </div>
        """, unsafe_allow_html=True)