"""
Machine Doctor - InfluxDB Tools

Tools used by AI agents to retrieve machine telemetry.

Important:
Agents should NOT directly access InfluxDB.
They should call these controlled tools.
"""

import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient

load_dotenv()

INFLUXDB_URL = os.getenv(
    "INFLUXDB_URL",
    "http://localhost:8086"
)

INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")

INFLUXDB_ORG = os.getenv(
    "INFLUXDB_ORG",
    "Dense Technology"
)

INFLUXDB_BUCKET = os.getenv(
    "INFLUXDB_BUCKET",
    "machine_doctor_telemetry"
)


def get_client():
    """
    Create an InfluxDB client.
    """

    return InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG,
    )


def get_machine_telemetry(
    machine_id: str,
    minutes: int = 10,
):
    """
    Retrieve recent telemetry for a machine.

    Args:
        machine_id:
            Machine identifier.

        minutes:
            Number of historical minutes to retrieve.

    Returns:
        List of telemetry records.
    """

    client = get_client()

    try:

        query_api = client.query_api()

        query = f"""
        from(bucket: "{INFLUXDB_BUCKET}")
            |> range(start: -{minutes}m)
            |> filter(
                fn: (r) =>
                    r._measurement == "machine_telemetry"
                    and r.machine_id == "{machine_id}"
            )
            |> pivot(
                rowKey: ["_time"],
                columnKey: ["_field"],
                valueColumn: "_value"
            )
            |> sort(columns: ["_time"])
        """

        tables = query_api.query(
            query=query,
            org=INFLUXDB_ORG,
        )

        telemetry = []

        for table in tables:

            for record in table.records:

                values = record.values

                telemetry.append(
                    {
                        "timestamp": str(
                            values.get("_time")
                        ),
                        "machine_id": values.get(
                            "machine_id"
                        ),
                        "rpm": values.get("rpm"),
                        "current_a": values.get(
                            "current_a"
                        ),
                        "temperature_c": values.get(
                            "temperature_c"
                        ),
                        "vibration_mm_s": values.get(
                            "vibration_mm_s"
                        ),
                        "frequency_hz": values.get(
                            "frequency_hz"
                        ),
                        "pressure_bar": values.get(
                            "pressure_bar"
                        ),
                        "flow_l_min": values.get(
                            "flow_l_min"
                        ),
                        "speed_rpm": values.get(
                            "speed_rpm"
                        ),
                        "setpoint_rpm": values.get(
                            "setpoint_rpm"
                        ),
                        "cycle_time_s": values.get(
                            "cycle_time_s"
                        ),
                        "good_count": values.get(
                            "good_count"
                        ),
                        "reject_count": values.get(
                            "reject_count"
                        ),
                    }
                )

        return telemetry

    finally:

        client.close()


def get_latest_telemetry(machine_id: str):
    """
    Get the latest telemetry record for a machine.
    """

    records = get_machine_telemetry(
        machine_id=machine_id,
        minutes=10,
    )

    if not records:
        return None

    return records[-1]