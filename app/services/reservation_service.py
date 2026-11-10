"""Logique métier de la réservation d'un créneau (aucun SQL ici)."""

from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from app.errors import DonneesInvalides
from app.models import Reservation
from app.repositories.reservation_repository import ReservationRepository

# Valeur provisoire : à confirmer avec l'équipe.
DUREE_MAX = timedelta(hours=8)


def _maintenant_utc() -> datetime:
    return datetime.now(timezone.utc)


class ReservationService:
    def __init__(
        self,
        repository: ReservationRepository,
        maintenant: Callable[[], datetime] = _maintenant_utc,
    ):
        self._repository = repository
        self._maintenant = maintenant

    def creer_reservation(
        self, user_id: int, gpu_id: int, start: datetime, end: datetime
    ) -> Reservation:
        if end <= start:
            raise DonneesInvalides("La fin doit être strictement après le début")
        if start < self._maintenant():
            raise DonneesInvalides("Le début ne peut pas être dans le passé")
        if end - start > DUREE_MAX:
            raise DonneesInvalides("La durée dépasse la durée maximale autorisée")
        return self._repository.inserer(user_id, gpu_id, start, end)