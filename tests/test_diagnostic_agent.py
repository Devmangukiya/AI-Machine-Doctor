from tools.evidence_tools import (
    get_machine_evidence,
)

from agents.diagnostic_agent import (
    DiagnosticAgent,
)


def main():

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - DIAGNOSTIC AGENT TEST")
    print("=" * 60)

    machine_id = "MACHINE_001"

    # -----------------------------------------
    # BUILD EVIDENCE
    # -----------------------------------------

    print()
    print("Collecting machine evidence...")

    evidence = get_machine_evidence(
        machine_id=machine_id,
        minutes=10,
    )

    print(
        "Evidence collected."
    )

    # -----------------------------------------
    # RUN AGENT
    # -----------------------------------------

    agent = DiagnosticAgent()

    result = agent.analyze(
        evidence
    )

    # -----------------------------------------
    # DISPLAY RESULT
    # -----------------------------------------

    print()
    print(
        f"Machine : {result.machine_id}"
    )

    print(
        f"State   : {result.machine_state}"
    )

    print()

    print("Observations")
    print("-" * 60)

    for observation in result.observations:

        print(
            f"- {observation}"
        )

    print()

    print("Diagnostic Hypotheses")
    print("-" * 60)

    for index, hypothesis in enumerate(
        result.hypotheses,
        start=1,
    ):

        print()
        print(
            f"Hypothesis {index}"
        )

        print(
            f"Cause      : {hypothesis.cause}"
        )

        print(
            f"Confidence : {hypothesis.confidence}"
        )

        print()
        print(
            "Supporting Evidence:"
        )

        for item in (
            hypothesis.supporting_evidence
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
                f"  - {item}"
            )

        print()
        print(
            "Recommended Checks:"
        )

        for item in (
            hypothesis.recommended_checks
        ):

            print(
                f"  - {item}"
            )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()