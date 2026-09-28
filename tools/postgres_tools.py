"""
Machine Doctor - PostgreSQL Tools

Controlled tools for retrieving machine events and alarms
from PostgreSQL.

Agents should use these functions instead of directly
accessing PostgreSQL.
"""

import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
    "5432",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "machine_doctor",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "postgres",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "",
)


def get_connection():
    """
    Create a PostgreSQL connection.
    """

    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def get_machine_events(
    machine_id: str,
    limit: int = 50,
):
    """
    Retrieve recent machine events.

    Returns:
        List of event dictionaries.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        query = """
        SELECT
            event_id,
            machine_id,
            event_type,
            message,
            timestamp,
            metadata
        FROM machine_events
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT %s;
        """

        cursor.execute(
            query,
            (machine_id, limit),
        )

        rows = cursor.fetchall()

        events = []

        for row in rows:

            events.append(
                {
                    "event_id": row[0],
                    "machine_id": row[1],
                    "event_type": row[2],
                    "message": row[3],
                    "timestamp": str(row[4]),
                    "metadata": row[5],
                }
            )

        cursor.close()

        return events

    finally:

        connection.close()


def get_machine_alarms(
    machine_id: str,
    limit: int = 50,
):
    """
    Retrieve recent machine alarms.

    Returns:
        List of alarm dictionaries.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        query = """
        SELECT
            alarm_id,
            machine_id,
            code,
            severity,
            message,
            timestamp,
            acknowledged,
            acknowledged_by,
            acknowledged_at
        FROM machine_alarms
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT %s;
        """

        cursor.execute(
            query,
            (machine_id, limit),
        )

        rows = cursor.fetchall()

        alarms = []

        for row in rows:

            alarms.append(
                {
                    "alarm_id": row[0],
                    "machine_id": row[1],
                    "code": row[2],
                    "severity": row[3],
                    "message": row[4],
                    "timestamp": str(row[5]),
                    "acknowledged": row[6],
                    "acknowledged_by": row[7],
                    "acknowledged_at": (
                        str(row[8])
                        if row[8] is not None
                        else None
                    ),
                }
            )

        cursor.close()

        return alarms

    finally:

        connection.close()


def get_latest_alarm(machine_id: str):
    """
    Retrieve the most recent alarm.
    """

    alarms = get_machine_alarms(
        machine_id=machine_id,
        limit=1,
    )

    if not alarms:
        return None

    return alarms[0]


def get_latest_event(machine_id: str):
    """
    Retrieve the most recent machine event.
    """

    events = get_machine_events(
        machine_id=machine_id,
        limit=1,
    )

    if not events:
        return None

    return events[0]