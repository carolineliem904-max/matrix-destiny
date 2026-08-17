from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.matrix.mahesa_gantari import (
    MahesaGantariCalculation,
    MahesaGantariCalculationRequest,
    MahesaGantariRwsMethodology,
)

router = APIRouter(prefix="/experimental/mahesa-gantari", tags=["experimental"])
methodology = MahesaGantariRwsMethodology()


@router.post("/personal", response_model=MahesaGantariCalculation)
def calculate_personal(
    payload: MahesaGantariCalculationRequest,
) -> MahesaGantariCalculation:
    if not settings.enable_experimental_methodologies:
        raise HTTPException(status_code=404, detail="Experimental methodology unavailable.")
    try:
        return methodology.calculate(payload.birth_date, payload.sect)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
