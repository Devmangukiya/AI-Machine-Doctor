"""
Machine Doctor - Anomaly Detection

Hybrid anomaly detector:

1. Engineering threshold detection
2. Statistical Z-score detection

Parameter behavior is controlled by parameter_config.py.
"""

from dataclasses import dataclass
from statistics import mean, stdev

from intelligence.anomaly.parameter_config import (
    PARAMETER_TYPES,
)

from intelligence.rules.engineering_limits import (
    ENGINEERING_LIMITS,
)


@dataclass
class AnomalyFinding:
    """
    Represents an anomalous measurement.
    """

    parameter: str

    value: float

    mean_value: float

    standard_deviation: float

    z_score: float

    severity: str

    message: str


class AnomalyDetector:
    """
    Detects machine anomalies using:

        Engineering limits
        +
        Statistical Z-score

    Cumulative counters are handled separately.
    """

    def __init__(
        self,
        warning_z_score: float = 2.0,
        critical_z_score: float = 3.0,
    ):

        self.warning_z_score = (
            warning_z_score
        )

        self.critical_z_score = (
            critical_z_score
        )

    # ========================================================
    # Engineering threshold detection
    # ========================================================

    def check_engineering_limit(
        self,
        parameter: str,
        value: float,
        baseline: float,
    ) -> AnomalyFinding | None:

        limits = ENGINEERING_LIMITS.get(
            parameter
        )

        if limits is None:

            return None

        # ----------------------------------------------------
        # High-only parameters
        # ----------------------------------------------------

        if "critical" in limits:

            if value >= limits["critical"]:

                return AnomalyFinding(

                    parameter=parameter,

                    value=value,

                    mean_value=baseline,

                    standard_deviation=0.0,

                    z_score=0.0,

                    severity="CRITICAL",

                    message=(
                        f"{parameter} exceeded "
                        f"the critical engineering "
                        f"threshold. "
                        f"Current={value:.2f}, "
                        f"critical_threshold="
                        f"{limits['critical']:.2f}"
                    ),
                )

        if "warning" in limits:

            if value >= limits["warning"]:

                return AnomalyFinding(

                    parameter=parameter,

                    value=value,

                    mean_value=baseline,

                    standard_deviation=0.0,

                    z_score=0.0,

                    severity="WARNING",

                    message=(
                        f"{parameter} exceeded "
                        f"the warning engineering "
                        f"threshold. "
                        f"Current={value:.2f}, "
                        f"warning_threshold="
                        f"{limits['warning']:.2f}"
                    ),
                )

        # ----------------------------------------------------
        # Range-based parameters
        # ----------------------------------------------------

        if "critical_low" in limits:

            if value <= limits["critical_low"]:

                return AnomalyFinding(

                    parameter=parameter,

                    value=value,

                    mean_value=baseline,

                    standard_deviation=0.0,

                    z_score=0.0,

                    severity="CRITICAL",

                    message=(
                        f"{parameter} fell below "
                        f"the critical lower limit. "
                        f"Current={value:.2f}, "
                        f"critical_low="
                        f"{limits['critical_low']:.2f}"
                    ),
                )

        if "critical_high" in limits:

            if value >= limits["critical_high"]:

                return AnomalyFinding(

                    parameter=parameter,

                    value=value,

                    mean_value=baseline,

                    standard_deviation=0.0,

                    z_score=0.0,

                    severity="CRITICAL",

                    message=(
                        f"{parameter} exceeded "
                        f"the critical upper limit. "
                        f"Current={value:.2f}, "
                        f"critical_high="
                        f"{limits['critical_high']:.2f}"
                    ),
                )

        if "warning_low" in limits:

            if value <= limits["warning_low"]:

                return AnomalyFinding(

                    parameter=parameter,

                    value=value,

                    mean_value=baseline,

                    standard_deviation=0.0,

                    z_score=0.0,

                    severity="WARNING",

                    message=(
                        f"{parameter} fell below "
                        f"the warning lower limit. "
                        f"Current={value:.2f}, "
                        f"warning_low="
                        f"{limits['warning_low']:.2f}"
                    ),
                )

        if "warning_high" in limits:

            if value >= limits["warning_high"]:

                return AnomalyFinding(

                    parameter=parameter,

                    value=value,

                    mean_value=baseline,

                    standard_deviation=0.0,

                    z_score=0.0,

                    severity="WARNING",

                    message=(
                        f"{parameter} exceeded "
                        f"the warning upper limit. "
                        f"Current={value:.2f}, "
                        f"warning_high="
                        f"{limits['warning_high']:.2f}"
                    ),
                )

        return None

    # ========================================================
    # Statistical detection
    # ========================================================

    def check_statistical_anomaly(
        self,
        parameter: str,
        values: list[float],
    ) -> AnomalyFinding | None:

        if len(values) < 3:

            return None

        current_value = values[-1]

        historical_values = values[:-1]

        average = mean(
            historical_values
        )

        standard_deviation = stdev(
            historical_values
        )

        if standard_deviation == 0:

            return None

        z_score = (
            current_value - average
        ) / standard_deviation

        absolute_z = abs(
            z_score
        )

        if absolute_z >= self.critical_z_score:

            severity = "CRITICAL"

        elif absolute_z >= self.warning_z_score:

            severity = "WARNING"

        else:

            return None

        return AnomalyFinding(

            parameter=parameter,

            value=current_value,

            mean_value=average,

            standard_deviation=standard_deviation,

            z_score=z_score,

            severity=severity,

            message=(
                f"{parameter} is statistically "
                f"anomalous. "
                f"Current value="
                f"{current_value:.2f}, "
                f"baseline="
                f"{average:.2f}, "
                f"z-score="
                f"{z_score:.2f}"
            ),
        )

    # ========================================================
    # Counter detection
    # ========================================================

    def check_counter(
        self,
        parameter: str,
        values: list[float],
    ) -> AnomalyFinding | None:

        if len(values) < 2:

            return None

        previous = values[-2]

        current = values[-1]

        delta = (
            current - previous
        )

        # ----------------------------------------------------
        # Counters should normally increase.
        # A decrease indicates a reset or data issue.
        # ----------------------------------------------------

        if delta < 0:

            return AnomalyFinding(

                parameter=parameter,

                value=current,

                mean_value=previous,

                standard_deviation=0.0,

                z_score=0.0,

                severity="WARNING",

                message=(
                    f"{parameter} decreased "
                    f"unexpectedly. "
                    f"Previous={previous:.2f}, "
                    f"Current={current:.2f}. "
                    f"This may indicate a counter "
                    f"reset or data discontinuity."
                ),
            )

        return None

    # ========================================================
    # Main detection
    # ========================================================

    def detect(
        self,
        telemetry_history: dict[str, list[float]],
    ) -> list[AnomalyFinding]:

        findings = []

        for parameter, values in (
            telemetry_history.items()
        ):

            if not values:

                continue

            parameter_type = (
                PARAMETER_TYPES.get(
                    parameter,
                    "instantaneous",
                )
            )

            current_value = values[-1]

            # ------------------------------------------------
            # Counter
            # ------------------------------------------------

            if parameter_type == "counter":

                finding = self.check_counter(
                    parameter,
                    values,
                )

                if finding is not None:

                    findings.append(
                        finding
                    )

                continue

            # ------------------------------------------------
            # Instantaneous parameter
            # ------------------------------------------------

            baseline = (
                mean(values[:-1])
                if len(values) > 1
                else current_value
            )

            # ------------------------------------------------
            # Engineering limit
            # ------------------------------------------------

            engineering_finding = (
                self.check_engineering_limit(
                    parameter,
                    current_value,
                    baseline,
                )
            )

            if engineering_finding is not None:

                findings.append(
                    engineering_finding
                )

                # Engineering limits have priority.
                continue

            # ------------------------------------------------
            # Statistical anomaly
            # ------------------------------------------------

            statistical_finding = (
                self.check_statistical_anomaly(
                    parameter,
                    values,
                )
            )

            if statistical_finding is not None:

                findings.append(
                    statistical_finding
                )

        return findings