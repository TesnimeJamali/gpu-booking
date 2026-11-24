"""Point d'entrée de l'application gpu-booking."""
#Seul endroit qui connaît à la fois les erreurs métier et HTTP

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.controller import router as reservations_router
from app.errors import (
    AccesInterdit,
    AnnulationImpossible,
    CreneauIndisponible,
    DonneesInvalides,
    ReservationIntrouvable,
)
app = FastAPI(title="gpu-booking")
app.include_router(reservations_router)


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

@app.exception_handler(ReservationIntrouvable)
async def reservation_introuvable_handler(request: Request, exc: ReservationIntrouvable):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc) or "Réservation introuvable"},
    )


@app.exception_handler(AccesInterdit)
async def acces_interdit_handler(request: Request, exc: AccesInterdit):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc) or "Accès interdit"},
    )


@app.exception_handler(AnnulationImpossible)
async def annulation_impossible_handler(request: Request, exc: AnnulationImpossible):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc) or "Annulation impossible"},
    )

@app.get("/health") 
def health():
    """Route de contrôle : permet de vérifier que l'application répond."""
    return {"status": "ok"}