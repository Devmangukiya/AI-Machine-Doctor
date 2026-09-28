"""
Machine Doctor - Machine Health Engine

Converts rule findings into an overall machine health score.
"""

from dataclasses import dataclass

from intelligence.rules.rule_engine import RuleFinding


@dataclass
class HealthResult:
    """
    Overall health result for a machine.
    """

    score: float

    status: str

    critical_findings: int

    warning_findings: int

    message: str


class HealthEngine:
    """
    Calculates machine health from rule findings.
    """

    def calculate(
        self,
        findings: list[RuleFinding],
    ) -> HealthResult:

        score = 100.0

        critical_count = 0
        warning_count = 0

        # ----------------------------------------------------
        # Apply penalties
        # ----------------------------------------------------

        for finding in findings:

            if finding.severity == "CRITICAL":

                critical_count += 1

                score -= 25

            elif finding.severity == "WARNING":

                warning_count += 1

                score -= 10

        # ----------------------------------------------------
        # Keep score between 0 and 100
        # ----------------------------------------------------

        score = max(
            0.0,
            min(100.0, score)
        )

        # ----------------------------------------------------
        # Determine health status
        # ----------------------------------------------------

        if score >= 90:

            status = "HEALTHY"

            message = (
                "Machine is operating within "
                "normal health limits."
            )

        elif score >= 70:

            status = "WARNING"

            message = (
                "Machine shows some abnormal "
                "conditions and should be monitored."
            )

        elif score >= 40:

            status = "DEGRADED"

            message = (
                "Machine health is degraded. "
                "Investigation is recommended."
            )

        else:

            status = "CRITICAL"

            message = (
                "Machine health is critical. "
                "Immediate investigation is recommended."
            )

        return HealthResult(
            score=score,
            status=status,
            critical_findings=critical_count,
            warning_findings=warning_count,
            message=message,
        )