"""
Machine Doctor - Evidence Tool

High-level tool that gathers machine data and converts it
into structured MachineEvidence.

This is the bridge between the data/tool layer and
the future AI Agent layer.
"""

from datetime import datetime, timezone

from tools.machine_tools import get_machine_status
from data.influx_reader import get_telemetry_history

from intelligence.anomaly.anomaly_detector import (
    AnomalyDetector,
)

from intelligence.evidence.evidence_builder import (
    EvidenceBuilder,
)


def get_machine_evidence(
    machine_id: str,
    minutes: int = 10,
):
    """
    Build structured evidence for a machine.

    Steps:

    1. Get current machine status.
    2. Read historical telemetry.
    3. Run anomaly detection.
    4. Build MachineEvidence.

    Returns:
        MachineEvidence
    """

    # -----------------------------------------
    # 1. MACHINE STATUS
    # -----------------------------------------

    machine_status = get_machine_status(
        machine_id
    )

    # -----------------------------------------
    # 2. TELEMETRY HISTORY
    # -----------------------------------------

    telemetry_history = get_telemetry_history(
        machine_id=machine_id,
        minutes=minutes,
    )

    # -----------------------------------------
    # 3. ANOMALY DETECTION
    # -----------------------------------------

    detector = AnomalyDetector()

    anomalies = detector.detect(
        telemetry_history
    )

    # -----------------------------------------
    # 4. CURRENT TELEMETRY
    # -----------------------------------------

    current_telemetry = (
        machine_status.get("telemetry")
        or {}
    )

    # -----------------------------------------
    # 5. ALARM
    # -----------------------------------------

    alarms = []

    latest_alarm = machine_status.get(
        "latest_alarm"
    )

    if latest_alarm:

        alarms.append(
            latest_alarm
        )

    # -----------------------------------------
    # 6. EVENT
    # -----------------------------------------

    events = []

    latest_event = machine_status.get(
        "latest_event"
    )

    if latest_event:

        events.append(
            latest_event
        )

    # -----------------------------------------
    # 7. BUILD EVIDENCE
    # -----------------------------------------

    builder = EvidenceBuilder()

    evidence = builder.build(
        machine_id=machine_id,

        timestamp=datetime.now(
            timezone.utc
        ).isoformat(),

        machine_state=machine_status.get(
            "machine_state",
            "UNKNOWN",
        ),

        telemetry=current_telemetry,

        anomalies=anomalies,

        alarms=alarms,

        events=events,
    )

    return evidence