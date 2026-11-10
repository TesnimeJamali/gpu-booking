"""Accès aux données des réservations (SQL uniquement)."""

from datetime import datetime
from typing import Any

from app.db import get_connection

# Espace de noms du verrou : évite les collisions avec d'autres usages
# des verrous consultatifs (UC05, par exemple).
VERROU_RESERVATION = 1


def inserer(
    user_id: int, gpu_id: int, start: datetime, end: datetime
) -> dict[str, Any]:
    """Insère une réservation et renvoie la ligne créée.

    Les insertions visant le même GPU sont sérialisées par un verrou
    consultatif, ce qui évite l'interblocage de PostgreSQL quand deux
    demandes arrivent en même temps. La seconde obtient alors
    psycopg.errors.ExclusionViolation (traitée dans le service).
    """
    with get_connection() as conn:
        conn.execute(
            "SELECT pg_advisory_xact_lock(%s::int, %s::int)",
            (VERROU_RESERVATION, gpu_id),
        )
        row = conn.execute(
            """
            INSERT INTO reservation (user_id, gpu_id, start_at, end_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id, user_id, gpu_id,
                      start_at AS "start", end_at AS "end", status
            """,
            (user_id, gpu_id, start, end),
        ).fetchone()

    if row is None:
        raise RuntimeError("L'insertion n'a renvoyé aucune ligne")
    return row