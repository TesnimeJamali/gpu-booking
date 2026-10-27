"""Premier test d'intégration (itération 1) : API + service + vraie base PostgreSQL."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from tests.helpers import corps, demain, entetes


def test_reservation_nominale(client):
    r = client.post("/reservations", json=corps(demain(10), demain(12)), headers=entetes(1))
    assert r.status_code == 201
    assert r.json()["status"] == "CONFIRMED"


def test_deux_reservations_simultanees_une_seule_reussit(client):
    """LE test du cas à risque : deux utilisateurs visent le même créneau en même temps."""
    barriere = Barrier(2) #fonctionne comme le départ d’une course : les deux requêtes attendent que l’autre soit prête, puis partent ensemble.
    
    def appeler(user_id):
        barriere.wait()  # les deux requêtes partent au même instant
        return client.post(
            "/reservations", json=corps(demain(10), demain(12)), headers=entetes(user_id)
        )

    with ThreadPoolExecutor(2) as pool:
        reponses = list(pool.map(appeler, [1, 2]))
    assert sorted(r.status_code for r in reponses) == [201, 409] #vérifie qu’on obtient exactement un succès et un refus.


def test_chevauchement_partiel_refuse(client):
    client.post("/reservations", json=corps(demain(10), demain(12)), headers=entetes(1))
    r = client.post("/reservations", json=corps(demain(11), demain(13)), headers=entetes(2))
    assert r.status_code == 409


def test_creneaux_consecutifs_acceptes(client):
    client.post("/reservations", json=corps(demain(10), demain(12)), headers=entetes(1))
    r = client.post("/reservations", json=corps(demain(12), demain(14)), headers=entetes(2))
    assert r.status_code == 201