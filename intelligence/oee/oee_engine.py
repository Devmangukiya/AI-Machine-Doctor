"""
Machine Doctor - OEE Engine

Calculates:
    Availability
    Performance
    Quality
    OEE
"""

from dataclasses import dataclass


@dataclass
class OEEInputs:
    """
    Inputs required for OEE calculation.
    """

    planned_production_time_s: float

    run_time_s: float

    ideal_cycle_time_s: float

    total_count: int

    good_count: int


@dataclass
class OEEResult:
    """
    OEE calculation result.
    """

    availability: float

    performance: float

    quality: float

    oee: float


class OEEEngine:
    """
    Calculates Overall Equipment Effectiveness.
    """

    def calculate(
        self,
        inputs: OEEInputs,
    ) -> OEEResult:

        # ----------------------------------------------------
        # Availability
        # ----------------------------------------------------

        if inputs.planned_production_time_s <= 0:

            availability = 0.0

        else:

            availability = (
                inputs.run_time_s
                / inputs.planned_production_time_s
            )

        # ----------------------------------------------------
        # Performance
        # ----------------------------------------------------

        if inputs.run_time_s <= 0:

            performance = 0.0

        else:

            performance = (
                inputs.ideal_cycle_time_s
                * inputs.total_count
            ) / inputs.run_time_s

        # ----------------------------------------------------
        # Quality
        # ----------------------------------------------------

        if inputs.total_count <= 0:

            quality = 0.0

        else:

            quality = (
                inputs.good_count
                / inputs.total_count
            )

        # ----------------------------------------------------
        # Clamp values
        # ----------------------------------------------------

        availability = max(
            0.0,
            min(1.0, availability)
        )

        performance = max(
            0.0,
            min(1.0, performance)
        )

        quality = max(
            0.0,
            min(1.0, quality)
        )

        # ----------------------------------------------------
        # OEE
        # ----------------------------------------------------

        oee = (
            availability
            * performance
            * quality
        )

        return OEEResult(
            availability=availability,
            performance=performance,
            quality=quality,
            oee=oee,
        )