"""Tests unitaires du service de réservation (UC02)(sans db)

Chaque test cite l'étape ou le scénario alternatif de la fiche UC02
(docs/uc02-reserver-creneau.md) qu'il couvre.
"""
from datetime import datetime, timedelta, timezone

import pytest

from app.errors import CreneauIndisponible, DonneesInvalides
from app.models import Reservation
from app.services.reservation_service import DUREE_MAX, ReservationService

# Horloge figée : le service reçoit « maintenant » en paramètre, donc ces dates
# écrites en dur restent valides quel que soit le jour où l'on lance les tests.
MAINTENANT = datetime(2026, 4, 30, 9, 0, tzinfo=timezone.utc) # 09h00
DEBUT = MAINTENANT + timedelta(hours=1)  # 10h00
FIN = DEBUT + timedelta(hours=2)  # 12h00


class FauxRepository:
    """Faux dépôt : il enregistre les appels et peut simuler une erreur."""

    def __init__(self, erreur=None):
        self.erreur = erreur
        self.appels = []

    def inserer(self, user_id, gpu_id, start, end):
        self.appels.append((user_id, gpu_id, start, end))
        if self.erreur:
            raise self.erreur
        return Reservation(
            id=1, user_id=user_id, gpu_id=gpu_id, start=start, end=end, status="CONFIRMED"
        )


def un_service(repository):
    return ReservationService(repository, maintenant=lambda: MAINTENANT)


def test_scenario_nominal_etapes_2_a_6():
    repo = FauxRepository()
    resultat = un_service(repo).creer_reservation(1, 1, DEBUT, FIN)
    assert repo.appels == [(1, 1, DEBUT, FIN)]
    assert resultat.status == "CONFIRMED"
    assert resultat.start == DEBUT and resultat.end == FIN


def test_alternatif_2a_fin_egale_au_debut():
    repo = FauxRepository()
    with pytest.raises(DonneesInvalides):
        un_service(repo).creer_reservation(1, 1, DEBUT, DEBUT) #fin = debut
    assert repo.appels == []


def test_alternatif_2a_fin_avant_le_debut():
    repo = FauxRepository()
    with pytest.raises(DonneesInvalides):
        un_service(repo).creer_reservation(1, 1, FIN, DEBUT)# debut> fin
    assert repo.appels == []


def test_alternatif_3a_debut_dans_le_passe():
    repo = FauxRepository()
    passe = MAINTENANT - timedelta(minutes=1)
    with pytest.raises(DonneesInvalides):
        un_service(repo).creer_reservation(1, 1, passe, passe + timedelta(hours=1))
    assert repo.appels == []


def test_etape_3_debut_egal_a_maintenant_accepte():
    repo = FauxRepository()
    un_service(repo).creer_reservation(1, 1, MAINTENANT, MAINTENANT + timedelta(hours=1))
    assert len(repo.appels) == 1


def test_alternatif_4a_duree_superieure_au_maximum():
    repo = FauxRepository()
    with pytest.raises(DonneesInvalides):
        un_service(repo).creer_reservation(1, 1, DEBUT, DEBUT + DUREE_MAX + timedelta(minutes=1))
    assert repo.appels == []


def test_etape_4_duree_egale_au_maximum_acceptee():
    repo = FauxRepository()
    un_service(repo).creer_reservation(1, 1, DEBUT, DEBUT + DUREE_MAX)
    assert len(repo.appels) == 1


def test_alternatif_5a_conflit_signale_par_le_repository():
    repo = FauxRepository(erreur=CreneauIndisponible("chevauchement"))
    with pytest.raises(CreneauIndisponible):
        un_service(repo).creer_reservation(1, 1, DEBUT, FIN)


def test_alternatif_5b_gpu_ou_utilisateur_inexistant():
    repo = FauxRepository(erreur=DonneesInvalides("GPU inexistant"))
    with pytest.raises(DonneesInvalides):
        un_service(repo).creer_reservation(1, 99, DEBUT, FIN)