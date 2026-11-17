"""Les tests unitaires n'utilisent pas PostgreSQL : on neutralise ici les fixtures
automatiques de tests/conftest.py (schéma et données de départ)."""
import pytest


@pytest.fixture(scope="session", autouse=True)
def schema():
    pass


@pytest.fixture(autouse=True)
def donnees():
    pass