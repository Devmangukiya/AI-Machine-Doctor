from tools.machine_tools import (
    get_machine_status,
)


def main():

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - MACHINE TOOL TEST")
    print("=" * 60)

    machine_id = "MACHINE_001"

    print()
    print(
        f"Getting machine status for {machine_id}..."
    )

    status = get_machine_status(
        machine_id
    )

    print()

    print(
        f"Machine ID : {status['machine_id']}"
    )

    print(
        f"State      : {status['machine_state']}"
    )

    print()

    # -----------------------------------------
    # TELEMETRY
    # -----------------------------------------

    print("Latest Telemetry")
    print("-" * 60)

    telemetry = status["telemetry"]

    if telemetry:

        for key, value in telemetry.items():

            print(
                f"{key:20} : {value}"
            )

    else:

        print(
            "No telemetry available."
        )

    # -----------------------------------------
    # ALARM
    # -----------------------------------------

    print()
    print("Latest Alarm")
    print("-" * 60)

    alarm = status["latest_alarm"]

    if alarm:

        print(
            f"Code     : {alarm['code']}"
        )

        print(
            f"Severity : {alarm['severity']}"
        )

        print(
            f"Message  : {alarm['message']}"
        )

        print(
            f"Time     : {alarm['timestamp']}"
        )

    else:

        print(
            "No alarm available."
        )

    # -----------------------------------------
    # EVENT
    # -----------------------------------------

    print()
    print("Latest Event")
    print("-" * 60)

    event = status["latest_event"]

    if event:

        print(
            f"Type    : {event['event_type']}"
        )

        print(
            f"Message : {event['message']}"
        )

        print(
            f"Time    : {event['timestamp']}"
        )

    else:

        print(
            "No event available."
        )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()