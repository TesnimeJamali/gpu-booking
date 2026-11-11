"""Connexion à PostgreSQL."""

import os

import psycopg
from psycopg.rows import DictRow, dict_row


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "La variable d'environnement DATABASE_URL n'est pas définie."
        )
    return url


def get_connection() -> psycopg.Connection[DictRow]:
    """Ouvre une nouvelle connexion. Les lignes sont renvoyées sous forme de dict."""
    return psycopg.connect(database_url(), row_factory=dict_row)