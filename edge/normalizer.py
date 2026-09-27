"""
Machine data normalization.

Converts raw machine data into the canonical
AI Machine Doctor telemetry schema.
"""

from schemas.telemetry import (
    MachineTelemetry,
    MotorTelemetry,
    VFDTelemetry,
    ProcessTelemetry,
    ProductionTelemetry,
)

from .models import RawMachineData


def normalize_machine_data(
    raw: RawMachineData,
) -> MachineTelemetry:

    telemetry = MachineTelemetry(

        machine_id=raw.machine_id,

        state=raw.state,

        motor=MotorTelemetry(
            rpm=raw.rpm,
            current_a=raw.current,
            temperature_c=raw.temperature,
            vibration_mm_s=raw.vibration,
        ),

        vfd=VFDTelemetry(
            frequency_hz=raw.frequency,

            status=(
                "FAULT"
                if raw.fault_code
                else "RUNNING"
            ),

            fault_code=raw.fault_code,
        ),

        process=ProcessTelemetry(
            pressure_bar=raw.pressure,
            flow_l_min=raw.flow,
            speed_rpm=raw.rpm,
            setpoint_rpm=1450.0,
        ),

        production=ProductionTelemetry(
            good_count=raw.good_count,
            reject_count=raw.reject_count,
            cycle_time_s=raw.cycle_time,
        ),
    )

    return telemetry