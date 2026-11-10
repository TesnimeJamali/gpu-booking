"""Contrôleur : routes HTTP des réservations."""

from fastapi import APIRouter

from app import service
from app.schemas import ReservationCreate, ReservationOut

router = APIRouter()


@router.post("/reservations", response_model=ReservationOut, status_code=201)
def creer(data: ReservationCreate):
    return service.creer_reservation(data)