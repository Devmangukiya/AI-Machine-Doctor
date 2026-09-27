"""
Simulation scenario engine.

The machine intentionally moves through:

NORMAL → DEGRADATION → FAULT → RECOVERY → NORMAL
"""

from enum import Enum

from .config import (
    NORMAL_DURATION_TICKS,
    DEGRADATION_DURATION_TICKS,
    FAULT_DURATION_TICKS,
    RECOVERY_DURATION_TICKS,
)


class Scenario(str, Enum):
    NORMAL = "NORMAL"
    DEGRADATION = "DEGRADATION"
    FAULT = "FAULT"
    RECOVERY = "RECOVERY"


class ScenarioEngine:

    def __init__(self):
        self.current_scenario = Scenario.NORMAL
        self.tick = 0

    def update(self) -> Scenario:
        """
        Advance the simulation by one tick.
        """

        self.tick += 1

        if self.current_scenario == Scenario.NORMAL:

            if self.tick > NORMAL_DURATION_TICKS:
                self.current_scenario = Scenario.DEGRADATION
                self.tick = 1

        elif self.current_scenario == Scenario.DEGRADATION:

            if self.tick > DEGRADATION_DURATION_TICKS:
                self.current_scenario = Scenario.FAULT
                self.tick = 1

        elif self.current_scenario == Scenario.FAULT:

            if self.tick > FAULT_DURATION_TICKS:
                self.current_scenario = Scenario.RECOVERY
                self.tick = 1

        elif self.current_scenario == Scenario.RECOVERY:

            if self.tick > RECOVERY_DURATION_TICKS:
                self.current_scenario = Scenario.NORMAL
                self.tick = 1

        return self.current_scenario

    def get_degradation_level(self) -> float:
        """
        Returns a normalized degradation value.

        0.0 = healthy
        1.0 = severe degradation
        """

        if self.current_scenario == Scenario.NORMAL:
            return 0.0

        if self.current_scenario == Scenario.DEGRADATION:

            progress = self.tick / DEGRADATION_DURATION_TICKS

            return min(1.0, progress)

        if self.current_scenario == Scenario.FAULT:
            return 1.0

        if self.current_scenario == Scenario.RECOVERY:

            progress = self.tick / RECOVERY_DURATION_TICKS

            return max(0.0, 1.0 - progress)

        return 0.0