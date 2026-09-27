"""
MQTT → InfluxDB telemetry writer.

Receives machine telemetry from MQTT and stores
it in InfluxDB for historical analysis.
"""

import json
import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

INFLUXDB_URL = os.getenv(
    "INFLUXDB_URL"
)

INFLUXDB_TOKEN = os.getenv(
    "INFLUXDB_TOKEN"
)

INFLUXDB_ORG = os.getenv(
    "INFLUXDB_ORG"
)

INFLUXDB_BUCKET = os.getenv(
    "INFLUXDB_BUCKET"
)

MQTT_HOST = "localhost"
MQTT_PORT = 1883

MQTT_TOPIC = (
    "machine/+/telemetry"
)


# ============================================================
# Validate configuration
# ============================================================

required_variables = {
    "INFLUXDB_URL": INFLUXDB_URL,
    "INFLUXDB_TOKEN": INFLUXDB_TOKEN,
    "INFLUXDB_ORG": INFLUXDB_ORG,
    "INFLUXDB_BUCKET": INFLUXDB_BUCKET,
}

missing = [
    name
    for name, value
    in required_variables.items()
    if not value
]

if missing:

    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(missing)
    )


# ============================================================
# InfluxDB client
# ============================================================

influx_client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG,
)

write_api = influx_client.write_api(
    write_options=SYNCHRONOUS
)


# ============================================================
# MQTT callbacks
# ============================================================

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties=None,
):

    print()

    print("=" * 60)
    print("       MQTT → INFLUXDB WRITER")
    print("=" * 60)

    print(
        f"MQTT Broker : {MQTT_HOST}:{MQTT_PORT}"
    )

    print(
        f"InfluxDB    : {INFLUXDB_URL}"
    )

    print(
        f"Organization: {INFLUXDB_ORG}"
    )

    print(
        f"Bucket      : {INFLUXDB_BUCKET}"
    )

    print(
        f"MQTT Topic  : {MQTT_TOPIC}"
    )

    print("=" * 60)

    if reason_code == 0:

        print(
            "[MQTT] Connected successfully."
        )

        client.subscribe(
            MQTT_TOPIC
        )

        print(
            f"[MQTT] Subscribed to: "
            f"{MQTT_TOPIC}"
        )

    else:

        print(
            f"[MQTT] Connection failed: "
            f"{reason_code}"
        )


def on_message(
    client,
    userdata,
    message,
):

    try:

        # ----------------------------------------------------
        # Decode MQTT payload
        # ----------------------------------------------------

        payload = json.loads(
            message.payload.decode("utf-8")
        )

        machine_id = payload[
            "machine_id"
        ]

        timestamp = payload[
            "timestamp"
        ]

        state = payload.get(
            "state"
        )

        motor = payload.get(
            "motor",
            {}
        )

        vfd = payload.get(
            "vfd",
            {}
        )

        process = payload.get(
            "process",
            {}
        )

        production = payload.get(
            "production",
            {}
        )

        # ----------------------------------------------------
        # Create InfluxDB Point
        # ----------------------------------------------------

        point = (
            Point("machine_telemetry")

            # Tags
            .tag(
                "machine_id",
                machine_id,
            )

            .tag(
                "state",
                state or "UNKNOWN",
            )

            # Motor
            .field(
                "rpm",
                float(
                    motor.get(
                        "rpm",
                        0,
                    )
                ),
            )

            .field(
                "current_a",
                float(
                    motor.get(
                        "current_a",
                        0,
                    )
                ),
            )

            .field(
                "temperature_c",
                float(
                    motor.get(
                        "temperature_c",
                        0,
                    )
                ),
            )

            .field(
                "vibration_mm_s",
                float(
                    motor.get(
                        "vibration_mm_s",
                        0,
                    )
                ),
            )

            # VFD
            .field(
                "frequency_hz",
                float(
                    vfd.get(
                        "frequency_hz",
                        0,
                    )
                ),
            )

            # Process
            .field(
                "pressure_bar",
                float(
                    process.get(
                        "pressure_bar",
                        0,
                    )
                ),
            )

            .field(
                "flow_l_min",
                float(
                    process.get(
                        "flow_l_min",
                        0,
                    )
                ),
            )

            .field(
                "speed_rpm",
                float(
                    process.get(
                        "speed_rpm",
                        0,
                    )
                ),
            )

            .field(
                "setpoint_rpm",
                float(
                    process.get(
                        "setpoint_rpm",
                        0,
                    )
                ),
            )

            # Production
            .field(
                "good_count",
                int(
                    production.get(
                        "good_count",
                        0,
                    )
                ),
            )

            .field(
                "reject_count",
                int(
                    production.get(
                        "reject_count",
                        0,
                    )
                ),
            )

            .field(
                "cycle_time_s",
                float(
                    production.get(
                        "cycle_time_s",
                        0,
                    )
                ),
            )

            # Timestamp
            .time(timestamp)
        )

        # ----------------------------------------------------
        # Write to InfluxDB
        # ----------------------------------------------------

        write_api.write(
            bucket=INFLUXDB_BUCKET,
            org=INFLUXDB_ORG,
            record=point,
        )

        print(
            f"[INFLUXDB] Stored telemetry "
            f"from {machine_id}"
        )

        print(
            f"  RPM         : "
            f"{motor.get('rpm'):.2f}"
        )

        print(
            f"  Temperature : "
            f"{motor.get('temperature_c'):.2f} °C"
        )

        print(
            f"  Current     : "
            f"{motor.get('current_a'):.2f} A"
        )

        print(
            f"  Vibration   : "
            f"{motor.get('vibration_mm_s'):.2f} mm/s"
        )

    except Exception as error:

        print(
            "[INFLUXDB] ERROR:"
        )

        print(error)


# ============================================================
# Start MQTT
# ============================================================

def main():

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )

    client.on_connect = on_connect
    client.on_message = on_message

    print(
        "[SYSTEM] Connecting to MQTT..."
    )

    client.connect(
        MQTT_HOST,
        MQTT_PORT,
        keepalive=60,
    )

    try:

        client.loop_forever()

    except KeyboardInterrupt:

        print()
        print(
            "[SYSTEM] Stopping..."
        )

    finally:

        client.disconnect()

        influx_client.close()

        print(
            "[SYSTEM] InfluxDB writer stopped."
        )


if __name__ == "__main__":
    main()