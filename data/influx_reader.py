"""
Read historical machine telemetry from InfluxDB.
"""

import os

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient


load_dotenv()


INFLUXDB_URL = os.getenv(
    "INFLUXDB_URL",
    "http://localhost:8086",
)

INFLUXDB_TOKEN = os.getenv(
    "INFLUXDB_TOKEN"
)

INFLUXDB_ORG = os.getenv(
    "INFLUXDB_ORG",
    "Dense Technology",
)

INFLUXDB_BUCKET = os.getenv(
    "INFLUXDB_BUCKET",
    "machine_doctor_telemetry",
)


# ============================================================
# InfluxDB Client
# ============================================================

def get_client():

    return InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG,
    )


# ============================================================
# Read Telemetry History
# ============================================================

def get_telemetry_history(
    machine_id: str,
    minutes: int = 10,
):
    """
    Read historical telemetry for a machine.

    Returns:

        {
            "rpm": [...],
            "current_a": [...],
            "temperature_c": [...],
            "vibration_mm_s": [...],
            "frequency_hz": [...],
            "pressure_bar": [...],
            "flow_l_min": [...],
            "speed_rpm": [...],
            "setpoint_rpm": [...],
            "good_count": [...],
            "reject_count": [...],
            "cycle_time_s": [...]
        }
    """

    client = get_client()

    try:

        query_api = client.query_api()

        # ----------------------------------------------------
        # Flux query
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Execute query
        # ----------------------------------------------------

        tables = query_api.query(
            query=query,
            org=INFLUXDB_ORG,
        )

        # ----------------------------------------------------
        # Complete telemetry history
        # ----------------------------------------------------

        history = {

            # Motor
            "rpm": [],
            "current_a": [],
            "temperature_c": [],
            "vibration_mm_s": [],

            # VFD
            "frequency_hz": [],

            # Process
            "pressure_bar": [],
            "flow_l_min": [],
            "speed_rpm": [],
            "setpoint_rpm": [],

            # Production
            "good_count": [],
            "reject_count": [],
            "cycle_time_s": [],
        }

        # ----------------------------------------------------
        # Process records
        # ----------------------------------------------------

        for table in tables:

            for record in table.records:

                values = record.values

                for parameter in history:

                    value = values.get(parameter)

                    if value is not None:

                        try:

                            history[parameter].append(
                                float(value)
                            )

                        except (
                            TypeError,
                            ValueError,
                        ):

                            pass

        return history

    finally:

        client.close()