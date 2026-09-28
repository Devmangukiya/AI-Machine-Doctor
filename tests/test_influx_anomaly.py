from data.influx_reader import get_telemetry_history

from intelligence.anomaly.anomaly_detector import (
    AnomalyDetector,
)


def main():

    machine_id = "MACHINE_001"

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - INFLUXDB ANOMALY DETECTION")
    print("=" * 60)

    print()

    print(
        f"Reading telemetry for {machine_id}..."
    )

    # --------------------------------------------------------
    # Read historical telemetry
    # --------------------------------------------------------

    history = get_telemetry_history(
        machine_id=machine_id,
        minutes=10,
    )

    print()

    for parameter, values in history.items():

        print(
            f"{parameter:20} : "
            f"{len(values)} samples"
        )

    # --------------------------------------------------------
    # Run anomaly detector
    # --------------------------------------------------------

    detector = AnomalyDetector()

    findings = detector.detect(
        history
    )

    print()

    print(
        "=" * 60
    )

    if not findings:

        print(
            "No anomalies detected."
        )

    else:

        print(
            f"Detected {len(findings)} anomaly/anomalies:"
        )

        print()

        for finding in findings:

            print(
                f"[{finding.severity}] "
                f"{finding.parameter}"
            )

            print(
                f"  Current     : "
                f"{finding.value:.2f}"
            )

            print(
                f"  Baseline    : "
                f"{finding.mean_value:.2f}"
            )

            print(
                f"  Z-score     : "
                f"{finding.z_score:.2f}"
            )

            print(
                f"  Message     : "
                f"{finding.message}"
            )

            print("-" * 60)

    print("=" * 60)


if __name__ == "__main__":
    main()