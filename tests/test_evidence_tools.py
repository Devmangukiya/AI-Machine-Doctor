from tools.evidence_tools import (
    get_machine_evidence,
)


def main():

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - EVIDENCE TOOL TEST")
    print("=" * 60)

    machine_id = "MACHINE_001"

    print()
    print(
        f"Building evidence for {machine_id}..."
    )

    evidence = get_machine_evidence(
        machine_id=machine_id,
        minutes=10,
    )

    print()

    print(
        f"Machine ID : {evidence.machine_id}"
    )

    print(
        f"State      : {evidence.machine_state}"
    )

    print()

    print("Evidence Findings")
    print("-" * 60)

    for item in evidence.findings:

        print(
            f"[{item.severity}] "
            f"{item.category}"
        )

        print(
            f"Source  : {item.source}"
        )

        print(
            f"Message : {item.message}"
        )

        print()

    print("-" * 60)

    print("Evidence Summary")
    print()

    print(
        f"Total evidence : "
        f"{evidence.summary['total_evidence']}"
    )

    print(
        f"Critical       : "
        f"{evidence.summary['critical_findings']}"
    )

    print(
        f"Warnings       : "
        f"{evidence.summary['warning_findings']}"
    )

    print()

    print("=" * 60)


if __name__ == "__main__":
    main()