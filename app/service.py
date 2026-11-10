"""Logique métier de la réservation d'un créneau."""

from typing import Any

from psycopg.errors import ExclusionViolation, ForeignKeyViolation

from app import repository
from app.errors import CreneauIndisponible, DonneesInvalides
from app.schemas import ReservationCreate


def creer_reservation(data: ReservationCreate) -> dict[str, Any]:
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
    except ForeignKeyViolation:
        raise DonneesInvalides("Utilisateur ou GPU inexistant") from None