from fastapi import APIRouter, HTTPException

from app.interpretations.formatter import ReadingComposer
from app.interpretations.repository import InterpretationRepository
from app.matrix.calculator import MatrixCalculator
from app.matrix.models import MatrixRequest, ReadingResponse

router = APIRouter(prefix="/matrix", tags=["matrix"])

calculator = MatrixCalculator()
repository = InterpretationRepository()
composer = ReadingComposer(repository)


@router.post("/calculate", response_model=ReadingResponse)
def calculate_matrix(payload: MatrixRequest) -> ReadingResponse:
    try:
        result = calculator.calculate(payload.birth_date)
        return composer.compose(
            calculation=result,
            language=payload.language,
            name=payload.name,
            focus=payload.focus,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
