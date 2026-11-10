"""Contrôleur : routes HTTP des réservations."""

from typing import Any

from fastapi import APIRouter, Header

from app import service
from app.schemas import ReservationCreate, ReservationOut

router = APIRouter()


@router.post("/reservations", response_model=ReservationOut, status_code=201)
def creer(
    data: ReservationCreate,
    x_user_id: int = Header(),
) -> dict[str, Any]:
    return service.creer_reservation(x_user_id, data)