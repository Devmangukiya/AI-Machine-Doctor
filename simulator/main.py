"""
Entry point for the AI Machine Doctor virtual machine.
"""

import json
import time

from .config import SIMULATION_INTERVAL_SECONDS
from .machine import VirtualMachine


def main():

    machine = VirtualMachine(seed=42)

    print()
    print("=" * 60)
    print("        AI MACHINE DOCTOR - MACHINE SIMULATOR")
    print("=" * 60)
    print()
    print(f"Machine ID   : {machine.machine_id}")
    print(f"Machine Type : {machine.machine_type}")
    print(f"Plant ID     : {machine.plant_id}")
    print()
    print("Simulation lifecycle:")
    print("NORMAL → DEGRADATION → FAULT → RECOVERY → NORMAL")
    print()
    print("Press CTRL+C to stop.")
    print("=" * 60)
    print()

    try:

        while True:

            telemetry = machine.generate_telemetry()

            print(
                json.dumps(
                    telemetry.model_dump(),
                    indent=2,
                    default=str,
                )
            )

            print("-" * 60)

            time.sleep(SIMULATION_INTERVAL_SECONDS)

    except KeyboardInterrupt:

        print()
        print("Simulation stopped.")


if __name__ == "__main__":
    main()