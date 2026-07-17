from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

LanguageCode = Literal["en", "id"]


class ChartCoordinates(BaseModel):
    x: float = Field(ge=0, le=100)
    y: float = Field(ge=0, le=100)


class MatrixPosition(BaseModel):
    id: str
    label: str
    value: int
    verified: bool
    calculation_trace: list[str]
    coordinates: ChartCoordinates | None = None
    interpretation_key: str | None = None


class MatrixCalculation(BaseModel):
    methodology_version: str
    birth_date: date
    positions: list[MatrixPosition]
    warnings: list[str]


class MatrixRequest(BaseModel):
    birth_date: date
    language: LanguageCode = "en"
    name: str | None = Field(default=None, max_length=80)
    focus: str | None = Field(default=None, max_length=180)

    @field_validator("name", "focus")
    @classmethod
    def empty_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class EnergyInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    energy: int = Field(ge=1, le=22)
    name: str
    keywords: list[str]
    core_meaning: str
    positive_expression: list[str]
    shadow_expression: list[str]
    relationships: str
    career: str
    money: str
    growth_advice: list[str]
    source_status: Literal["draft", "reviewed", "verified"]


class PositionInterpretation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    label: str
    description: str
    source_status: Literal["draft", "reviewed", "verified"]


class InterpretedPosition(BaseModel):
    position: MatrixPosition
    role: PositionInterpretation | None = None
    energy: EnergyInterpretation | None = None


class ReadingResponse(BaseModel):
    methodology_version: str
    birth_date: date
    language: LanguageCode
    name: str | None
    focus: str | None
    positions: list[InterpretedPosition]
    summary: str
    warnings: list[str]
    disclaimer: str
