from schemas.telemetry import (
    MachineTelemetry,
    MotorTelemetry,
    VFDTelemetry,
    ProcessTelemetry,
    ProductionTelemetry,
)

from intelligence.rules.rule_engine import RuleEngine
from intelligence.health.health_engine import HealthEngine


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

    # --------------------------------------------------------
    # Rule Engine
    # --------------------------------------------------------

    rule_engine = RuleEngine()

    findings = rule_engine.evaluate(
        telemetry
    )

    # --------------------------------------------------------
    # Health Engine
    # --------------------------------------------------------

    health_engine = HealthEngine()

    result = health_engine.calculate(
        findings
    )

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("       MACHINE DOCTOR - HEALTH ENGINE")
    print("=" * 60)

    print()

    print(
        f"Machine          : {telemetry.machine_id}"
    )

    print(
        f"Health Score     : {result.score:.1f} / 100"
    )

    print(
        f"Health Status    : {result.status}"
    )

    print(
        f"Critical Issues  : {result.critical_findings}"
    )

    print(
        f"Warning Issues   : {result.warning_findings}"
    )

    print()

    print(
        f"Message          : {result.message}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()