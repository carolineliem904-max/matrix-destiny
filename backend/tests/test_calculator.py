import json
from datetime import date
from pathlib import Path

import pytest

from app.matrix.calculator import MatrixCalculator


def test_placeholder_methodology_matches_fixture() -> None:
    fixture = json.loads(
        (Path(__file__).parent / "fixtures" / "known_matrices.json").read_text()
    )[0]
    result = MatrixCalculator().calculate(date.fromisoformat(fixture["birth_date"]))

    assert result.methodology_version == fixture["methodology_version"]
    assert [position.id for position in result.positions] == fixture["positions"]
    assert {position.value for position in result.positions} == {
        fixture["expected_value"]
    }
    assert {position.verified for position in result.positions} == {fixture["verified"]}
    assert result.warnings


def test_future_birth_date_is_rejected() -> None:
    with pytest.raises(ValueError, match="future"):
        MatrixCalculator().calculate(date(2999, 1, 1))
