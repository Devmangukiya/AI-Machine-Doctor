from schemas.telemetry import (
    MachineTelemetry,
    MotorTelemetry,
    VFDTelemetry,
    ProcessTelemetry,
    ProductionTelemetry,
)

from intelligence.rules.rule_engine import RuleEngine


def create_test_telemetry():

    return MachineTelemetry(
        machine_id="MACHINE_001",
        state="FAULT",

        motor=MotorTelemetry(
            rpm=1350,
            current_a=9.8,
            temperature_c=90,
            vibration_mm_s=5.5,
        ),

        vfd=VFDTelemetry(
            frequency_hz=0,
            status="FAULT",
            fault_code="F3001",
        ),

        process=ProcessTelemetry(
            pressure_bar=5.2,
            flow_l_min=85,
            speed_rpm=1350,
            setpoint_rpm=1450,
        ),

        production=ProductionTelemetry(
            good_count=100,
            reject_count=10,
            cycle_time_s=6.0,
        ),
    )


def main():

    telemetry = create_test_telemetry()

    engine = RuleEngine()

    findings = engine.evaluate(telemetry)

    print()
    print("=" * 60)
    print("       MACHINE DOCTOR - RULE ENGINE")
    print("=" * 60)

    print(f"\nMachine : {telemetry.machine_id}")
    print(f"State   : {telemetry.state}")

    print()

    if not findings:

        print("No abnormal conditions detected.")

    else:

        print(
            f"Detected {len(findings)} finding(s):"
        )

        print()

        for finding in findings:

            print(
                f"[{finding.severity}] "
                f"{finding.rule_id}"
            )

            print(
                f"  Parameter : {finding.parameter}"
            )

            print(
                f"  Value     : {finding.value}"
            )

            print(
                f"  Threshold : {finding.threshold}"
            )

            print(
                f"  Message   : {finding.message}"
            )

            print("-" * 60)


if __name__ == "__main__":
    main()