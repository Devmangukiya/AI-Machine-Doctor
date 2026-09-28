from tools.influx_tools import (
    get_machine_telemetry,
    get_latest_telemetry,
)


def main():

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - INFLUXDB TOOL TEST")
    print("=" * 60)

    machine_id = "MACHINE_001"

    print()
    print(f"Reading telemetry for {machine_id}...")

    records = get_machine_telemetry(
        machine_id=machine_id,
        minutes=10,
    )

    print()
    print(f"Records received: {len(records)}")

    if records:

        print()
        print("Latest telemetry:")
        print("-" * 60)

        latest = records[-1]

        for key, value in latest.items():

            print(
                f"{key:20} : {value}"
            )

    print()
    print("Testing latest telemetry function...")

    latest = get_latest_telemetry(
        machine_id
    )

    print()

    if latest:

        print("Latest record retrieved successfully.")

    else:

        print("No telemetry found.")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()