"""
Virtual industrial machine.

This class simulates machine behavior and generates correlated
industrial telemetry.
"""

import random
from datetime import datetime, timezone

from .config import (
    MACHINE_ID,
    MACHINE_TYPE,
    PLANT_ID,
    NORMAL_RPM,
    NORMAL_CURRENT,
    NORMAL_TEMPERATURE,
    NORMAL_VIBRATION,
    NORMAL_PRESSURE,
    NORMAL_FLOW,
    NORMAL_FREQUENCY,
    NORMAL_CYCLE_TIME,
    HIGH_CURRENT_THRESHOLD,
    OVERLOAD_CURRENT_THRESHOLD,
    HIGH_TEMPERATURE_THRESHOLD,
    CRITICAL_TEMPERATURE_THRESHOLD,
    HIGH_VIBRATION_THRESHOLD,
    CRITICAL_VIBRATION_THRESHOLD,
    HIGH_CYCLE_TIME_THRESHOLD,
    GOOD_PART_PROBABILITY,
    DEGRADED_GOOD_PART_PROBABILITY,
)

from .models import (
    Alarm,
    MachineEvent,
    MachineTelemetry,
    MotorData,
    ProcessData,
    ProductionData,
    VFDData,
)

from .scenarios import Scenario, ScenarioEngine


