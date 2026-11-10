from datetime import datetime, timedelta, timezone

def demain(heure=10, minute=0):
    """Un instant fixe de demain (UTC) : les tests restent valides quelle que soit la date."""
    j = datetime.now(timezone.utc) + timedelta(days=1)
    return j.replace(hour=heure, minute=minute, second=0, microsecond=0)


def corps(debut, fin, gpu_id=1):
    #le contenu de la demande de réservation : le GPU, le début, la fin.
    return {"gpu_id": gpu_id, "start": debut.isoformat(), "end": fin.isoformat()}


def entetes(user_id):
    #user ID
    return {"X-User-Id": str(user_id)}