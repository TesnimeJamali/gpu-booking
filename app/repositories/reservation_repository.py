"""Accès aux données des réservations (SQL uniquement, aucune règle métier)."""

from datetime import datetime

from psycopg.errors import ExclusionViolation, ForeignKeyViolation

from app.db import get_connection
from app.errors import AnnulationImpossible, CreneauIndisponible, DonneesInvalides
from app.models import Reservation

# Espace de noms du verrou consultatif (évite les collisions avec UC05).
VERROU_RESERVATION = 1

COLONNES = 'id, user_id, gpu_id, start_at AS "start", end_at AS "end", status'


class ReservationRepository:
    def inserer(
        self, user_id: int, gpu_id: int, start: datetime, end: datetime
    ) -> Reservation:
        """Insère une réservation.

        Les insertions visant le même GPU sont sérialisées par un verrou
        consultatif (évite l'interblocage PostgreSQL en cas de demandes
        simultanées). Les erreurs SQL sont traduites en erreurs métier.
        """
        try:
            with get_connection() as conn:
                conn.execute(
                    "SELECT pg_advisory_xact_lock(%s::int, %s::int)",
                    (VERROU_RESERVATION, gpu_id),
                )
                row = conn.execute(
                    f"""
                    INSERT INTO reservation (user_id, gpu_id, start_at, end_at)
                    VALUES (%s, %s, %s, %s)
                    RETURNING {COLONNES}
                    """,
                    (user_id, gpu_id, start, end),
                ).fetchone()
        except ExclusionViolation:
            raise CreneauIndisponible(
                "Ce créneau chevauche une réservation existante"
            ) from None
        except ForeignKeyViolation:
            raise DonneesInvalides("Utilisateur ou GPU inexistant") from None

        if row is None:
            raise RuntimeError("L'insertion n'a renvoyé aucune ligne")
        return Reservation(**row)

    def trouver(self, reservation_id: int) -> Reservation | None:
        """Renvoie la réservation, ou None si elle n'existe pas."""
        with get_connection() as conn:
            row = conn.execute(
                f"SELECT {COLONNES} FROM reservation WHERE id = %s",
                (reservation_id,),
            ).fetchone()
        return Reservation(**row) if row else None

    def annuler(self, reservation_id: int) -> Reservation:
        """Passe la réservation en CANCELLED (seulement si elle est CONFIRMED)."""
        with get_connection() as conn:
            row = conn.execute(
                f"""
                UPDATE reservation SET status = 'CANCELLED'
                WHERE id = %s AND status = 'CONFIRMED'
                RETURNING {COLONNES}
                """,
                (reservation_id,),
            ).fetchone()
        if row is None:
            raise AnnulationImpossible("La réservation n'est plus active")
        return Reservation(**row)