class VirtualMachine:

    def __init__(self, seed: int = 42):

        # ------------------------------------------------------------
        # Machine identity
        # ------------------------------------------------------------

        self.machine_id = MACHINE_ID
        self.machine_type = MACHINE_TYPE
        self.plant_id = PLANT_ID

        # ------------------------------------------------------------
        # Random generator
        # ------------------------------------------------------------

        # Fixed seed makes simulation reproducible.
        self.random = random.Random(seed)

        # ------------------------------------------------------------
        # Scenario engine
        # ------------------------------------------------------------

        self.scenario_engine = ScenarioEngine()

        # ------------------------------------------------------------
        # Production counters
        # ------------------------------------------------------------

        self.good_count = 0
        self.reject_count = 0

        # ------------------------------------------------------------
        # Previous state
        # ------------------------------------------------------------

        self.previous_scenario = Scenario.NORMAL

    # ----------------------------------------------------------------
    # Utility
    # ----------------------------------------------------------------

    def noise(self, amount: float) -> float:
        """
        Generate small random sensor noise.
        """

        return self.random.uniform(-amount, amount)

    # ----------------------------------------------------------------
    # Production
    # ----------------------------------------------------------------

    def update_production(self, scenario: Scenario):

        if scenario == Scenario.FAULT:

            # Production stops during fault.
            return

        if scenario == Scenario.DEGRADATION:

            if self.random.random() < DEGRADED_GOOD_PART_PROBABILITY:
                self.good_count += 1
            else:
                self.reject_count += 1

            return

        if scenario == Scenario.RECOVERY:

            if self.random.random() < GOOD_PART_PROBABILITY:
                self.good_count += 1
            else:
                self.reject_count += 1

            return

        # Normal operation

        if self.random.random() < GOOD_PART_PROBABILITY:
            self.good_count += 1
        else:
            self.reject_count += 1

    # ----------------------------------------------------------------
    # Alarm generation
    # ----------------------------------------------------------------

    def generate_alarms(
        self,
        current: float,
        temperature: float,
        vibration: float,
        cycle_time: float,
    ) -> list[Alarm]:

        alarms = []

        now = datetime.now(timezone.utc)

        if current >= HIGH_CURRENT_THRESHOLD:

            severity = (
                "CRITICAL"
                if current >= OVERLOAD_CURRENT_THRESHOLD
                else "WARNING"
            )

            alarms.append(
                Alarm(
                    machine_id=self.machine_id,
                    code="MOTOR_OVERLOAD",
                    severity=severity,
                    message=(
                        f"Motor current is high: "
                        f"{current:.2f} A"
                    ),
                    timestamp=now,
                )
            )

        if temperature >= HIGH_TEMPERATURE_THRESHOLD:

            severity = (
                "CRITICAL"
                if temperature >= CRITICAL_TEMPERATURE_THRESHOLD
                else "WARNING"
            )

            alarms.append(
                Alarm(
                    machine_id=self.machine_id,
                    code="HIGH_MOTOR_TEMPERATURE",
                    severity=severity,
                    message=(
                        f"Motor temperature is high: "
                        f"{temperature:.2f} °C"
                    ),
                    timestamp=now,
                )
            )

        if vibration >= HIGH_VIBRATION_THRESHOLD:

            severity = (
                "CRITICAL"
                if vibration >= CRITICAL_VIBRATION_THRESHOLD
                else "WARNING"
            )

            alarms.append(
                Alarm(
                    machine_id=self.machine_id,
                    code="HIGH_VIBRATION",
                    severity=severity,
                    message=(
                        f"Motor vibration is high: "
                        f"{vibration:.2f} mm/s"
                    ),
                    timestamp=now,
                )
            )

        if cycle_time >= HIGH_CYCLE_TIME_THRESHOLD:

            alarms.append(
                Alarm(
                    machine_id=self.machine_id,
                    code="HIGH_CYCLE_TIME",
                    severity="WARNING",
                    message=(
                        f"Cycle time increased to "
                        f"{cycle_time:.2f} seconds"
                    ),
                    timestamp=now,
                )
            )

        return alarms

    # ----------------------------------------------------------------
    # Event generation
    # ----------------------------------------------------------------

    def generate_events(
        self,
        scenario: Scenario,
    ) -> list[MachineEvent]:

        events = []

        if scenario != self.previous_scenario:

            now = datetime.now(timezone.utc)

            events.append(
                MachineEvent(
                    machine_id=self.machine_id,
                    event_type="SCENARIO_CHANGE",
                    message=(
                        f"Machine scenario changed from "
                        f"{self.previous_scenario.value} "
                        f"to {scenario.value}"
                    ),
                    timestamp=now,
                )
            )

            if scenario == Scenario.FAULT:

                events.append(
                    MachineEvent(
                        machine_id=self.machine_id,
                        event_type="MACHINE_FAULT",
                        message="Machine entered FAULT state.",
                        timestamp=now,
                    )
                )

            elif scenario == Scenario.RECOVERY:

                events.append(
                    MachineEvent(
                        machine_id=self.machine_id,
                        event_type="MACHINE_RECOVERY",
                        message="Machine entered recovery.",
                        timestamp=now,
                    )
                )

            elif scenario == Scenario.NORMAL:

                events.append(
                    MachineEvent(
                        machine_id=self.machine_id,
                        event_type="MACHINE_NORMAL",
                        message="Machine returned to normal operation.",
                        timestamp=now,
                    )
                )

        self.previous_scenario = scenario

        return events

    # ----------------------------------------------------------------
    # Telemetry generation
    # ----------------------------------------------------------------

    def generate_telemetry(self) -> MachineTelemetry:

        # Update scenario first.
        scenario = self.scenario_engine.update()

        degradation = self.scenario_engine.get_degradation_level()

        # ------------------------------------------------------------
        # Motor behavior
        # ------------------------------------------------------------

        rpm = (
            NORMAL_RPM
            - degradation * 120
            + self.noise(10)
        )

        current = (
            NORMAL_CURRENT
            + degradation * 3.2
            + self.noise(0.15)
        )

        temperature = (
            NORMAL_TEMPERATURE
            + degradation * 30
            + self.noise(0.8)
        )

        vibration = (
            NORMAL_VIBRATION
            + degradation * 3.5
            + self.noise(0.08)
        )

        # ------------------------------------------------------------
        # Process behavior
        # ------------------------------------------------------------

        pressure = (
            NORMAL_PRESSURE
            + degradation * 0.8
            + self.noise(0.05)
        )

        flow = (
            NORMAL_FLOW
            - degradation * 15
            + self.noise(1.0)
        )

        # ------------------------------------------------------------
        # Cycle time
        # ------------------------------------------------------------

        cycle_time = (
            NORMAL_CYCLE_TIME
            + degradation * 1.8
            + self.noise(0.05)
        )

        # ------------------------------------------------------------
        # Production
        # ------------------------------------------------------------

        self.update_production(scenario)

        # ------------------------------------------------------------
        # Alarms
        # ------------------------------------------------------------

        alarms = self.generate_alarms(
            current=current,
            temperature=temperature,
            vibration=vibration,
            cycle_time=cycle_time,
        )

        # ------------------------------------------------------------
        # Events
        # ------------------------------------------------------------

        events = self.generate_events(scenario)

        # ------------------------------------------------------------
        # Machine state
        # ------------------------------------------------------------

        if scenario == Scenario.FAULT:

            state = "FAULT"

            # During fault, VFD stops.
            vfd_status = "FAULT"
            frequency = 0.0
            fault_code = "F3001"

        elif scenario == Scenario.RECOVERY:

            state = "RUNNING"

            vfd_status = "RUNNING"
            frequency = NORMAL_FREQUENCY
            fault_code = None

        else:

            state = "RUNNING"

            vfd_status = "RUNNING"
            frequency = NORMAL_FREQUENCY
            fault_code = None

        # ------------------------------------------------------------
        # Return complete telemetry object
        # ------------------------------------------------------------

        return MachineTelemetry(

            machine_id=self.machine_id,

            machine_type=self.machine_type,

            plant_id=self.plant_id,

            timestamp=datetime.now(timezone.utc),

            state=state,

            scenario=scenario.value,

            motor=MotorData(
                rpm=max(0, rpm),
                current_a=max(0, current),
                temperature_c=temperature,
                vibration_mm_s=max(0, vibration),
            ),

            vfd=VFDData(
                frequency_hz=frequency,
                status=vfd_status,
                fault_code=fault_code,
            ),

            process=ProcessData(
                pressure_bar=max(0, pressure),
                flow_l_min=max(0, flow),
                speed_rpm=max(0, rpm),
                setpoint_rpm=NORMAL_RPM,
            ),

            production=ProductionData(
                good_count=self.good_count,
                reject_count=self.reject_count,
                cycle_time_s=cycle_time,
            ),

            active_alarms=alarms,

            events=events,
        )