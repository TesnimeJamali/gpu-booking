"""Modèles de données de l'API (requêtes et réponses)."""

from datetime import datetime

from pydantic import AwareDatetime, BaseModel, model_validator


class ReservationCreate(BaseModel):
    """Corps de la requête POST /reservations."""

    user_id: int
    gpu_id: int
    debut: AwareDatetime
    fin: AwareDatetime

    @model_validator(mode="after")
    def verifier_ordre(self):
        if self.fin <= self.debut:
            raise ValueError("fin doit être strictement après debut")
        return self


class ReservationOut(BaseModel):
    """Réservation renvoyée par l'API (réponse 201)."""

    id: int
    user_id: int
    gpu_id: int
    debut: datetime
    fin: datetime
    status: str