"""
MQTT client for the AI Machine Doctor Edge Gateway.
"""

import json

import paho.mqtt.client as mqtt


class MQTTClient:

    def __init__(
        self,
        broker_host: str = "localhost",
        broker_port: int = 1883,
    ):
        self.broker_host = broker_host
        self.broker_port = broker_port

        self.connected = False

        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):
        if reason_code == 0:
            self.connected = True
            print("[MQTT] Connected to broker")
        else:
            print(
                f"[MQTT] Connection failed: "
                f"{reason_code}"
            )

    def _on_disconnect(
        self,
        client,
        userdata,
        disconnect_flags,
        reason_code,
        properties,
    ):
        self.connected = False
        print("[MQTT] Disconnected from broker")

    def connect(self):

        print(
            f"[MQTT] Connecting to "
            f"{self.broker_host}:{self.broker_port}"
        )

        self.client.connect(
            self.broker_host,
            self.broker_port,
            keepalive=60,
        )

        self.client.loop_start()

    def publish(
        self,
        topic: str,
        payload: dict,
    ):

        if not self.connected:
            print(
                "[MQTT] Not connected. "
                "Message not published."
            )
            return

        message = json.dumps(payload)

        result = self.client.publish(
            topic,
            message,
            qos=1,
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(
                f"[MQTT] Published → {topic}"
            )
        else:
            print(
                f"[MQTT] Publish failed → {topic}"
            )

    def disconnect(self):

        self.client.loop_stop()
        self.client.disconnect()

        print("[MQTT] Client stopped")