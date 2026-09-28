"""
Machine Doctor - Diagnostic Agent

The Diagnostic Agent analyzes MachineEvidence and produces
structured diagnostic hypotheses.

This first version is deterministic.

Later, an LLM will be placed above/beside this layer to:
- understand operator questions
- select tools
- interpret the diagnostic result
- explain findings naturally
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DiagnosticHypothesis:
    cause: str
    confidence: str
    supporting_evidence: list[str] = field(
        default_factory=list
    )
    missing_evidence: list[str] = field(
        default_factory=list
    )
    recommended_checks: list[str] = field(
        default_factory=list
    )


@dataclass
class DiagnosticResult:
    machine_id: str
    machine_state: str
    observations: list[str]
    hypotheses: list[DiagnosticHypothesis]
    critical_findings: int
    warning_findings: int


class DiagnosticAgent:

    def analyze(
        self,
        evidence: Any,
    ) -> DiagnosticResult:
        """
        Analyze MachineEvidence.

        The agent does not directly access databases.

        It receives structured evidence and reasons over it.
        """

        observations = []

        hypotheses = []

        # --------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------

        machine_id = evidence.machine_id
        machine_state = evidence.machine_state

        critical_count = evidence.summary.get(
            "critical_findings",
            0,
        )

        warning_count = evidence.summary.get(
            "warning_findings",
            0,
        )

        # --------------------------------------------------
        # EXTRACT EVIDENCE
        # --------------------------------------------------

        anomaly_parameters = []

        alarm_codes = []

        event_types = []

        for item in evidence.findings:

            # -------------------------------
            # ANOMALY
            # -------------------------------

            if item.category == "ANOMALY":

                parameter = item.data.get(
                    "parameter"
                )

                if parameter:

                    anomaly_parameters.append(
                        parameter
                    )

                observations.append(
                    item.message
                )

            # -------------------------------
            # ALARM
            # -------------------------------

            elif item.category == "ALARM":

                code = item.data.get(
                    "code"
                )

                if code:

                    alarm_codes.append(
                        code
                    )

                observations.append(
                    item.message
                )

            # -------------------------------
            # EVENT
            # -------------------------------

            elif item.category == "EVENT":

                event_type = item.data.get(
                    "event_type"
                )

                if event_type:

                    event_types.append(
                        event_type
                    )

                observations.append(
                    item.message
                )

        # --------------------------------------------------
        # DIAGNOSTIC RULE 1
        # MOTOR OVERLOAD
        # --------------------------------------------------

        overload_detected = (
            "MOTOR_OVERLOAD"
            in alarm_codes
            or "current_a"
            in anomaly_parameters
        )

        if overload_detected:

            supporting = []

            if "MOTOR_OVERLOAD" in alarm_codes:

                supporting.append(
                    "Motor overload alarm detected."
                )

            if "current_a" in anomaly_parameters:

                supporting.append(
                    "Motor current is outside its expected range."
                )

            hypotheses.append(
                DiagnosticHypothesis(

                    cause=(
                        "Motor overload or excessive mechanical load"
                    ),

                    confidence="MEDIUM",

                    supporting_evidence=supporting,

                    missing_evidence=[
                        "Motor drive fault information",
                        "Mechanical load condition",
                        "Recent maintenance history",
                    ],

                    recommended_checks=[
                        "Check motor load.",
                        "Check for mechanical obstruction.",
                        "Check VFD/drive diagnostics.",
                        "Inspect recent maintenance records.",
                    ],
                )
            )

        # --------------------------------------------------
        # DIAGNOSTIC RULE 2
        # HIGH TEMPERATURE
        # --------------------------------------------------

        temperature_detected = (
            "temperature_c"
            in anomaly_parameters
            or "HIGH_MOTOR_TEMPERATURE"
            in alarm_codes
        )

        if temperature_detected:

            supporting = []

            if (
                "temperature_c"
                in anomaly_parameters
            ):

                supporting.append(
                    "Motor temperature is above the configured limit."
                )

            if (
                "HIGH_MOTOR_TEMPERATURE"
                in alarm_codes
            ):

                supporting.append(
                    "High motor temperature alarm detected."
                )

            hypotheses.append(
                DiagnosticHypothesis(

                    cause=(
                        "Motor overheating"
                    ),

                    confidence="MEDIUM",

                    supporting_evidence=supporting,

                    missing_evidence=[
                        "Motor cooling condition",
                        "Ambient temperature",
                        "Motor load history",
                    ],

                    recommended_checks=[
                        "Check motor cooling.",
                        "Check motor load.",
                        "Check ventilation.",
                        "Inspect motor temperature trend.",
                    ],
                )
            )

        # --------------------------------------------------
        # DIAGNOSTIC RULE 3
        # HIGH VIBRATION
        # --------------------------------------------------

        vibration_detected = (
            "vibration_mm_s"
            in anomaly_parameters
            or "HIGH_VIBRATION"
            in alarm_codes
        )

        if vibration_detected:

            supporting = []

            if (
                "vibration_mm_s"
                in anomaly_parameters
            ):

                supporting.append(
                    "Machine vibration is above the configured limit."
                )

            if (
                "HIGH_VIBRATION"
                in alarm_codes
            ):

                supporting.append(
                    "High vibration alarm detected."
                )

            hypotheses.append(
                DiagnosticHypothesis(

                    cause=(
                        "Mechanical vibration or rotating-component issue"
                    ),

                    confidence="MEDIUM",

                    supporting_evidence=supporting,

                    missing_evidence=[
                        "Bearing condition",
                        "Alignment information",
                        "Vibration frequency spectrum",
                    ],

                    recommended_checks=[
                        "Inspect bearings.",
                        "Check shaft/coupling alignment.",
                        "Inspect rotating components.",
                        "Review vibration trend.",
                    ],
                )
            )

        # --------------------------------------------------
        # DIAGNOSTIC RULE 4
        # HIGH CYCLE TIME
        # --------------------------------------------------

        cycle_detected = (
            "cycle_time_s"
            in anomaly_parameters
            or "HIGH_CYCLE_TIME"
            in alarm_codes
        )

        if cycle_detected:

            supporting = []

            if (
                "cycle_time_s"
                in anomaly_parameters
            ):

                supporting.append(
                    "Cycle time is above the configured limit."
                )

            if (
                "HIGH_CYCLE_TIME"
                in alarm_codes
            ):

                supporting.append(
                    "High cycle-time alarm detected."
                )

            hypotheses.append(
                DiagnosticHypothesis(

                    cause=(
                        "Production cycle degradation"
                    ),

                    confidence="MEDIUM",

                    supporting_evidence=supporting,

                    missing_evidence=[
                        "Production target",
                        "Operating mode",
                        "Production recipe/settings",
                    ],

                    recommended_checks=[
                        "Check machine operating conditions.",
                        "Check production settings.",
                        "Review cycle-time trend.",
                    ],
                )
            )

        return DiagnosticResult(

            machine_id=machine_id,

            machine_state=machine_state,

            observations=observations,

            hypotheses=hypotheses,

            critical_findings=critical_count,

            warning_findings=warning_count,
        )