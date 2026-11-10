"""Entités du domaine."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reservation:
    id: int
    user_id: int
    gpu_id: int
    start: datetime
    end: datetime
    status: str