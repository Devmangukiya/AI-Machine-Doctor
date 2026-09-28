"""
Machine Doctor - Machine Tools

High-level tools that combine information from
multiple Machine Doctor data sources.

These tools are designed for AI agents.
"""

from tools.influx_tools import (
    get_latest_telemetry,
)

from tools.postgres_tools import (
    get_latest_alarm,
    get_latest_event,
)


def get_machine_status(machine_id: str):
    """
    Get the current operational picture of a machine.

    Combines:

    - latest telemetry
    - latest alarm
    - latest event

    Returns:
        Structured machine status dictionary.
    """

    telemetry = get_latest_telemetry(
        machine_id
    )

    alarm = get_latest_alarm(
        machine_id
    )

    event = get_latest_event(
        machine_id
    )

    # -----------------------------------------
    # Determine machine state
    # -----------------------------------------

    machine_state = "UNKNOWN"

    if event:

        event_type = event.get(
            "event_type"
        )

        if event_type == "MACHINE_FAULT":
            machine_state = "FAULT"

        elif event_type == "MACHINE_RECOVERY":
            machine_state = "RECOVERY"

        elif event_type == "MACHINE_NORMAL":
            machine_state = "NORMAL"

        elif event_type == "SCENARIO_CHANGE":

            message = event.get(
                "message",
                ""
            )

            if "FAULT" in message:
                machine_state = "FAULT"

            elif "RECOVERY" in message:
                machine_state = "RECOVERY"

            elif "NORMAL" in message:
                machine_state = "NORMAL"

    # -----------------------------------------
    # Determine alarm severity
    # -----------------------------------------

    alarm_severity = None

    if alarm:

        alarm_severity = alarm.get(
            "severity"
        )

    # -----------------------------------------
    # Return combined machine status
    # -----------------------------------------

    return {
        "machine_id": machine_id,

        "machine_state": machine_state,

        "telemetry": telemetry,

        "latest_alarm": alarm,

        "latest_event": event,

        "alarm_severity": alarm_severity,
    }