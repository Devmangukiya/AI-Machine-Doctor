"""
Canonical machine definition for AI Machine Doctor.
"""

from pydantic import BaseModel


class Machine(BaseModel):
    """
    Represents an industrial machine registered in Machine Doctor.
    """

    machine_id: str
    machine_type: str

    customer_id: str
    factory_id: str
    plant_id: str

    manufacturer: str | None = None
    model: str | None = None

    controller_type: str | None = None
    controller_protocol: str | None = None

    is_active: bool = True