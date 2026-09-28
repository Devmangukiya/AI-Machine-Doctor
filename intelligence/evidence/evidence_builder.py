"""
Machine Doctor - Evidence Builder

Combines machine intelligence outputs into a single
structured evidence object.

This layer does NOT diagnose the machine.

It collects:
    - machine state
    - telemetry
    - anomalies
    - alarms
    - events
    - health
    - OEE

The future Reasoning Engine will use this evidence
to form and evaluate hypotheses.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceItem:
    """
    One piece of machine evidence.
    """

    source: str

    category: str

    severity: str

    message: str

    data: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class MachineEvidence:
    """
    Complete evidence package for one machine.
    """

    machine_id: str

    timestamp: str

    machine_state: str

    telemetry: dict[str, Any]

    findings: list[EvidenceItem]

    summary: dict[str, Any]


class EvidenceBuilder:
    """
    Builds a unified evidence package.
    """

    def build(
        self,
        machine_id: str,
        timestamp: str,
        machine_state: str,
        telemetry: dict[str, Any],
        anomalies: list[Any] | None = None,
        alarms: list[Any] | None = None,
        events: list[Any] | None = None,
        health: Any | None = None,
        oee: Any | None = None,
    ) -> MachineEvidence:

        evidence_items = []

        # ====================================================
        # 1. Anomaly findings
        # ====================================================

        if anomalies:

            for anomaly in anomalies:

                evidence_items.append(
                    EvidenceItem(

                        source="anomaly_detector",

                        category="ANOMALY",

                        severity=anomaly.severity,

                        message=anomaly.message,

                        data={
                            "parameter":
                                anomaly.parameter,

                            "value":
                                anomaly.value,

                            "baseline":
                                anomaly.mean_value,

                            "z_score":
                                anomaly.z_score,
                        },
                    )
                )

        # ====================================================
        # 2. Alarms
        # ====================================================

        if alarms:
            for alarm in alarms:

                severity = getattr(
                    alarm,
                    "severity",
                    None,
                )

                if severity is None:
                    severity = alarm.get(
                        "severity",
                        "WARNING",
                    )

                message = getattr(
                    alarm,
                    "message",
                    None,
                )

                if message is None:
                    message = alarm.get(
                        "message",
                        "Machine alarm detected.",
                    )

                code = getattr(
                    alarm,
                    "code",
                    None,
                )

                if code is None:
                    code = alarm.get(
                        "code"
                    )

                acknowledged = getattr(
                    alarm,
                    "acknowledged",
                    None,
                )

                if acknowledged is None:
                    acknowledged = alarm.get(
                        "acknowledged",
                        False,
                    )

                evidence_items.append(
                    EvidenceItem(
                        source="alarm_system",
                        category="ALARM",
                        severity=severity,
                        message=message,
                        data={
                            "code": code,
                            "acknowledged": acknowledged,
                        },
                    )
                )
        # ====================================================
        # 3. Events
        # ====================================================

        if events:
            for event in events:

                message = getattr(
                    event,
                    "message",
                    None,
                )

                if message is None:
                    message = event.get(
                        "message",
                        "Machine event detected.",
                    )

                event_type = getattr(
                    event,
                    "event_type",
                    None,
                )

                if event_type is None:
                    event_type = event.get(
                        "event_type"
                    )

                evidence_items.append(
                    EvidenceItem(
                        source="event_system",
                        category="EVENT",
                        severity="INFO",
                        message=message,
                        data={
                            "event_type": event_type,
                        },
                    )
                )
        # ====================================================
        # 4. Health
        # ====================================================

        health_summary = {}

        if health is not None:

            health_summary = {

                "score": getattr(
                    health,
                    "score",
                    None,
                ),

                "status": getattr(
                    health,
                    "status",
                    None,
                ),

                "critical_findings":
                    getattr(
                        health,
                        "critical_findings",
                        0,
                    ),

                "warning_findings":
                    getattr(
                        health,
                        "warning_findings",
                        0,
                    ),

                "message": getattr(
                    health,
                    "message",
                    None,
                ),
            }

            evidence_items.append(
                EvidenceItem(

                    source="health_engine",

                    category="HEALTH",

                    severity=(
                        "CRITICAL"
                        if health_summary[
                            "status"
                        ] == "CRITICAL"
                        else "INFO"
                    ),

                    message=(
                        health_summary[
                            "message"
                        ]
                        or "Health calculated."
                    ),

                    data=health_summary,
                )
            )

        # ====================================================
        # 5. OEE
        # ====================================================

        oee_summary = {}

        if oee is not None:

            oee_summary = {

                "availability":
                    getattr(
                        oee,
                        "availability",
                        None,
                    ),

                "performance":
                    getattr(
                        oee,
                        "performance",
                        None,
                    ),

                "quality":
                    getattr(
                        oee,
                        "quality",
                        None,
                    ),

                "oee":
                    getattr(
                        oee,
                        "oee",
                        None,
                    ),
            }

            evidence_items.append(
                EvidenceItem(

                    source="oee_engine",

                    category="OEE",

                    severity="INFO",

                    message=(
                        "OEE calculation available."
                    ),

                    data=oee_summary,
                )
            )

        # ====================================================
        # 6. Summary
        # ====================================================

        critical_count = sum(
            1
            for item in evidence_items
            if item.severity == "CRITICAL"
        )

        warning_count = sum(
            1
            for item in evidence_items
            if item.severity == "WARNING"
        )

        summary = {

            "total_evidence":
                len(evidence_items),

            "critical_findings":
                critical_count,

            "warning_findings":
                warning_count,

            "machine_state":
                machine_state,

            "health":
                health_summary,

            "oee":
                oee_summary,
        }

        # ====================================================
        # 7. Final evidence object
        # ====================================================

        return MachineEvidence(

            machine_id=machine_id,

            timestamp=timestamp,

            machine_state=machine_state,

            telemetry=telemetry,

            findings=evidence_items,

            summary=summary,
        )