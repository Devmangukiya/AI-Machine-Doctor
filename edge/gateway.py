"""
AI Machine Doctor Edge Gateway.
"""

from schemas.telemetry import MachineTelemetry

from .models import RawMachineData
from .normalizer import normalize_machine_data


class EdgeGateway:

    def __init__(
        self,
        edge_id: str,
    ):

        self.edge_id = edge_id

    def process(
        self,
        raw_data: RawMachineData,
    ) -> MachineTelemetry:

        print(
            f"[EDGE] Received data from "
            f"{raw_data.machine_id}"
        )

        telemetry = normalize_machine_data(
            raw_data
        )

        print(
            f"[EDGE] Normalized telemetry for "
            f"{telemetry.machine_id}"
        )

        return telemetry