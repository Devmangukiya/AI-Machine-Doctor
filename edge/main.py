"""
Run the Edge Gateway with the virtual machine.
"""

import json
import time

from .mqtt_client import MQTTClient

from simulator.machine import VirtualMachine

from .config import (
    EDGE_ID,
    PROCESS_INTERVAL_SECONDS,
)

from .gateway import EdgeGateway

from .models import RawMachineData


def main():

    print()
    print("=" * 60)
    print("       AI MACHINE DOCTOR - EDGE GATEWAY")
    print("=" * 60)
    print()

    machine = VirtualMachine(seed=42)

    gateway = EdgeGateway(
        edge_id=EDGE_ID
    )

    mqtt = MQTTClient(
        broker_host="localhost",
        broker_port=1883,
    )

    mqtt.connect()

    print(
        f"Edge ID    : {EDGE_ID}"
    )

    print(
        f"Machine ID : {machine.machine_id}"
    )

    print()

    print(
        "Simulator → Edge Gateway → MQTT"
    )

    print("=" * 60)

    try:

        while True:

            # =================================================
            # 1. Get machine data from simulator
            # =================================================

            machine_data = (
                machine.generate_telemetry()
            )

            # =================================================
            # 2. Simulate raw industrial input
            #
            # In the real world this section will eventually
            # receive data from PLC / OPC UA / Modbus etc.
            # =================================================

            raw_data = RawMachineData(

                machine_id=(
                    machine_data.machine_id
                ),

                rpm=(
                    machine_data.motor.rpm
                ),

                current=(
                    machine_data.motor.current_a
                ),

                temperature=(
                    machine_data.motor.temperature_c
                ),

                vibration=(
                    machine_data.motor.vibration_mm_s
                ),

                frequency=(
                    machine_data.vfd.frequency_hz
                ),

                pressure=(
                    machine_data.process.pressure_bar
                ),

                flow=(
                    machine_data.process.flow_l_min
                ),

                good_count=(
                    machine_data.production.good_count
                ),

                reject_count=(
                    machine_data.production.reject_count
                ),

                cycle_time=(
                    machine_data.production.cycle_time_s
                ),

                state=machine_data.state,

                fault_code=(
                    machine_data.vfd.fault_code
                ),
            )

            # =================================================
            # 3. Process through Edge Gateway
            # =================================================

            telemetry = gateway.process(
                raw_data
            )

            # =================================================
            # 6. Publish EVENTS
            # =================================================

            events_topic = (
                f"machine/"
                f"{telemetry.machine_id}"
                f"/events"
            )

            for event in machine.last_events:

                mqtt.publish(
                    topic=events_topic,
                    payload=event.model_dump(
                        mode="json"
                    ),
                )

            # =================================================
            # 7. Publish ALARMS
            # =================================================

            alarms_topic = (
                f"machine/"
                f"{telemetry.machine_id}"
                f"/alarms"
            )

            for alarm in machine.last_alarms:

                mqtt.publish(
                    topic=alarms_topic,
                    payload=alarm.model_dump(
                        mode="json"
                    ),
                )

            # =================================================
            # 4. Publish TELEMETRY
            # =================================================

            telemetry_topic = (
                f"machine/"
                f"{telemetry.machine_id}"
                f"/telemetry"
            )

            mqtt.publish(
                topic=telemetry_topic,
                payload=telemetry.model_dump(
                    mode="json"
                ),
            )

            # =================================================
            # 5. Publish MACHINE STATE
            # =================================================

            state_topic = (
                f"machine/"
                f"{telemetry.machine_id}"
                f"/state"
            )

            state_payload = {
                "machine_id": telemetry.machine_id,
                "timestamp": telemetry.timestamp.isoformat(),
                "state": telemetry.state,
            }

            mqtt.publish(
                topic=state_topic,
                payload=state_payload,
            )

            # =================================================
            # 6. Display normalized telemetry
            # =================================================

            print()

            print(
                json.dumps(
                    telemetry.model_dump(),
                    indent=2,
                    default=str,
                )
            )

            print()

            print(
                f"[MQTT] Telemetry → "
                f"{telemetry_topic}"
            )

            print(
                f"[MQTT] State → "
                f"{state_topic}"
            )

            print("-" * 60)

            # =================================================
            # 7. Wait before next machine reading
            # =================================================

            time.sleep(
                PROCESS_INTERVAL_SECONDS
            )

    except KeyboardInterrupt:

        mqtt.disconnect()

        print()
        print("Edge Gateway stopped.")


if __name__ == "__main__":
    main()