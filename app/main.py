"""Point d'entrée de l'application gpu-booking."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import CreneauIndisponible, DonneesInvalides

app = FastAPI(title="gpu-booking")


@app.exception_handler(CreneauIndisponible)
async def creneau_indisponible_handler(request: Request, exc: CreneauIndisponible):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc) or "Créneau indisponible"},
    )


@app.exception_handler(DonneesInvalides)
async def donnees_invalides_handler(request: Request, exc: DonneesInvalides):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc) or "Données invalides"},
    )


@app.get("/health")
def health():
    """Route de contrôle : permet de vérifier que l'application répond."""
    return {"status": "ok"}