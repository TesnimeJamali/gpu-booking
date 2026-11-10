"""Contrôleur : routes HTTP des réservations (mince)."""

from dataclasses import asdict

from fastapi import APIRouter, Depends, Header

from app.repositories.reservation_repository import ReservationRepository
from app.schemas import ReservationCreate, ReservationOut
from app.services.reservation_service import ReservationService

router = APIRouter()


def get_reservation_service() -> ReservationService:
    return ReservationService(ReservationRepository())


@router.post("/reservations", response_model=ReservationOut, status_code=201)
def creer(
    data: ReservationCreate,
    x_user_id: int = Header(),
    service: ReservationService = Depends(get_reservation_service),
) -> ReservationOut:
    reservation = service.creer_reservation(
        x_user_id, data.gpu_id, data.start, data.end
    )
    return ReservationOut(**asdict(reservation))