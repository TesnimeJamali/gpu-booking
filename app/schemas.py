from pydantic import AwareDatetime, BaseModel, model_validator


class ReservationCreate(BaseModel):
    user_id: int
    gpu_id: int
    debut: AwareDatetime
    fin: AwareDatetime
    # (le validateur verifier_ordre reste identique)


class ReservationOut(BaseModel):
    id: int
    user_id: int
    gpu_id: int
    debut: datetime
    fin: datetime
    status: str