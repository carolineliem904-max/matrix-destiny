import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.matrix.validator import validate_birth_date

FixtureStatus = Literal[
    "transcribed",
    "independently_checked",
    "teacher_verified",
    "disputed",
]
FixtureSourceType = Literal[
    "synthetic",
    "course_material",
    "teacher_chart",
    "book",
    "other",
]

_ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _parse_strict_iso_date(value: Any, field_name: str) -> date:
    if isinstance(value, datetime):
        raise ValueError(f"{field_name} must be a date, not a datetime.")
    if isinstance(value, date):
        return value
    if not isinstance(value, str) or not _ISO_DATE_PATTERN.fullmatch(value):
        raise ValueError(f"{field_name} must use YYYY-MM-DD format.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid calendar date.") from exc


class ReferenceChartCoordinates(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: float = Field(ge=0, le=100)
    y: float = Field(ge=0, le=100)


class ExpectedReferencePosition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    position_id: str = Field(min_length=1)
    source_label: str = Field(min_length=1)
    label_en: str | None = None
    label_id: str | None = None
    expected_value: int = Field(strict=True)
    calculation_trace: list[str] | None = None
    chart_coordinates: ReferenceChartCoordinates | None = None
    status: FixtureStatus
    notes: str | None = None
    is_raw_intermediate: bool = False

    @field_validator("expected_value")
    @classmethod
    def validate_expected_value(cls, value: int) -> int:
        if value < 1:
            raise ValueError("expected_value must be a positive integer.")
        return value

    @model_validator(mode="after")
    def validate_final_value_range(self) -> "ExpectedReferencePosition":
        if self.expected_value > 22 and not self.is_raw_intermediate:
            raise ValueError(
                "expected_value must be between 1 and 22 unless "
                "is_raw_intermediate is true."
            )
        return self


class MethodologyReferenceFixture(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_name: str = Field(min_length=1)
    birth_date: date
    methodology_version: str = Field(min_length=1)
    source_name: str
    source_type: FixtureSourceType
    source_reference: str
    verified_by: str | None = None
    verification_date: date | None = None
    notes: str
    is_synthetic: bool = False
    expected_positions: list[ExpectedReferencePosition] = Field(min_length=1)

    @field_validator("birth_date", mode="before")
    @classmethod
    def validate_birth_date(cls, value: Any) -> date:
        parsed = _parse_strict_iso_date(value, "birth_date")
        validate_birth_date(parsed)
        return parsed

    @field_validator("verification_date", mode="before")
    @classmethod
    def validate_verification_date(cls, value: Any) -> date | None:
        if value is None:
            return None
        parsed = _parse_strict_iso_date(value, "verification_date")
        if parsed > date.today():
            raise ValueError("verification_date cannot be in the future.")
        return parsed

    @model_validator(mode="after")
    def validate_fixture_integrity(self) -> "MethodologyReferenceFixture":
        position_ids = [position.position_id for position in self.expected_positions]
        if len(position_ids) != len(set(position_ids)):
            raise ValueError("expected_positions contains duplicate position_id values.")

        teacher_verified = any(
            position.status == "teacher_verified"
            for position in self.expected_positions
        )
        if teacher_verified:
            required_metadata = {
                "source_name": self.source_name,
                "source_reference": self.source_reference,
                "verified_by": self.verified_by,
                "verification_date": self.verification_date,
            }
            missing = [
                name
                for name, value in required_metadata.items()
                if value is None
                or (isinstance(value, str) and not value.strip())
            ]
            if self.source_type == "synthetic":
                missing.append("non-synthetic source_type")
            if self.is_synthetic:
                missing.append("is_synthetic=false")
            if missing:
                raise ValueError(
                    "teacher_verified fixtures require authoritative source metadata: "
                    + ", ".join(missing)
                )

        if self.is_synthetic and self.source_type != "synthetic":
            raise ValueError("Synthetic fixtures must use source_type 'synthetic'.")

        return self

    @property
    def is_acceptance_ready(self) -> bool:
        return (
            not self.is_synthetic
            and self.source_type != "synthetic"
            and all(
                position.status == "teacher_verified"
                for position in self.expected_positions
            )
        )


def load_reference_fixture(path: Path) -> MethodologyReferenceFixture:
    data = json.loads(path.read_text(encoding="utf-8"))
    return MethodologyReferenceFixture.model_validate(data)


def load_reference_fixtures(
    paths: Iterable[Path],
) -> tuple[MethodologyReferenceFixture, ...]:
    return tuple(
        load_reference_fixture(path)
        for path in sorted(paths, key=lambda item: item.as_posix())
    )


def acceptance_ready_fixtures(
    fixtures: Iterable[MethodologyReferenceFixture],
) -> tuple[MethodologyReferenceFixture, ...]:
    return tuple(fixture for fixture in fixtures if fixture.is_acceptance_ready)
