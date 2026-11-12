"""Modèles de données de l'API (requêtes et réponses)."""

from datetime import datetime

from pydantic import AwareDatetime, BaseModel, model_validator


class ReservationCreate(BaseModel):
    """Corps de la requête POST /reservations (l'utilisateur est dans X-User-Id)."""

    gpu_id: int
    start: AwareDatetime
    end: AwareDatetime

    @model_validator(mode="after")
    def verifier_ordre(self):
        if self.end <= self.start:
            raise ValueError("end doit être strictement après start")
        return self


class ReservationOut(BaseModel):
    """Réservation renvoyée par l'API (réponse 201)."""

    id: int
    user_id: int
    gpu_id: int
    start: datetime
    end: datetime
    status: str