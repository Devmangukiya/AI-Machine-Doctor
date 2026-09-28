"""
PostgreSQL writer for AI Machine Doctor.

Stores machine events and alarms received from MQTT.
"""

import json
import os
from uuid import UUID

import pg8000
from dotenv import load_dotenv


load_dotenv()


class PostgreSQLWriter:

    def __init__(self):

        self.host = os.getenv(
            "POSTGRES_HOST",
            "localhost",
        )

        self.port = int(
            os.getenv(
                "POSTGRES_PORT",
                "5432",
            )
        )

        self.database = os.getenv(
            "POSTGRES_DB",
            "ai_machine_doctor",
        )

        self.user = os.getenv(
            "POSTGRES_USER",
            "postgres",
        )

        self.password = os.getenv(
            "POSTGRES_PASSWORD",
        )

        self.connection = None

    # ========================================================
    # CONNECT
    # ========================================================

    def connect(self):

        self.connection = pg8000.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )

        print(
            "[POSTGRES] Connected successfully."
        )

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        if self.connection:

            self.connection.close()

            print(
                "[POSTGRES] Connection closed."
            )

    # ========================================================
    # MACHINE
    # ========================================================

    def ensure_machine(
        self,
        machine_id: str,
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO machines (
                machine_id,
                machine_name,
                machine_type,
                plant_id,
                status
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (machine_id)
            DO NOTHING;
            """,
            (
                machine_id,
                machine_id,
                "MOTOR_DRIVEN_MACHINE",
                "PLANT_001",
                "UNKNOWN",
            ),
        )

        self.connection.commit()

        cursor.close()

    # ========================================================
    # EVENT
    # ========================================================

    def write_event(
        self,
        event: dict,
    ):

        machine_id = event["machine_id"]

        self.ensure_machine(
            machine_id
        )

        cursor = self.connection.cursor()

        event_id = event["event_id"]

        cursor.execute(
            """
            INSERT INTO machine_events (
                event_id,
                machine_id,
                event_type,
                message,
                timestamp,
                metadata
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (event_id)
            DO NOTHING;
            """,
            (
                UUID(event_id),
                machine_id,
                event["event_type"],
                event["message"],
                event["timestamp"],
                json.dumps(
                    event.get(
                        "metadata",
                        {}
                    )
                ),
            ),
        )

        self.connection.commit()

        cursor.close()

        print(
            f"[POSTGRES] Stored event "
            f"{event['event_type']} "
            f"from {machine_id}"
        )

    # ========================================================
    # ALARM
    # ========================================================

    def write_alarm(
        self,
        alarm: dict,
    ):

        machine_id = alarm["machine_id"]

        self.ensure_machine(
            machine_id
        )

        cursor = self.connection.cursor()

        alarm_id = alarm["alarm_id"]

        cursor.execute(
            """
            INSERT INTO machine_alarms (
                alarm_id,
                machine_id,
                code,
                severity,
                message,
                timestamp,
                acknowledged,
                acknowledged_by,
                acknowledged_at
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (alarm_id)
            DO NOTHING;
            """,
            (
                UUID(alarm_id),
                machine_id,
                alarm["code"],
                alarm["severity"],
                alarm["message"],
                alarm["timestamp"],
                alarm.get(
                    "acknowledged",
                    False
                ),
                alarm.get(
                    "acknowledged_by"
                ),
                alarm.get(
                    "acknowledged_at"
                ),
            ),
        )

        self.connection.commit()

        cursor.close()

        print(
            f"[POSTGRES] Stored alarm "
            f"{alarm['code']} "
            f"({alarm['severity']}) "
            f"from {machine_id}"
        )