from tools.postgres_tools import (
    get_machine_events,
    get_machine_alarms,
    get_latest_event,
    get_latest_alarm,
)


def main():

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - POSTGRESQL TOOL TEST")
    print("=" * 60)

    machine_id = "MACHINE_001"

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    print()
    print("Reading machine events...")

    events = get_machine_events(
        machine_id=machine_id,
        limit=10,
    )

    print()
    print(f"Events received: {len(events)}")

    for event in events:

        print()
        print(
            f"[{event['event_type']}]"
        )

        print(
            f"Time    : {event['timestamp']}"
        )

        print(
            f"Message : {event['message']}"
        )

    # --------------------------------------------------
    # ALARMS
    # --------------------------------------------------

    print()
    print("-" * 60)

    print()
    print("Reading machine alarms...")

    alarms = get_machine_alarms(
        machine_id=machine_id,
        limit=10,
    )

    print()
    print(f"Alarms received: {len(alarms)}")

    for alarm in alarms:

        print()

        print(
            f"[{alarm['severity']}] "
            f"{alarm['code']}"
        )

        print(
            f"Time    : {alarm['timestamp']}"
        )

        print(
            f"Message : {alarm['message']}"
        )

        print(
            f"Ack     : {alarm['acknowledged']}"
        )

    # --------------------------------------------------
    # LATEST EVENT
    # --------------------------------------------------

    print()
    print("-" * 60)

    latest_event = get_latest_event(
        machine_id
    )

    print()
    print("Latest event:")

    if latest_event:

        print(
            latest_event
        )

    else:

        print(
            "No event found."
        )

    # --------------------------------------------------
    # LATEST ALARM
    # --------------------------------------------------

    print()
    print("Latest alarm:")

    latest_alarm = get_latest_alarm(
        machine_id
    )

    if latest_alarm:

        print(
            latest_alarm
        )

    else:

        print(
            "No alarm found."
        )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()