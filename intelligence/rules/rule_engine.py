"""
Machine Doctor - Rule Engine

Deterministic rules for detecting abnormal machine conditions.

This layer does NOT use AI/LLMs.
It converts machine telemetry into structured findings.
"""

from dataclasses import dataclass
from typing import List

from schemas.telemetry import MachineTelemetry


# ============================================================
# RULE THRESHOLDS
# ============================================================

HIGH_CURRENT_A = 8.0
CRITICAL_CURRENT_A = 9.5

HIGH_TEMPERATURE_C = 75.0
CRITICAL_TEMPERATURE_C = 85.0

HIGH_VIBRATION_MM_S = 4.0
CRITICAL_VIBRATION_MM_S = 5.0

HIGH_CYCLE_TIME_S = 5.0


# ============================================================
# RULE RESULT
# ============================================================

@dataclass
class RuleFinding:
    """
    Result produced when a machine rule is triggered.
    """

    rule_id: str

    severity: str

    parameter: str

    value: float | str

    threshold: float | str

    message: str


# ============================================================
# RULE ENGINE
# ============================================================

class RuleEngine:
    """
    Evaluates machine telemetry using deterministic rules.
    """

    def evaluate(
        self,
        telemetry: MachineTelemetry,
    ) -> List[RuleFinding]:

        findings = []

        # ====================================================
        # MOTOR CURRENT
        # ====================================================

        current = telemetry.motor.current_a

        if current >= CRITICAL_CURRENT_A:

            findings.append(
                RuleFinding(
                    rule_id="MOTOR_CURRENT_CRITICAL",
                    severity="CRITICAL",
                    parameter="current_a",
                    value=current,
                    threshold=CRITICAL_CURRENT_A,
                    message=(
                        f"Motor current is critically high: "
                        f"{current:.2f} A"
                    ),
                )
            )

        elif current >= HIGH_CURRENT_A:

            findings.append(
                RuleFinding(
                    rule_id="MOTOR_CURRENT_HIGH",
                    severity="WARNING",
                    parameter="current_a",
                    value=current,
                    threshold=HIGH_CURRENT_A,
                    message=(
                        f"Motor current is high: "
                        f"{current:.2f} A"
                    ),
                )
            )

        # ====================================================
        # MOTOR TEMPERATURE
        # ====================================================

        temperature = telemetry.motor.temperature_c

        if temperature >= CRITICAL_TEMPERATURE_C:

            findings.append(
                RuleFinding(
                    rule_id="MOTOR_TEMPERATURE_CRITICAL",
                    severity="CRITICAL",
                    parameter="temperature_c",
                    value=temperature,
                    threshold=CRITICAL_TEMPERATURE_C,
                    message=(
                        f"Motor temperature is critically high: "
                        f"{temperature:.2f} °C"
                    ),
                )
            )

        elif temperature >= HIGH_TEMPERATURE_C:

            findings.append(
                RuleFinding(
                    rule_id="MOTOR_TEMPERATURE_HIGH",
                    severity="WARNING",
                    parameter="temperature_c",
                    value=temperature,
                    threshold=HIGH_TEMPERATURE_C,
                    message=(
                        f"Motor temperature is high: "
                        f"{temperature:.2f} °C"
                    ),
                )
            )

        # ====================================================
        # VIBRATION
        # ====================================================

        vibration = telemetry.motor.vibration_mm_s

        if vibration >= CRITICAL_VIBRATION_MM_S:

            findings.append(
                RuleFinding(
                    rule_id="MOTOR_VIBRATION_CRITICAL",
                    severity="CRITICAL",
                    parameter="vibration_mm_s",
                    value=vibration,
                    threshold=CRITICAL_VIBRATION_MM_S,
                    message=(
                        f"Motor vibration is critically high: "
                        f"{vibration:.2f} mm/s"
                    ),
                )
            )

        elif vibration >= HIGH_VIBRATION_MM_S:

            findings.append(
                RuleFinding(
                    rule_id="MOTOR_VIBRATION_HIGH",
                    severity="WARNING",
                    parameter="vibration_mm_s",
                    value=vibration,
                    threshold=HIGH_VIBRATION_MM_S,
                    message=(
                        f"Motor vibration is high: "
                        f"{vibration:.2f} mm/s"
                    ),
                )
            )

        # ====================================================
        # CYCLE TIME
        # ====================================================

        cycle_time = telemetry.production.cycle_time_s

        if cycle_time >= HIGH_CYCLE_TIME_S:

            findings.append(
                RuleFinding(
                    rule_id="CYCLE_TIME_HIGH",
                    severity="WARNING",
                    parameter="cycle_time_s",
                    value=cycle_time,
                    threshold=HIGH_CYCLE_TIME_S,
                    message=(
                        f"Cycle time is high: "
                        f"{cycle_time:.2f} seconds"
                    ),
                )
            )

        # ====================================================
        # MACHINE STATE
        # ====================================================

        if telemetry.state == "FAULT":

            findings.append(
                RuleFinding(
                    rule_id="MACHINE_FAULT",
                    severity="CRITICAL",
                    parameter="state",
                    value=telemetry.state,
                    threshold="RUNNING",
                    message=(
                        "Machine is currently in FAULT state."
                    ),
                )
            )

        return findings