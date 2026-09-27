"""
Configuration for the virtual industrial machine.
"""

# -------------------------------------------------------------------
# Machine identity
# -------------------------------------------------------------------

MACHINE_ID = "MACHINE_001"
MACHINE_TYPE = "MOTOR_DRIVEN_MACHINE"
PLANT_ID = "PLANT_001"


# -------------------------------------------------------------------
# Simulation
# -------------------------------------------------------------------

SIMULATION_INTERVAL_SECONDS = 1.0

# Number of simulation ticks spent in each scenario
NORMAL_DURATION_TICKS = 20
DEGRADATION_DURATION_TICKS = 20
FAULT_DURATION_TICKS = 10
RECOVERY_DURATION_TICKS = 15


# -------------------------------------------------------------------
# Normal operating values
# -------------------------------------------------------------------

NORMAL_RPM = 1450.0
NORMAL_CURRENT = 6.5
NORMAL_TEMPERATURE = 60.0
NORMAL_VIBRATION = 2.0

NORMAL_PRESSURE = 5.0
NORMAL_FLOW = 100.0

NORMAL_FREQUENCY = 50.0
NORMAL_CYCLE_TIME = 4.2


# -------------------------------------------------------------------
# Machine limits / alarm thresholds
# -------------------------------------------------------------------

HIGH_CURRENT_THRESHOLD = 8.5
OVERLOAD_CURRENT_THRESHOLD = 9.0

HIGH_TEMPERATURE_THRESHOLD = 75.0
CRITICAL_TEMPERATURE_THRESHOLD = 85.0

HIGH_VIBRATION_THRESHOLD = 4.0
CRITICAL_VIBRATION_THRESHOLD = 5.0

HIGH_CYCLE_TIME_THRESHOLD = 5.0


# -------------------------------------------------------------------
# Production
# -------------------------------------------------------------------

GOOD_PART_PROBABILITY = 0.98

DEGRADED_GOOD_PART_PROBABILITY = 0.90