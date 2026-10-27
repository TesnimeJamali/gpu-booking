"""Erreurs métier de l'application.

Ces exceptions ne connaissent pas HTTP : c'est main.py qui les
convertit en codes de réponse (409, 422...).
"""


class ReservationError(Exception):
    """Classe de base des erreurs liées aux réservations."""


class CreneauIndisponible(ReservationError):
    """Le créneau chevauche une réservation existante (-> 409)."""


class DonneesInvalides(ReservationError):
    """Les données de la demande sont incohérentes (-> 422)."""