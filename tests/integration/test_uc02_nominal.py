"""Tests d'intégration de UC02 : API + service + repository + vraie base PostgreSQL.
Chaque test cite l'étape de la fiche UC02 (docs/uc02-reserver-creneau.md) qu'il couvre.
"""
from tests.helpers import corps, demain, entetes

def test_scenario_nominal_etapes_5_et_6_reservation_enregistree(client, conn):
    """Étapes 5 et 6 : 201 renvoyé ET la réservation est bien enregistrée en base."""
    debut, fin = demain(10), demain(12)

    r = client.post("/reservations", json=corps(debut, fin), headers=entetes(1))

    assert r.status_code == 201
    assert r.json()["status"] == "CONFIRMED"
    lignes = conn.execute(
        "SELECT user_id, gpu_id, start_at, end_at, status FROM reservation"
    ).fetchall()
    assert len(lignes) == 1
    assert lignes[0]["user_id"] == 1
    assert lignes[0]["gpu_id"] == 1
    assert lignes[0]["start_at"] == debut
    assert lignes[0]["end_at"] == fin
    assert lignes[0]["status"] == "CONFIRMED"


def test_postcondition_echec_conflit_5a_aucune_reservation_supplementaire(client, conn):
    """Alternatif 5a + postcondition d'échec : un conflit (409) ne crée rien en base."""
    client.post("/reservations", json=corps(demain(10), demain(12)), headers=entetes(1))

    r = client.post("/reservations", json=corps(demain(11), demain(13)), headers=entetes(2))

    assert r.status_code == 409
    lignes = conn.execute("SELECT user_id FROM reservation").fetchall()
    assert len(lignes) == 1
    assert lignes[0]["user_id"] == 1