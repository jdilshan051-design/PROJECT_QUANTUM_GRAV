import numpy as np

class QuantumGravPhysicsEngine:
    def __init__(self):
        # Physical constants (scaled for hypersonic & theoretical warp simulation)
        self.c = 299792458.05  # Speed of light (m/s)
        self.hypersonic_ref_speed = 343.0  # Speed of sound at sea level (m/s)

    def calculate_relativistic_time_dilation(self, mach_speed: float, warp_bubble_density: float) -> dict:
        """
        High-accuracy calculation of Lorentz Gamma factor and microsecond time slip
        incorporating Alcubierre warp metric suppression coefficients.
        """
        v = mach_speed * self.hypersonic_ref_speed
        # Effective velocity scaled by warp density reduction
        v_effective = v * max(0.001, (1.0 - (warp_bubble_density * 0.095)))
        
        beta = v_effective / self.c
        # Prevent division by zero or imaginary numbers at extreme limits
        beta = min(beta, 0.999999999)
        
        lorentz_gamma = 1.0 / np.sqrt(1.0 - (beta ** 2))
        
        # High-precision microsecond time slip calculation per second elapsed
        time_slip_us = (lorentz_gamma - 1.0) * 1_000_000.0 * 0.001
        cockpit_drift_ms = time_slip_us * 0.001 * warp_bubble_density

        return {
            "Lorentz_Gamma": round(lorentz_gamma, 6),
            "Time_Slip_Microseconds": round(time_slip_us, 5),
            "Cockpit_Drift_ms": round(cockpit_drift_ms, 4)
        }

    def compute_flight_metrics(self, mach_speed: float, field_voltage_mv: float, warp_bubble_density: float) -> dict:
        """
        Computes sensitive hypersonic and quantum gravimetric metrics.
        """
        # Highly sensitive non-linear drag suppression based on field voltage and warp density
        voltage_factor = min(1.0, field_voltage_mv / 1000.0)
        density_factor = min(1.0, warp_bubble_density / 10.0)
        
        drag_reduction = 95.0 + (4.99 * (voltage_factor * density_factor))
        drag_reduction = min(99.999, max(0.0, drag_reduction))

        # Sonic boom attenuation in decibels (scaled exponentially for sensitivity)
        base_db = 120.0
        attenuation = (field_voltage_mv * 0.08) + (warp_bubble_density * 4.5)
        sonic_boom_db = max(3.5, base_db - attenuation)

        # Warp Metric Tensor T00 (Negative energy density index)
        t00_index = -(warp_bubble_density ** 2) * (field_voltage_mv / 50.0) * 0.1618
        metric_distortion = round(warp_bubble_density * (field_voltage_mv / 100.0) * 0.155, 4)

        rel_time = self.calculate_relativistic_time_dilation(mach_speed, warp_bubble_density)

        return {
            "Mach_Speed": round(mach_speed, 2),
            "Field_Voltage_MV": round(field_voltage_mv, 2),
            "Warp_Bubble_Density": round(warp_bubble_density, 2),
            "Drag_Reduction_Percent": round(drag_reduction, 4),
            "Sonic_Boom_Level_dB": round(sonic_boom_db, 2),
            "Warp_Metrics": {
                "Negative_Energy_Index_T00": round(t00_index, 4),
                "Metric_Distortion_Factor": metric_distortion
            },
            "Relativistic_Time_Dilation": rel_time
        }