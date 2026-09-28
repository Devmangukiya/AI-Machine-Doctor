"""
Machine-specific engineering limits.

These values are currently simulator limits.
For a real machine, these should come from:
    - OEM specifications
    - PLC configuration
    - VFD configuration
    - machine commissioning data
    - maintenance engineering limits
"""


ENGINEERING_LIMITS = {

    # --------------------------------------------------------
    # Motor
    # --------------------------------------------------------

    "current_a": {
        "warning": 8.0,
        "critical": 9.0,
    },

    "temperature_c": {
        "warning": 75.0,
        "critical": 85.0,
    },

    "vibration_mm_s": {
        "warning": 3.5,
        "critical": 5.0,
    },

    # --------------------------------------------------------
    # VFD
    # --------------------------------------------------------

    "frequency_hz": {
        "warning_low": 5.0,
        "warning_high": 55.0,
        "critical_low": 0.0,
        "critical_high": 60.0,
    },

    # --------------------------------------------------------
    # Process
    # --------------------------------------------------------

    "pressure_bar": {
        "warning_low": 3.0,
        "warning_high": 7.0,
        "critical_low": 1.0,
        "critical_high": 8.0,
    },

    "flow_l_min": {
        "warning_low": 70.0,
        "warning_high": 130.0,
        "critical_low": 50.0,
        "critical_high": 150.0,
    },

    # --------------------------------------------------------
    # Speed
    # --------------------------------------------------------

    "speed_rpm": {
        "warning_low": 1200.0,
        "warning_high": 1600.0,
        "critical_low": 1000.0,
        "critical_high": 1700.0,
    },

    # --------------------------------------------------------
    # Production
    # --------------------------------------------------------

    "cycle_time_s": {
        "warning": 5.0,
        "critical": 6.0,
    },
}