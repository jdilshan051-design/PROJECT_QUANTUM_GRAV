import math
import random

class SwarmMeshEngine:
    """
    Phase 4: Ultimate Interstellar Fleet Swarm, Quantum Navigation, Antigravity & Advanced Telemetry Engine.
    Includes:
    1. Multi-Vessel Swarm Telemetry & Mesh Synchronization
    2. Quantum Entanglement Navigation & Autonomous Pathfinding (QENAP)
    3. Interstellar Gravitational Anomaly & Dark Matter Radar Scan
    4. Quantum Entanglement Telemetry (QETB) Packet Loss & Sync Matrix Grid
    5. Warp Bubble Interference & Overlap Density Heatmap
    6. Crew Life Support & Cosmic Radiation Absorption Monitor
    """
    def __init__(self):
        self.step_counter = 0

    def compute_fleet_swarm(self, fleet_size: int = 5, sync_phase_deg: float = 0.0, warp_index: float = 7.0, qenap_active: bool = True, formation: str = "SPHERE", emergency_cooling: bool = False, antigravity_repulsion: bool = True):
        self.step_counter += 1

        fleet_vessels = []
        base_stability = 99.4
        repulsion_boost = 1.25 if antigravity_repulsion else 0.90

        for i in range(1, fleet_size + 1):
            phase_offset = sync_phase_deg + (i * (360.0 / fleet_size))

            form_multiplier = 1.0
            if formation == "WEDGE":
                form_multiplier = 1.02 + (i * 0.01)
            elif formation == "ECHELON":
                form_multiplier = 0.98 + (i * 0.015)
            elif formation == "LINE":
                form_multiplier = 1.05

            vessel_warp = round(warp_index * form_multiplier + (math.sin(math.radians(phase_offset + self.step_counter * 5)) * 0.1), 2)
            vessel_stability = round(min(100.0, max(85.0, base_stability - (abs(vessel_warp - warp_index) * 8.0)) * repulsion_boost), 2)

            # Fixed missing multiplication operator (-)
            sync_health = round(100.0 - (math.cos(math.radians(phase_offset)) * 1.0), 2)

            fleet_vessels.append({
                "vessel_id": f"QUANTUM-SWARM-0{i}",
                "warp_factor": vessel_warp,
                "stability": vessel_stability,
                "sync_health": sync_health,
                "phase_angle": round(phase_offset % 360, 1),
                "mesh_role": "COMMAND_NODE" if i == 1 else "RESONANCE_RELAY"
            })

        # QENAP Pathfinding & Radar Anomaly Detection
        anomalies_detected = 0 if (qenap_active or antigravity_repulsion) else 2
        pathfinding_status = "RADAR_SECURE_SHIELDED" if antigravity_repulsion else ("OPTIMAL_CLEAR" if qenap_active else "ANOMALY_WARNING")

        # Fixed missing multiplication operator (-)
        route_efficiency = round(99.98 - (anomalies_detected * 10.0), 2)

        # QETB Packet Loss & Sync Matrix
        qetb_mesh_bandwidth = round(85.5 + (fleet_size * 14.2), 2)

        # Fixed missing multiplication operator (-)
        entanglement_fidelity = round(99.99 - (abs(warp_index - 7.0) * 0.1), 2)
        packet_loss_percent = round(max(0.001, (warp_index - 5.0) * 0.01), 3)
        sync_matrix_status = "LOCKED_SYNCHRONIZED"

        # Warp Bubble Interference & Overlap Heatmap Metric (Fixed missing operators)
        bubble_overlap_density = round(1.85 * warp_index * (fleet_size / 5.0), 2) # MW/m³
        interference_index = round(0.04 * abs(warp_index - 7.0), 3)

        # Life Support & Cosmic Radiation Monitor
        base_thermal = 420.0 + (warp_index * 42.5)
        if emergency_cooling:
            thermal_dissipation_kw = round(base_thermal * 0.75, 1)
            life_support_index = 100.0

            # Fixed missing multiplication operator (-)
            radiation_absorption_msv = round(0.12 * (warp_index / 7.0), 3)
        else:
            thermal_dissipation_kw = round(base_thermal, 1)

            # Fixed missing multiplication operators and subtraction (-)
            quantum_core_degradation = round(0.0008 * self.step_counter, 4)
            life_support_index = round(max(90.0, 100.0 - quantum_core_degradation), 2)
            radiation_absorption_msv = round(0.24 * (warp_index / 7.0), 3)

        radar_scans = [
            {"id": "DM-CLUSTER-09", "type": "Dark Matter", "bearing": "142°", "dist": "1.4 LY"},
            {"id": "BH-MICRO-02", "type": "Micro-Black Hole", "bearing": "285°", "dist": "3.8 LY"}
        ] if anomalies_detected > 0 else [{"id": "SECTOR-CLEAR", "type": "Deep Space Vacuum", "bearing": "N/A", "dist": "0 LY"}]

        return {
            "status": "ADVANCED_INTERSTELLAR_SYNCHRONIZED",
            "step": self.step_counter,
            "fleet_size": fleet_size,
            "formation": formation,
            "metrics": {
                "mesh_sync_phase": round(sync_phase_deg, 2),
                "fleet_avg_warp": round(sum(v["warp_factor"] for v in fleet_vessels) / fleet_size, 2),
                "overall_mesh_integrity": round(sum(v["sync_health"] for v in fleet_vessels) / fleet_size, 2),

                # Fixed missing multiplication operator (-)
                "antigravity_pressure_mpa": round(1.24 * warp_index * (1.5 if antigravity_repulsion else 0.5), 2),

                "entanglement_fidelity_percent": entanglement_fidelity,
                "packet_loss_percent": packet_loss_percent,
                "sync_matrix_status": sync_matrix_status,
                "qetb_mesh_bandwidth_gbps": qetb_mesh_bandwidth,
                "bubble_overlap_density_mw": bubble_overlap_density,
                "interference_index": interference_index,
                "route_efficiency_percent": route_efficiency,
                "navigation_status": pathfinding_status,
                "thermal_dissipation_kw": thermal_dissipation_kw,
                "life_support_index": life_support_index,
                "radiation_absorption_msv": radiation_absorption_msv
            },
            "fleet_nodes": fleet_vessels,
            "radar_scans": radar_scans
        }