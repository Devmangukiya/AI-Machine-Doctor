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
        "Simulator → Edge Gateway"
    )

    print("=" * 60)

    try:

        while True:

            # ------------------------------------------------
            # 1. Get machine data
            # ------------------------------------------------

            machine_data = (
                machine.generate_telemetry()
            )

            # ------------------------------------------------
            # 2. Simulate raw industrial input
            # ------------------------------------------------

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

            # ------------------------------------------------
            # 3. Process through Edge
            # ------------------------------------------------

            telemetry = gateway.process(
                raw_data
            )

            topic = (
                f"machine/{telemetry.machine_id}/telemetry"
            )

            mqtt.publish(
                topic=topic,
                payload=telemetry.model_dump(
                    mode="json"
                ),
            )

            # ------------------------------------------------
            # 4. Display normalized telemetry
            # ------------------------------------------------

            print(
                json.dumps(
                    telemetry.model_dump(),
                    indent=2,
                    default=str,
                )
            )

            print("-" * 60)

            time.sleep(
                PROCESS_INTERVAL_SECONDS
            )

    except KeyboardInterrupt:

        mqtt.disconnect()

        print()
        print("Edge Gateway stopped.")


if __name__ == "__main__":
    main()