"""
Raw machine data received by the Edge Gateway.

In the real world, this could come from:
- Siemens PLC
- OPC UA
- Modbus TCP
- MQTT
- Other industrial controllers
"""

from pydantic import BaseModel


class RawMachineData(BaseModel):

    machine_id: str

    rpm: float

    current: float

    temperature: float

    vibration: float

    frequency: float

    pressure: float

    flow: float

    good_count: int

    reject_count: int

    cycle_time: float

    state: str

    fault_code: str | None = None