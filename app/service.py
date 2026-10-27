"""Logique métier de la réservation d'un créneau."""

from psycopg.errors import ExclusionViolation

from app import repository
from app.errors import CreneauIndisponible
from app.schemas import ReservationCreate


def creer_reservation(data: ReservationCreate) -> dict:
    try:
        return repository.inserer(
            user_id=data.user_id,
            gpu_id=data.gpu_id,
            debut=data.debut,
            fin=data.fin,
        )
    except ExclusionViolation:
        raise CreneauIndisponible(
            "Ce créneau chevauche une réservation existante"
        ) from None