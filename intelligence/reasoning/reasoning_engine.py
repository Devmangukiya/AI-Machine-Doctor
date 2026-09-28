"""
Machine Doctor - Reasoning Engine

Evaluates diagnostic hypotheses against machine evidence.

Important:
The reasoning engine does not invent evidence.
It evaluates evidence already collected by Machine Doctor.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReasonedHypothesis:

    cause: str

    confidence: str

    score: int

    supporting_evidence: list[str] = field(
        default_factory=list
    )

    contradictory_evidence: list[str] = field(
        default_factory=list
    )

    missing_evidence: list[str] = field(
        default_factory=list
    )

    recommended_checks: list[str] = field(
        default_factory=list
    )


@dataclass
class ReasoningResult:

    machine_id: str

    machine_state: str

    primary_hypothesis: str | None

    hypotheses: list[ReasonedHypothesis]

    reasoning_summary: str


class ReasoningEngine:

    def reason(
        self,
        diagnostic_result: Any,
        evidence: Any,
    ) -> ReasoningResult:

        reasoned_hypotheses = []

        machine_id = (
            diagnostic_result.machine_id
        )

        machine_state = (
            diagnostic_result.machine_state
        )

        # --------------------------------------------------
        # Evaluate every diagnostic hypothesis
        # --------------------------------------------------

        for hypothesis in diagnostic_result.hypotheses:

            supporting = list(
                hypothesis.supporting_evidence
            )

            contradictory = []

            missing = list(
                hypothesis.missing_evidence
            )

            # Start with a score based on actual
            # supporting evidence.
            score = len(supporting)

            # --------------------------------------------------
            # Machine state is contextual evidence.
            #
            # It should NOT automatically count as proof
            # of the root cause.
            # --------------------------------------------------

            if machine_state == "FAULT":

                supporting.append(
                    "Machine is currently in FAULT state."
                )

            elif machine_state == "RECOVERY":

                supporting.append(
                    "Machine is currently in RECOVERY state."
                )

            elif machine_state == "NORMAL":

                supporting.append(
                    "Machine is currently in NORMAL state."
                )

            # --------------------------------------------------
            # Detect whether evidence contains critical
            # engineering findings.
            # --------------------------------------------------

            critical_evidence = 0

            anomaly_evidence = 0
            alarm_evidence = 0

            for item in evidence.findings:

                if item.category == "ANOMALY":

                    anomaly_evidence += 1

                    if item.severity == "CRITICAL":
                        critical_evidence += 1

                elif item.category == "ALARM":

                    alarm_evidence += 1

                    if item.severity == "CRITICAL":
                        critical_evidence += 1

            # --------------------------------------------------
            # Evidence weighting
            # --------------------------------------------------

            # Actual anomaly + alarm evidence provides
            # stronger support than machine state alone.

            if anomaly_evidence > 0:
                score += 2

            if alarm_evidence > 0:
                score += 2

            if critical_evidence > 0:
                score += 2

            # --------------------------------------------------
            # Confidence calculation
            # --------------------------------------------------

            if score >= 6:

                confidence = "HIGH"

            elif score >= 3:

                confidence = "MEDIUM"

            else:

                confidence = "LOW"

            # --------------------------------------------------
            # Contradictory state
            # --------------------------------------------------

            if machine_state == "NORMAL":

                contradictory.append(
                    "Machine is currently reporting NORMAL state."
                )

            # --------------------------------------------------
            # Build reasoned hypothesis
            # --------------------------------------------------

            reasoned_hypotheses.append(
                ReasonedHypothesis(

                    cause=hypothesis.cause,

                    confidence=confidence,

                    score=score,

                    supporting_evidence=supporting,

                    contradictory_evidence=contradictory,

                    missing_evidence=missing,

                    recommended_checks=list(
                        hypothesis.recommended_checks
                    ),
                )
            )

        # --------------------------------------------------
        # Sort hypotheses by score
        # --------------------------------------------------

        reasoned_hypotheses.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        # --------------------------------------------------
        # Select primary hypothesis
        # --------------------------------------------------

        primary_hypothesis = None

        if reasoned_hypotheses:

            primary_hypothesis = (
                reasoned_hypotheses[0].cause
            )

        # --------------------------------------------------
        # Build reasoning summary
        # --------------------------------------------------

        if reasoned_hypotheses:

            primary = reasoned_hypotheses[0]

            reasoning_summary = (
                f"The strongest current hypothesis is "
                f"'{primary.cause}' with "
                f"{primary.confidence} confidence "
                f"based on the available evidence. "
                f"Further verification is required before "
                f"treating this hypothesis as a confirmed root cause."
            )

        else:

            reasoning_summary = (
                "Insufficient evidence to generate "
                "a diagnostic hypothesis."
            )

        return ReasoningResult(

            machine_id=machine_id,

            machine_state=machine_state,

            primary_hypothesis=primary_hypothesis,

            hypotheses=reasoned_hypotheses,

            reasoning_summary=reasoning_summary,
        )