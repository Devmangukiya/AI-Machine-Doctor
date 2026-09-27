"""
Compatibility layer for the simulator.

The canonical schemas live in the schemas/ package.
"""

from schemas.alarms import MachineAlarm
from schemas.events import MachineEvent

from schemas.telemetry import (
    MachineTelemetry,
    MotorTelemetry,
    VFDTelemetry,
    ProcessTelemetry,
    ProductionTelemetry,
)


# ------------------------------------------------------------
# Compatibility aliases
# ------------------------------------------------------------
#
# The simulator currently uses the older names.
# These aliases allow the simulator to keep working while
# the canonical schemas use the new standardized names.
#

Alarm = MachineAlarm

MotorData = MotorTelemetry

VFDData = VFDTelemetry

ProcessData = ProcessTelemetry

ProductionData = ProductionTelemetry


__all__ = [
    "MachineTelemetry",
    "MotorTelemetry",
    "VFDTelemetry",
    "ProcessTelemetry",
    "ProductionTelemetry",
    "MachineEvent",
    "MachineAlarm",

    # Compatibility names
    "Alarm",
    "MotorData",
    "VFDData",
    "ProcessData",
    "ProductionData",
]