from tools.evidence_tools import (
    get_machine_evidence,
)

from agents.diagnostic_agent import (
    DiagnosticAgent,
)

from intelligence.reasoning.reasoning_engine import (
    ReasoningEngine,
)


def main():

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - REASONING ENGINE TEST")
    print("=" * 60)

    machine_id = "MACHINE_001"

    # --------------------------------------------------
    # BUILD EVIDENCE
    # --------------------------------------------------

    print()
    print("Collecting evidence...")

    evidence = get_machine_evidence(
        machine_id=machine_id,
        minutes=10,
    )

    # --------------------------------------------------
    # DIAGNOSTIC AGENT
    # --------------------------------------------------

    print(
        "Running Diagnostic Agent..."
    )

    diagnostic_agent = DiagnosticAgent()

    diagnostic_result = (
        diagnostic_agent.analyze(
            evidence
        )
    )

    # --------------------------------------------------
    # REASONING ENGINE
    # --------------------------------------------------

    print(
        "Running Reasoning Engine..."
    )

    reasoning_engine = ReasoningEngine()

    result = reasoning_engine.reason(
        diagnostic_result,
        evidence,
    )

    # --------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------

    print()
    print(
        f"Machine : {result.machine_id}"
    )

    print(
        f"State   : {result.machine_state}"
    )

    print()

    print(
        "Primary Hypothesis"
    )

    print("-" * 60)

    print(
        result.primary_hypothesis
    )

    print()

    print(
        "Reasoning Summary"
    )

    print("-" * 60)

    print(
        result.reasoning_summary
    )

    print()

    print(
        "Detailed Reasoning"
    )

    print("-" * 60)

    for index, hypothesis in enumerate(
        result.hypotheses,
        start=1,
    ):

        print()

        print(
            f"Hypothesis {index}: "
            f"{hypothesis.cause}"
        )

        print(
            f"Confidence: "
            f"{hypothesis.confidence}"
        )

        print()

        print(
            "Supporting Evidence:"
        )

        for item in (
            hypothesis.supporting_evidence
        ):

            print(
                f"  + {item}"
            )

        print()

        print(
            "Contradictory Evidence:"
        )

        for item in (
            hypothesis.contradictory_evidence
        ):

            print(
                f"  - {item}"
            )

        print()

        print(
            "Missing Evidence:"
        )

        for item in (
            hypothesis.missing_evidence
        ):

            print(
                f"  ? {item}"
            )

        print()

        print(
            "Recommended Checks:"
        )

        for item in (
            hypothesis.recommended_checks
        ):

            print(
                f"  → {item}"
            )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()