from datetime import datetime, timezone

from intelligence.anomaly.anomaly_detector import (
    AnomalyDetector,
)

from intelligence.evidence.evidence_builder import (
    EvidenceBuilder,
)


def main():

    print()
    print("=" * 60)
    print("       MACHINE DOCTOR - EVIDENCE BUILDER")
    print("=" * 60)

    # --------------------------------------------------------
    # Simulated telemetry
    # --------------------------------------------------------

    telemetry = {

        "rpm": 1350,

        "current_a": 9.69,

        "temperature_c": 89.90,

        "vibration_mm_s": 5.53,

        "frequency_hz": 0.0,

        "pressure_bar": 5.2,

        "flow_l_min": 85.0,

        "speed_rpm": 1350,

        "setpoint_rpm": 1450,

        "cycle_time_s": 6.03,
    }

    # --------------------------------------------------------
    # Generate anomaly findings
    # --------------------------------------------------------

    detector = AnomalyDetector()

    history = {

        "current_a": [
            7.5,
            7.7,
            7.8,
            8.0,
            8.2,
            9.69,
        ],

        "temperature_c": [
            65,
            68,
            70,
            73,
            76,
            89.90,
        ],

        "vibration_mm_s": [
            2.0,
            2.2,
            2.5,
            3.0,
            3.5,
            5.53,
        ],

        "cycle_time_s": [
            4.2,
            4.4,
            4.6,
            4.8,
            5.0,
            6.03,
        ],
    }

    anomalies = detector.detect(
        history
    )

    # --------------------------------------------------------
    # Build evidence
    # --------------------------------------------------------

    builder = EvidenceBuilder()

    evidence = builder.build(

        machine_id="MACHINE_001",

        timestamp=(
            datetime.now(
                timezone.utc
            ).isoformat()
        ),

        machine_state="FAULT",

        telemetry=telemetry,

        anomalies=anomalies,
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print()

    print(
        f"Machine : "
        f"{evidence.machine_id}"
    )

    print(
        f"State   : "
        f"{evidence.machine_state}"
    )

    print()

    print(
        "Evidence Findings:"
    )

    print("-" * 60)

    for item in evidence.findings:

        print(
            f"[{item.severity}] "
            f"{item.category}"
        )

        print(
            f"Source  : "
            f"{item.source}"
        )

        print(
            f"Message : "
            f"{item.message}"
        )

        print("-" * 60)

    print()

    print(
        "Summary:"
    )

    print(
        f"Total evidence : "
        f"{evidence.summary['total_evidence']}"
    )

    print(
        f"Critical       : "
        f"{evidence.summary['critical_findings']}"
    )

    print(
        f"Warnings       : "
        f"{evidence.summary['warning_findings']}"
    )

    print()

    print("=" * 60)


if __name__ == "__main__":
    main()