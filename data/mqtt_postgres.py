"""
MQTT -> PostgreSQL consumer.

Stores machine events and alarms received from MQTT.
"""

import json
import time

import paho.mqtt.client as mqtt

from data.postgres_writer import PostgreSQLWriter


# ============================================================
# CONFIGURATION
# ============================================================

MQTT_HOST = "localhost"
MQTT_PORT = 1883

EVENT_TOPIC = "machine/+/events"
ALARM_TOPIC = "machine/+/alarms"


# ============================================================
# POSTGRES WRITER
# ============================================================

writer = PostgreSQLWriter()


# ============================================================
# MQTT CALLBACK
# ============================================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print(
            "[MQTT] Connected successfully."
        )

        client.subscribe(EVENT_TOPIC)

        client.subscribe(ALARM_TOPIC)

        print(
            f"[MQTT] Subscribed to: {EVENT_TOPIC}"
        )

        print(
            f"[MQTT] Subscribed to: {ALARM_TOPIC}"
        )

    else:

        print(
            f"[MQTT] Connection failed. Code: {rc}"
        )


def on_message(client, userdata, message):

    try:

        # ----------------------------------------------------
        # Decode MQTT payload
        # ----------------------------------------------------

        payload = json.loads(
            message.payload.decode("utf-8")
        )

        topic = message.topic

        print()
        print(
            f"[MQTT] Message received: {topic}"
        )

        # ----------------------------------------------------
        # EVENT
        # ----------------------------------------------------

        if topic.endswith("/events"):

            writer.write_event(
                payload
            )

        # ----------------------------------------------------
        # ALARM
        # ----------------------------------------------------

        elif topic.endswith("/alarms"):

            writer.write_alarm(
                payload
            )

    except Exception as error:

        print(
            f"[ERROR] Failed to process MQTT message: "
            f"{error}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("       MQTT -> POSTGRESQL")
    print("=" * 60)
    print()

    print(
        f"MQTT Broker : {MQTT_HOST}:{MQTT_PORT}"
    )

    print(
        f"Event Topic : {EVENT_TOPIC}"
    )

    print(
        f"Alarm Topic : {ALARM_TOPIC}"
    )

    print()

    # --------------------------------------------------------
    # PostgreSQL
    # --------------------------------------------------------

    print(
        "[SYSTEM] Connecting to PostgreSQL..."
    )

    writer.connect()

    # --------------------------------------------------------
    # MQTT
    # --------------------------------------------------------

    print(
        "[SYSTEM] Connecting to MQTT..."
    )

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION1
    )

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(
        MQTT_HOST,
        MQTT_PORT,
        60,
    )

    print(
        "[SYSTEM] Starting MQTT listener..."
    )

    print()

    try:

        client.loop_forever()

    except KeyboardInterrupt:

        print()
        print(
            "[SYSTEM] Stopping..."
        )

    finally:

        client.disconnect()

        writer.close()


if __name__ == "__main__":
    main()