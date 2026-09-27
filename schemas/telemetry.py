"""
Canonical telemetry schema for AI Machine Doctor.

This defines the standard format in which machine telemetry
is represented throughout the entire system.
"""

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


# ------------------------------------------------------------
# Machine State
# ------------------------------------------------------------

MachineState = Literal[
    "RUNNING",
    "IDLE",
    "STOPPED",
    "FAULT",
    "MAINTENANCE",
]


# ------------------------------------------------------------
# Motor Telemetry
# ------------------------------------------------------------

class MotorTelemetry(BaseModel):
    rpm: float = Field(ge=0)

    current_a: float = Field(ge=0)

    temperature_c: float

    vibration_mm_s: float = Field(ge=0)


# ------------------------------------------------------------
# VFD Telemetry
# ------------------------------------------------------------

class VFDTelemetry(BaseModel):
    frequency_hz: float = Field(ge=0)

    status: str

    fault_code: str | None = None


# ------------------------------------------------------------
# Process Telemetry
# ------------------------------------------------------------

class ProcessTelemetry(BaseModel):
    pressure_bar: float = Field(ge=0)

    flow_l_min: float = Field(ge=0)

    speed_rpm: float = Field(ge=0)

    setpoint_rpm: float = Field(ge=0)


# ------------------------------------------------------------
# Production Telemetry
# ------------------------------------------------------------

class ProductionTelemetry(BaseModel):
    good_count: int = Field(ge=0)

    reject_count: int = Field(ge=0)

    cycle_time_s: float = Field(gt=0)


# ------------------------------------------------------------
# Complete Machine Telemetry
# ------------------------------------------------------------

class MachineTelemetry(BaseModel):
    """
    Standard telemetry message used throughout
    the AI Machine Doctor platform.
    """

    schema_version: str = "1.0"

    machine_id: str

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    state: MachineState

    motor: MotorTelemetry

    vfd: VFDTelemetry

    process: ProcessTelemetry

    production: ProductionTelemetry