"""
Machine telemetry parameter configuration.

Defines how each parameter should be interpreted
by Machine Doctor.
"""


PARAMETER_TYPES = {

    # --------------------------------------------------------
    # Instantaneous sensor values
    # --------------------------------------------------------

    "rpm": "instantaneous",

    "current_a": "instantaneous",

    "temperature_c": "instantaneous",

    "vibration_mm_s": "instantaneous",

    "frequency_hz": "instantaneous",

    "pressure_bar": "instantaneous",

    "flow_l_min": "instantaneous",

    "speed_rpm": "instantaneous",

    "setpoint_rpm": "instantaneous",

    "cycle_time_s": "instantaneous",

    # --------------------------------------------------------
    # Cumulative counters
    # --------------------------------------------------------

    "good_count": "counter",

    "reject_count": "counter",
}