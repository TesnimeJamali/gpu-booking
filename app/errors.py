
class ReservationError(Exception):
    """Classe de base des erreurs liées aux réservations."""


class CreneauIndisponible(ReservationError):
    """Le créneau chevauche une réservation existante (-> 409)."""


class DonneesInvalides(ReservationError):
    """Les données de la demande sont incohérentes (-> 422)."""


class ReservationIntrouvable(ReservationError):
    """La réservation demandée n'existe pas (-> 404)."""


class AccesInterdit(ReservationError):
    """L'utilisateur n'est pas le propriétaire de la réservation (-> 403)."""


class AnnulationImpossible(ReservationError):
    """La réservation est déjà commencée ou n'est plus active (-> 409)."""