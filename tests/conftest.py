import os
from pathlib import Path
from urllib.parse import urlparse

import psycopg #pour connecter a une db postgres
import pytest
from fastapi.testclient import TestClient

# pas de planificateur pendant les tests
os.environ["SCHEDULER_ENABLED"] = "0"

#on impose une base dédiée aux tests car les tests EFFACENT le schéma de la base visée :
URL_TEST = os.environ.get(
    "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/gpu_test"
)
if not urlparse(URL_TEST).path.endswith("test"):
    raise RuntimeError(
        "TEST_DATABASE_URL doit viser une base dont le nom finit par 'test' "
        "(les tests suppriment toutes les tables)."
    )
os.environ["DATABASE_URL"] = URL_TEST  # l'application utilisera la base de test

from app.db import database_url
from app.main import app
SCHEMA = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


@pytest.fixture(scope="session", autouse=True)
#au début des tests, on vide la base et recrée les tables à partir du schema.sql
def schema():
    """Recrée le schéma une fois pour toute la session de tests."""
    with psycopg.connect(database_url(), autocommit=True) as conn:
        conn.execute("DROP SCHEMA public CASCADE")
        conn.execute("CREATE SCHEMA public")
        conn.execute(SCHEMA.read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def donnees():
    """Données de départ identiques avant chaque test : 3 utilisateurs, 1 GPU.
    Chaque test part donc d’une situation identique et propre. """
    with psycopg.connect(database_url(), autocommit=True) as conn:
        conn.execute(
            "TRUNCATE notification, reservation, gpu, app_user RESTART IDENTITY CASCADE"
        )
        conn.execute(
            """INSERT INTO app_user (nom, role, quota_hebdo_heures) VALUES
                ('Elabed', 'USER', 10), ('Mariem', 'USER', 10), ('Admin', 'ADMIN', 40)"""
        )
        conn.execute("INSERT INTO gpu (nom) VALUES ('GPU-0')")


@pytest.fixture
def client():
    """un faux navigateur qui envoie des requêtes à l’application. Les tests l’utilisent pour appeler /reservations"""
    return TestClient(app)


@pytest.fixture
def conn():
    """Connexion directe pour préparer ou vérifier des données dans les tests."""
    with psycopg.connect(database_url(), row_factory=psycopg.rows.dict_row) as c:
        yield c