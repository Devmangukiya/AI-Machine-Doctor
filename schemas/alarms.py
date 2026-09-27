"""
Canonical machine alarm schema.
"""

from datetime import datetime, timezone
from uuid import uuid4
from typing import Literal

from pydantic import BaseModel, Field


AlarmSeverity = Literal[
    "INFO",
    "WARNING",
    "CRITICAL",
]


class MachineAlarm(BaseModel):

    alarm_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    machine_id: str

    code: str

    severity: AlarmSeverity

    message: str

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    acknowledged: bool = False

    acknowledged_by: str | None = None

    acknowledged_at: datetime | None = None