"""
Canonical machine event schema.
"""

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class MachineEvent(BaseModel):
    """
    Represents something that happened on a machine.
    """

    event_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    machine_id: str

    event_type: str

    message: str

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: dict = Field(default_factory=dict)