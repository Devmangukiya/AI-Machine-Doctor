from intelligence.anomaly.anomaly_detector import (
    AnomalyDetector,
)


def main():

    detector = AnomalyDetector()

    # --------------------------------------------------------
    # Simulated historical machine behavior
    # --------------------------------------------------------

    telemetry_history = {

        "temperature_c": [
            60.1,
            60.4,
            59.8,
            60.5,
            60.2,
            60.7,
            60.3,
            60.6,
            61.0,
            72.0,
        ],

        "current_a": [
            6.2,
            6.3,
            6.1,
            6.4,
            6.2,
            6.3,
            6.4,
            6.2,
            6.3,
            9.5,
        ],

        "vibration_mm_s": [
            1.9,
            2.0,
            2.1,
            1.8,
            2.0,
            2.1,
            1.9,
            2.0,
            2.1,
            5.5,
        ],

        "rpm": [
            1445,
            1450,
            1448,
            1452,
            1447,
            1451,
            1449,
            1450,
            1448,
            1300,
        ],
    }

    # --------------------------------------------------------
    # Run detector
    # --------------------------------------------------------

    findings = detector.detect(
        telemetry_history
    )

    print()
    print("=" * 60)
    print("       MACHINE DOCTOR - ANOMALY DETECTION")
    print("=" * 60)

    print()

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
                f"  Current value : "
                f"{finding.value:.2f}"
            )

            print(
                f"  Baseline      : "
                f"{finding.mean_value:.2f}"
            )

            print(
                f"  Std deviation : "
                f"{finding.standard_deviation:.2f}"
            )

            print(
                f"  Z-score       : "
                f"{finding.z_score:.2f}"
            )

            print(
                f"  Message       : "
                f"{finding.message}"
            )

            print(
                "-" * 60
            )


if __name__ == "__main__":
    main()