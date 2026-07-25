import json
from copy import deepcopy
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.matrix.reference_fixtures import (
    MethodologyReferenceFixture,
    acceptance_ready_fixtures,
    load_reference_fixture,
    load_reference_fixtures,
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "synthetic_example.json"


def synthetic_fixture_data() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_valid_synthetic_fixture_is_not_acceptance_ready() -> None:
    fixture = load_reference_fixture(FIXTURE_PATH)

    assert fixture.case_name == "Synthetic schema example - not authoritative"
    assert fixture.is_synthetic is True
    assert fixture.is_acceptance_ready is False
    assert acceptance_ready_fixtures([fixture]) == ()


@pytest.mark.parametrize(
    "invalid_date",
    ["1990-02-30", "16-08-1990", "1990-8-16", "1990-08-16T00:00:00", None],
)
def test_invalid_birth_date_is_rejected(invalid_date: object) -> None:
    data = synthetic_fixture_data()
    data["birth_date"] = invalid_date

    with pytest.raises(ValidationError, match="birth_date"):
        MethodologyReferenceFixture.model_validate(data)


def test_duplicate_position_ids_are_rejected() -> None:
    data = synthetic_fixture_data()
    data["expected_positions"].append(deepcopy(data["expected_positions"][0]))

    with pytest.raises(ValidationError, match="duplicate position_id"):
        MethodologyReferenceFixture.model_validate(data)


def test_out_of_range_final_value_is_rejected() -> None:
    data = synthetic_fixture_data()
    data["expected_positions"][0]["expected_value"] = 23

    with pytest.raises(ValidationError, match="between 1 and 22"):
        MethodologyReferenceFixture.model_validate(data)


def test_teacher_verified_position_requires_source_metadata() -> None:
    data = synthetic_fixture_data()
    data["expected_positions"][0]["status"] = "teacher_verified"
    data["source_name"] = ""
    data["source_reference"] = ""

    with pytest.raises(ValidationError, match="authoritative source metadata"):
        MethodologyReferenceFixture.model_validate(data)


def test_empty_expected_positions_is_rejected() -> None:
    data = synthetic_fixture_data()
    data["expected_positions"] = []

    with pytest.raises(ValidationError, match="at least 1"):
        MethodologyReferenceFixture.model_validate(data)


def test_raw_intermediate_value_above_22_is_valid() -> None:
    data = synthetic_fixture_data()
    position = data["expected_positions"][0]
    position["expected_value"] = 29
    position["is_raw_intermediate"] = True

    fixture = MethodologyReferenceFixture.model_validate(data)

    assert fixture.expected_positions[0].expected_value == 29
    assert fixture.expected_positions[0].is_raw_intermediate is True


def test_unknown_status_is_rejected() -> None:
    data = synthetic_fixture_data()
    data["expected_positions"][0]["status"] = "probably_correct"

    with pytest.raises(ValidationError, match="teacher_verified"):
        MethodologyReferenceFixture.model_validate(data)


def test_fixture_loading_is_deterministic() -> None:
    first = load_reference_fixtures([FIXTURE_PATH])
    second = load_reference_fixtures(reversed([FIXTURE_PATH]))

    assert first == second
    assert first[0].model_dump(mode="json") == second[0].model_dump(mode="json")
