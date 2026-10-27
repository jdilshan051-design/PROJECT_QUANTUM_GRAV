import pytest
from core.physics_engine import QuantumGravPhysicsEngine

def test_physics_engine_output():
    engine = QuantumGravPhysicsEngine()
    results = engine.compute_flight_metrics(mach_speed=5.0, field_voltage_mv=500.0, warp_bubble_density=4.0)
    
    assert "Mach_Speed" in results
    assert results["Mach_Speed"] == 5.0
    assert results["Drag_Reduction_Percent"] > 80.0
    assert results["Relativistic_Time_Dilation"]["Lorentz_Gamma"] >= 1.0

def test_time_dilation():
    engine = QuantumGravPhysicsEngine()
    time_data = engine.calculate_relativistic_time_dilation(velocity_mach=10.0, warp_bubble_density=5.0)
    
    assert time_data["Lorentz_Gamma"] > 1.0
    assert time_data["Cockpit_Drift_ms"] > 0.0