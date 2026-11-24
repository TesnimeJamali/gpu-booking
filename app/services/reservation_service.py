"""Logique métier des réservations (aucun SQL ici)."""

from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from app.errors import (
    AccesInterdit,
    AnnulationImpossible,
    DonneesInvalides,
    ReservationIntrouvable,
)
from app.models import Reservation
from app.repositories.reservation_repository import ReservationRepository

# Valeur provisoire : à confirmer avec l'équipe.
# Conservée au niveau du module pour compatibilité avec les tests existants.
DUREE_MAX = timedelta(hours=8)


def _maintenant_utc() -> datetime:
    return datetime.now(timezone.utc)


class ReservationService:
    DUREE_MAX = DUREE_MAX  # attribut de classe, comme dans le diagramme UML

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
        if end - start > self.DUREE_MAX:
            raise DonneesInvalides("La durée dépasse la durée maximale autorisée")
        return self._repository.inserer(user_id, gpu_id, start, end)

    def annuler_reservation(self, user_id: int, reservation_id: int) -> Reservation:
        reservation = self._repository.trouver(reservation_id)
        if reservation is None:
            raise ReservationIntrouvable("Réservation introuvable")
        if reservation.user_id != user_id:
            raise AccesInterdit("Seul le propriétaire peut annuler sa réservation")
        if reservation.status != "CONFIRMED":
            raise AnnulationImpossible("La réservation n'est plus active")
        if reservation.start <= self._maintenant():
            raise AnnulationImpossible(
                "Une réservation déjà commencée ne peut pas être annulée"
            )
        return self._repository.annuler(reservation_id)