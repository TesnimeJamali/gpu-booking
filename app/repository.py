"""Accès aux données des réservations (SQL uniquement)."""

from datetime import datetime
from typing import Any

from app.db import get_connection


def inserer(
    user_id: int, gpu_id: int, debut: datetime, fin: datetime
) -> dict[str, Any]:
    """Insère une réservation et renvoie la ligne créée.

    Si le créneau chevauche une réservation existante, PostgreSQL lève
    psycopg.errors.ExclusionViolation (traitée dans le service).
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            INSERT INTO reservation (user_id, gpu_id, start_at, end_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id, user_id, gpu_id,
                      start_at AS debut, end_at AS fin, status
            """,
            (user_id, gpu_id, debut, fin),
        ).fetchone()

    if row is None:
        raise RuntimeError("L'insertion n'a renvoyé aucune ligne")
    return row