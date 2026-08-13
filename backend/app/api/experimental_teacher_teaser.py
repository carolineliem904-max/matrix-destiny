from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.core.config import settings
from app.matrix.calculator import MatrixCalculator
from app.matrix.compatibility import TeacherTeaserCompatibilityComposer
from app.matrix.models import MatrixCalculation, MatrixPosition
from app.matrix.rules import (
    TEACHER_TEASER_SUPPORTED_POSITIONS,
    TeacherTeaserMethodology,
)

router = APIRouter(
    prefix="/experimental/teacher-teaser",
    tags=["experimental"],
)

UNSUPPORTED_POSITIONS: tuple[str, ...] = (
    "small_internal_nodes",
    "annual_energy",
    "monthly_energy",
    "age_cycles",
    "money_output",
    "relationship_output",
    "ahmad_sahroni_forecast",
)

calculator = MatrixCalculator(methodology=TeacherTeaserMethodology())
compatibility_composer = TeacherTeaserCompatibilityComposer()


class ExperimentalPersonalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    birth_date: date
    name: str | None = Field(default=None, max_length=80)


class ExperimentalPersonRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=80)
    birth_date: date


class ExperimentalCompatibilityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    person_1: ExperimentalPersonRequest
    person_2: ExperimentalPersonRequest


class ExperimentalPersonalMatrix(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    methodology_version: str
    verified: bool
    birth_date: date
    supported_positions: list[MatrixPosition]
    unsupported_positions: list[str]
    warnings: list[str]


class ExperimentalCompatibilityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    methodology_version: str
    verified: bool
    person_1: ExperimentalPersonalMatrix
    person_2: ExperimentalPersonalMatrix
    supported_compatibility_positions: list[MatrixPosition]
    unsupported_positions: list[str]
    warnings: list[str]


def _require_experimental_flag() -> None:
    if not settings.enable_experimental_methodologies:
        raise HTTPException(
            status_code=404,
            detail=(
                "Teacher teaser experimental endpoints are unavailable. "
                "Set ENABLE_EXPERIMENTAL_METHODOLOGIES=true for local development."
            ),
        )


def _personal_payload(
    calculation: MatrixCalculation,
    name: str | None,
) -> ExperimentalPersonalMatrix:
    return ExperimentalPersonalMatrix(
        name=name,
        methodology_version=calculation.methodology_version,
        verified=False,
        birth_date=calculation.birth_date,
        supported_positions=calculation.positions,
        unsupported_positions=list(UNSUPPORTED_POSITIONS),
        warnings=calculation.warnings,
    )


@router.post("/personal", response_model=ExperimentalPersonalMatrix)
def calculate_experimental_personal(
    payload: ExperimentalPersonalRequest,
) -> ExperimentalPersonalMatrix:
    _require_experimental_flag()
    try:
        result = calculator.calculate(payload.birth_date)
        return _personal_payload(result, payload.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/compatibility",
    response_model=ExperimentalCompatibilityResponse,
)
def calculate_experimental_compatibility(
    payload: ExperimentalCompatibilityRequest,
) -> ExperimentalCompatibilityResponse:
    _require_experimental_flag()
    try:
        person_1 = calculator.calculate(payload.person_1.birth_date)
        person_2 = calculator.calculate(payload.person_2.birth_date)
        compatibility = compatibility_composer.compose(person_1, person_2)
        return ExperimentalCompatibilityResponse(
            methodology_version=compatibility.methodology_version,
            verified=False,
            person_1=_personal_payload(person_1, payload.person_1.name),
            person_2=_personal_payload(person_2, payload.person_2.name),
            supported_compatibility_positions=compatibility.positions,
            unsupported_positions=list(UNSUPPORTED_POSITIONS),
            warnings=[
                *compatibility.warnings,
                "Only supported teacher-teaser positions are returned.",
            ],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
