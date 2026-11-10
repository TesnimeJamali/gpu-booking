"""Accès aux données des réservations (SQL uniquement)."""

from datetime import datetime

from app.db import get_connection


def inserer(user_id: int, gpu_id: int, debut: datetime, fin: datetime) -> dict:
    with get_connection() as conn:
        return conn.execute(
            """
            INSERT INTO reservation (user_id, gpu_id, start_at, end_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id, user_id, gpu_id,
                      start_at AS debut, end_at AS fin, status
            """,
            (user_id, gpu_id, debut, fin),
        ).fetchone()