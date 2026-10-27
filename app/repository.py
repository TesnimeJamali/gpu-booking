"""Accès aux données des réservations (SQL uniquement)."""

from datetime import datetime

from app.db import get_connection


def inserer(user_id: int, gpu_id: int, debut: datetime, fin: datetime) -> dict:
    """Insère une réservation et renvoie la ligne créée.

    Si le créneau chevauche une réservation existante, PostgreSQL lève
    psycopg.errors.ExclusionViolation (traitée dans le service).
    """
    with get_connection() as conn:
        return conn.execute(
            """
            INSERT INTO reservations (user_id, gpu_id, debut, fin)
            VALUES (%s, %s, %s, %s)
            RETURNING id, user_id, gpu_id, debut, fin
            """,
            (user_id, gpu_id, debut, fin),
        ).fetchone()