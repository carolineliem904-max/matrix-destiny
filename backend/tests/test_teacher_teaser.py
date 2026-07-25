from datetime import date
from pathlib import Path

import pytest

from app.matrix.calculator import MatrixCalculator
from app.matrix.compatibility import (
    CompatibilityCalculation,
    MissingCompatibilityPositionError,
    TeacherTeaserCompatibilityComposer,
    UnsupportedCompatibilityPositionError,
)
from app.matrix.models import MatrixCalculation
from app.matrix.reference_fixtures import (
    CompatibilityReferenceFixture,
    MethodologyReferenceFixture,
    load_compatibility_reference_fixture,
    load_reference_fixture,
)
from app.matrix.rules import (
    PROVISIONAL_METHODOLOGIES,
    TEACHER_TEASER_SUPPORTED_POSITIONS,
    TeacherTeaserMethodology,
    UnverifiedPlaceholderMethodology,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"
TAYLOR_FIXTURE_PATH = FIXTURES_DIR / "teacher_teaser_taylor_swift.json"
TRAVIS_FIXTURE_PATH = FIXTURES_DIR / "teacher_teaser_travis_kelce.json"
COMPATIBILITY_FIXTURE_PATH = (
    FIXTURES_DIR / "teacher_teaser_compatibility.json"
)


def values_by_id(
    calculation: MatrixCalculation | CompatibilityCalculation,
) -> dict[str, int]:
    return {
        position.id: position.value
        for position in calculation.positions
    }


def expected_values(
    fixture: MethodologyReferenceFixture | CompatibilityReferenceFixture,
) -> dict[str, int]:
    return {
        position.position_id: position.expected_value
        for position in fixture.expected_positions
    }


@pytest.mark.parametrize(
    "fixture_path",
    [TAYLOR_FIXTURE_PATH, TRAVIS_FIXTURE_PATH],
)
def test_personal_reference_fixture(fixture_path: Path) -> None:
    fixture = load_reference_fixture(fixture_path)
    result = TeacherTeaserMethodology().calculate(fixture.birth_date)

    assert values_by_id(result) == expected_values(fixture)
    assert {position.verified for position in result.positions} == {False}
    assert fixture.is_acceptance_ready is False


def test_all_and_only_supported_personal_positions_are_calculated() -> None:
    result = TeacherTeaserMethodology().calculate(date(1989, 12, 13))

    assert tuple(position.id for position in result.positions) == (
        TEACHER_TEASER_SUPPORTED_POSITIONS
    )
    assert all(position.coordinates is None for position in result.positions)
    assert all(
        position.interpretation_key is None for position in result.positions
    )


def test_all_supported_compatibility_positions_match_fixture() -> None:
    methodology = TeacherTeaserMethodology()
    taylor = methodology.calculate(date(1989, 12, 13))
    travis = methodology.calculate(date(1989, 10, 5))
    result = TeacherTeaserCompatibilityComposer().compose(taylor, travis)
    fixture = load_compatibility_reference_fixture(COMPATIBILITY_FIXTURE_PATH)

    assert values_by_id(result) == expected_values(fixture)
    assert tuple(position.id for position in result.positions) == (
        TEACHER_TEASER_SUPPORTED_POSITIONS
    )
    assert {position.verified for position in result.positions} == {False}
    assert all(position.calculation_trace for position in result.positions)
    assert {
        position.position_id
        for position in fixture.expected_positions
        if position.status == "inferred"
    } == {"earth_line", "sky_line"}
    assert fixture.is_acceptance_ready is False


def test_taylor_calculation_traces_include_supplied_examples() -> None:
    result = TeacherTeaserMethodology().calculate(date(1989, 12, 13))
    positions = {position.id: position for position in result.positions}

    assert positions["C"].calculation_trace[:3] == [
        "Year digits: 1 + 9 + 8 + 9 = 27",
        "27 is greater than 22",
        "2 + 7 = 9",
    ]
    assert positions["D"].calculation_trace[:3] == [
        "A + B + C = 13 + 12 + 9 = 34",
        "34 is greater than 22",
        "3 + 4 = 7",
    ]
    assert positions["E"].calculation_trace[:3] == [
        "Earth Line + Sky Line = 22 + 19 = 41",
        "41 is greater than 22",
        "4 + 1 = 5",
    ]
    assert "A + B + C + D = 13 + 12 + 9 + 7 = 41" in (
        positions["E"].calculation_trace[-1]
    )
    assert all(position.calculation_trace for position in result.positions)


def test_personal_and_compatibility_calculations_are_deterministic() -> None:
    methodology = TeacherTeaserMethodology()
    composer = TeacherTeaserCompatibilityComposer()

    first_personal = methodology.calculate(date(1989, 12, 13))
    second_personal = methodology.calculate(date(1989, 12, 13))
    first_compatibility = composer.compose(
        first_personal,
        methodology.calculate(date(1989, 10, 5)),
    )
    second_compatibility = composer.compose(
        second_personal,
        methodology.calculate(date(1989, 10, 5)),
    )

    assert first_personal == second_personal
    assert first_compatibility == second_compatibility


def test_leap_day_birth_date() -> None:
    result = TeacherTeaserMethodology().calculate(date(2000, 2, 29))

    assert values_by_id(result)["A"] == 11
    assert values_by_id(result)["B"] == 2


def test_century_containing_year_sums_each_digit() -> None:
    result = TeacherTeaserMethodology().calculate(date(2000, 1, 1))
    position_c = next(position for position in result.positions if position.id == "C")

    assert position_c.value == 2
    assert position_c.calculation_trace[0] == "Year digits: 2 + 0 + 0 + 0 = 2"


def test_personal_inputs_in_preserved_range_remain_unchanged() -> None:
    result = TeacherTeaserMethodology().calculate(date(2001, 11, 22))
    values = values_by_id(result)

    assert values["A"] == 22
    assert values["B"] == 11


def test_methodology_uses_existing_multi_round_normalizer() -> None:
    methodology = TeacherTeaserMethodology()

    assert methodology.normalizer.normalize(999) == 9


def test_unsupported_compatibility_position_is_rejected() -> None:
    methodology = TeacherTeaserMethodology()
    taylor = methodology.calculate(date(1989, 12, 13))
    travis = methodology.calculate(date(1989, 10, 5))

    with pytest.raises(
        UnsupportedCompatibilityPositionError,
        match="money_line",
    ):
        TeacherTeaserCompatibilityComposer().compose(
            taylor,
            travis,
            position_ids=["money_line"],
        )


def test_missing_supported_compatibility_position_is_rejected() -> None:
    methodology = TeacherTeaserMethodology()
    taylor = methodology.calculate(date(1989, 12, 13))
    travis = methodology.calculate(date(1989, 10, 5))
    incomplete_taylor = taylor.model_copy(
        update={
            "positions": [
                position for position in taylor.positions if position.id != "A"
            ]
        }
    )

    with pytest.raises(MissingCompatibilityPositionError, match="A"):
        TeacherTeaserCompatibilityComposer().compose(
            incomplete_taylor,
            travis,
        )


def test_compatibility_is_symmetric_for_input_order() -> None:
    methodology = TeacherTeaserMethodology()
    taylor = methodology.calculate(date(1989, 12, 13))
    travis = methodology.calculate(date(1989, 10, 5))
    composer = TeacherTeaserCompatibilityComposer()

    forward = composer.compose(taylor, travis)
    reverse = composer.compose(travis, taylor)

    assert forward.positions == reverse.positions


def test_methodology_version_status_and_registration() -> None:
    methodology = TeacherTeaserMethodology()
    result = methodology.calculate(date(1989, 12, 13))

    assert methodology.version == "teacher-teaser-v0.1"
    assert methodology.status == "transcribed_from_teacher_material"
    assert result.methodology_version == methodology.version
    assert (
        PROVISIONAL_METHODOLOGIES[methodology.version]
        is TeacherTeaserMethodology
    )


def test_teacher_teaser_is_not_the_public_default() -> None:
    assert isinstance(MatrixCalculator().methodology, UnverifiedPlaceholderMethodology)
    assert not isinstance(MatrixCalculator().methodology, TeacherTeaserMethodology)
