from datetime import date
from typing import Iterable, Literal

from pydantic import BaseModel, ConfigDict

from app.matrix.models import MatrixCalculation, MatrixPosition
from app.matrix.normalization import ConsecutiveDigitAdditionNormalizer
from app.matrix.rules import (
    TEACHER_TEASER_POSITION_LABELS,
    TEACHER_TEASER_SUPPORTED_POSITIONS,
    TeacherTeaserMethodology,
)


class UnsupportedCompatibilityPositionError(ValueError):
    """Raised when compatibility is requested for an unsupported position."""


class MissingCompatibilityPositionError(ValueError):
    """Raised when a personal calculation lacks a required supported position."""


class CompatibilityCalculation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    methodology_version: str
    status: Literal["transcribed_from_teacher_material"]
    person_1_birth_date: date
    person_2_birth_date: date
    positions: list[MatrixPosition]
    warnings: list[str]


class TeacherTeaserCompatibilityComposer:
    methodology_version = TeacherTeaserMethodology.version
    status = TeacherTeaserMethodology.status
    supported_positions = TEACHER_TEASER_SUPPORTED_POSITIONS

    def __init__(self) -> None:
        self.normalizer = ConsecutiveDigitAdditionNormalizer()

    def compose(
        self,
        person_1: MatrixCalculation,
        person_2: MatrixCalculation,
        position_ids: Iterable[str] | None = None,
    ) -> CompatibilityCalculation:
        for calculation in (person_1, person_2):
            if calculation.methodology_version != self.methodology_version:
                raise ValueError(
                    "Compatibility inputs must use teacher-teaser-v0.1."
                )

        requested = (
            tuple(position_ids)
            if position_ids is not None
            else self.supported_positions
        )
        unsupported = [
            position_id
            for position_id in requested
            if position_id not in self.supported_positions
        ]
        if unsupported:
            raise UnsupportedCompatibilityPositionError(
                "Unsupported compatibility position(s): "
                + ", ".join(unsupported)
            )

        person_1_positions = {
            position.id: position for position in person_1.positions
        }
        person_2_positions = {
            position.id: position for position in person_2.positions
        }
        missing = [
            position_id
            for position_id in requested
            if position_id not in person_1_positions
            or position_id not in person_2_positions
        ]
        if missing:
            raise MissingCompatibilityPositionError(
                "Compatibility input is missing supported position(s): "
                + ", ".join(missing)
            )

        positions: list[MatrixPosition] = []
        for position_id in requested:
            input_values = sorted(
                (
                    person_1_positions[position_id].value,
                    person_2_positions[position_id].value,
                )
            )
            raw_value = sum(input_values)
            normalized = self.normalizer.normalize_with_trace(raw_value)
            positions.append(
                MatrixPosition(
                    id=position_id,
                    label=(
                        "Compatibility "
                        + TEACHER_TEASER_POSITION_LABELS[position_id]
                    ),
                    value=normalized.value,
                    verified=False,
                    calculation_trace=[
                        f"{position_id} compatibility inputs: "
                        f"{input_values[0]} + {input_values[1]} = {raw_value}",
                        *normalized.calculation_trace,
                    ],
                    coordinates=None,
                    interpretation_key=None,
                )
            )

        return CompatibilityCalculation(
            methodology_version=self.methodology_version,
            status=self.status,
            person_1_birth_date=person_1.birth_date,
            person_2_birth_date=person_2.birth_date,
            positions=positions,
            warnings=[
                "Compatibility is provisional, supports only explicitly listed positions, and is not teacher-verified."
            ],
        )
