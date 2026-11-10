"""Logique métier de la réservation d'un créneau."""

from typing import Any

from psycopg.errors import ExclusionViolation, ForeignKeyViolation

from app import repository
from app.errors import CreneauIndisponible, DonneesInvalides
from app.schemas import ReservationCreate


def creer_reservation(user_id: int, data: ReservationCreate) -> dict[str, Any]:
    try:
        return repository.inserer(
            user_id=user_id,
            gpu_id=data.gpu_id,
            start=data.start,
            end=data.end,
        )
    except ExclusionViolation:
        raise CreneauIndisponible(
            "Ce créneau chevauche une réservation existante"
        ) from None
    except ForeignKeyViolation:
        raise DonneesInvalides("Utilisateur ou GPU inexistant") from None