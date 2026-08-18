import json
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.matrix.arcana_profiles import (
    MAHESA_GANTARI_RWS_ARCANA,
    get_mahesa_gantari_arcana,
)
from app.matrix.astrology import Sect, SectSource
from app.matrix.calculator import MatrixCalculator
from app.matrix.mahesa_gantari import (
    COURSE_METHODOLOGIES,
    CourseLine,
    FormulaEvidence,
    MahesaGantariCalculationRequest,
    MahesaGantariRwsMethodology,
)
from app.matrix.rules import (
    ConsecutiveDigitAdditionExperimentalMethodology,
    TeacherTeaserMethodology,
    UnverifiedPlaceholderMethodology,
)

FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "mahesa_gantari_1988_08_18.json"
)
HEALTH_FIXTURE_PATH = (
    Path(__file__).parent
    / "fixtures"
    / "mahesa_gantari_1990_08_16.json"
)


def fixture_data() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def health_fixture_data() -> dict:
    return json.loads(HEALTH_FIXTURE_PATH.read_text(encoding="utf-8"))


def point_values(result) -> dict[str, int]:
    return {point.position_id: point.value for point in result.points}


def purpose_values(result) -> dict[str, int]:
    return {
        "earth": result.purpose.earth.value,
        "sky": result.purpose.sky.value,
        "soul_searching": result.purpose.soul_searching.value,
        "male": result.purpose.male.value,
        "female": result.purpose.female.value,
        "socialization": result.purpose.socialization.value,
        "spiritual_knowledge": result.purpose.spiritual_knowledge.value,
    }


def test_course_fixture_all_points_and_purpose_values() -> None:
    fixture = fixture_data()
    result = MahesaGantariRwsMethodology().calculate(date(1988, 8, 18))

    assert point_values(result) == fixture["expected_points"]
    assert purpose_values(result) == fixture["expected_purpose"]
    assert result.methodology_version == fixture["methodology_version"]
    assert result.status == fixture["status"]
    assert result.verified is fixture["verified"] is False


@pytest.mark.parametrize(
    ("line_name", "ordered_ids"),
    [
        ("money_line", ("L", "L_plus_N", "N")),
        ("relationship_line", ("M", "M_plus_N", "N")),
        ("karmic_tail", ("M", "D_plus_M", "D")),
        ("deepest_desire", ("O", "E_plus_O")),
        ("male_generation", ("F", "H")),
        ("female_generation", ("G", "I")),
    ],
)
def test_course_fixture_ordered_domain_lines(
    line_name: str,
    ordered_ids: tuple[str, ...],
) -> None:
    fixture = fixture_data()
    result = MahesaGantariRwsMethodology().calculate(date(1988, 8, 18))
    line = getattr(result, line_name)

    assert line.ordered_point_ids == ordered_ids
    assert list(line.values) == fixture["expected_lines"][line_name]
    assert line.evidence.verified is False


def test_relationship_and_karmic_tail_remain_distinct_objects() -> None:
    result = MahesaGantariRwsMethodology().calculate(date(1988, 8, 18))

    assert result.relationship_line.values == result.karmic_tail.values
    assert result.relationship_line.line_id != result.karmic_tail.line_id
    assert (
        result.relationship_line.ordered_point_ids
        != result.karmic_tail.ordered_point_ids
    )
    assert (
        result.relationship_line.component_labels
        != result.karmic_tail.component_labels
    )


def test_course_calculation_traces_and_evidence_metadata() -> None:
    result = MahesaGantariRwsMethodology().calculate(date(1988, 8, 18))
    points = {point.position_id: point for point in result.points}

    assert points["C"].calculation_trace[:3] == (
        "Year digits: 1 + 9 + 8 + 8 = 26",
        "26 is greater than 22",
        "2 + 6 = 8",
    )
    assert points["O"].calculation_trace[:3] == (
        "F + G + H + I = 8 + 16 + 15 + 7 = 46",
        "46 is greater than 22",
        "4 + 6 = 10",
    )
    assert all(point.calculation_trace for point in result.points)
    assert all(
        point.evidence.methodology_version == "mahesa-gantari-rws-v0.1"
        and point.evidence.source_document
        and point.evidence.source_page > 0
        and point.evidence.evidence_status
        and point.evidence.verified is False
        for point in result.points
    )
    assert result.purpose.male.evidence.evidence_status == (
        "reconstructed_from_course_diagram"
    )
    assert result.purpose.female.evidence.evidence_status == (
        "reconstructed_from_course_diagram"
    )
    assert result.purpose.male.evidence.verified is False
    assert result.purpose.female.evidence.verified is False


def test_e_plus_j_is_reconstructed_with_trace() -> None:
    fixture = health_fixture_data()
    result = MahesaGantariRwsMethodology().calculate(date(1990, 8, 16))
    point = {item.position_id: item for item in result.points}["E_plus_J"]

    assert point.value == fixture["expected_e_plus_j"]
    assert point.calculation_trace[:3] == (
        "E + J = 5 + 21 = 26",
        "26 is greater than 22",
        "2 + 6 = 8",
    )
    assert point.evidence.evidence_status == "reconstructed_from_reference_diagram"
    assert point.evidence.verified is False
    assert len(result.points) == fixture["expected_point_count"]


def health_values(result) -> dict[str, tuple[int, int, int]]:
    return {
        row.row_id: (row.physics.value, row.energy.value, row.emotions.value)
        for row in result.health_card.rows
    }


def test_health_card_fixture_values_order_and_evidence() -> None:
    fixture = health_fixture_data()
    result = MahesaGantariRwsMethodology().calculate(date(1990, 8, 16))

    assert [row.row_id for row in result.health_card.rows] == [
        "sahasrara",
        "ajna",
        "vishuddha",
        "anahata",
        "manipura",
        "svadhisthana",
        "muladhara",
    ]
    assert health_values(result) == {
        row_id: tuple(values)
        for row_id, values in fixture["expected_health_card"].items()
    }
    assert (
        result.health_card.result.physics.value,
        result.health_card.result.energy.value,
        result.health_card.result.emotions.value,
    ) == tuple(fixture["expected_result"])
    cells = [
        cell
        for row in result.health_card.rows
        for cell in (row.physics, row.energy, row.emotions)
    ] + [
        result.health_card.result.physics,
        result.health_card.result.energy,
        result.health_card.result.emotions,
    ]
    assert all(cell.calculation_trace for cell in cells)
    assert all(cell.verified is False for cell in cells)
    assert all(cell.evidence.verified is False for cell in cells)
    assert all(
        cell.evidence.evidence_status
        == "reconstructed_from_reference_health_card"
        for cell in cells
    )
    assert result.health_card.rows[4].emotions.formula == "normalize(E + E)"
    assert result.health_card.rows[4].emotions.calculation_trace[0] == "E + E = 5 + 5 = 10"


def test_sect_does_not_affect_health_card() -> None:
    methodology = MahesaGantariRwsMethodology()
    day = methodology.calculate(date(1990, 8, 16), Sect.DAY)
    night = methodology.calculate(date(1990, 8, 16), Sect.NIGHT)
    unknown = methodology.calculate(date(1990, 8, 16), Sect.UNKNOWN)

    assert health_values(day) == health_values(night) == health_values(unknown)
    assert day.health_card.result == night.health_card.result == unknown.health_card.result


def line_evidence() -> FormulaEvidence:
    return FormulaEvidence(
        source_page=41,
        evidence_status="explicitly_stated_in_course",
    )


def test_course_line_accepts_matching_unique_components() -> None:
    line = CourseLine(
        line_id="example",
        ordered_point_ids=("A", "B"),
        values=(1, 2),
        component_labels=("first", "second"),
        evidence=line_evidence(),
    )

    assert line.ordered_point_ids == ("A", "B")


@pytest.mark.parametrize(
    ("ordered_ids", "values", "labels", "message"),
    [
        ((), (), (), "at least one component"),
        (("A", "B"), (1,), ("first", "second"), "equal lengths"),
        (("A", "B"), (1, 2), ("first",), "equal lengths"),
        (("A", "A"), (1, 1), ("first", "again"), "must not contain duplicates"),
    ],
)
def test_course_line_rejects_invalid_component_structure(
    ordered_ids: tuple[str, ...],
    values: tuple[int, ...],
    labels: tuple[str, ...],
    message: str,
) -> None:
    with pytest.raises(ValidationError, match=message):
        CourseLine(
            line_id="invalid",
            ordered_point_ids=ordered_ids,
            values=values,
            component_labels=labels,
            evidence=line_evidence(),
        )


def test_course_methodology_uses_shared_normalizer_rules() -> None:
    methodology = MahesaGantariRwsMethodology()

    assert methodology.normalizer.normalize(11) == 11
    assert methodology.normalizer.normalize(22) == 22
    assert methodology.normalizer.normalize(999) == 9
    assert {point.value for point in methodology.calculate(date(1988, 8, 18)).points} <= set(
        range(1, 23)
    )


def test_rws_arcana_profile_is_complete_unique_and_reference_only() -> None:
    energies = [arcana.energy_number for arcana in MAHESA_GANTARI_RWS_ARCANA]
    names = [arcana.arcana_name for arcana in MAHESA_GANTARI_RWS_ARCANA]

    assert energies == list(range(1, 23))
    assert 0 not in energies
    assert len(energies) == len(set(energies)) == 22
    assert len(names) == len(set(names)) == 22
    assert get_mahesa_gantari_arcana(8).arcana_name == "Strength"
    assert get_mahesa_gantari_arcana(11).arcana_name == "Justice"
    assert get_mahesa_gantari_arcana(22).arcana_name == "The Fool"
    assert all(
        arcana.tarot_profile == "rws-mahesa-gantari-v0.1"
        and arcana.publication_status == "reference_only"
        and arcana.source_metadata.verified is False
        for arcana in MAHESA_GANTARI_RWS_ARCANA
    )


@pytest.mark.parametrize("energy", [0, -1, 23, True, "8", None])
def test_arcana_profile_rejects_invalid_energy(energy: object) -> None:
    with pytest.raises(ValueError, match="1 through 22"):
        get_mahesa_gantari_arcana(energy)  # type: ignore[arg-type]


def test_arcana_associations_are_structured_and_not_weighted() -> None:
    strength = get_mahesa_gantari_arcana(8)
    tower = get_mahesa_gantari_arcana(16)

    assert strength.astrology_associations.zodiac_association == "Leo"
    assert strength.astrology_associations.direct_planet_association is None
    assert tower.astrology_associations.direct_planet_association == "Mars"
    assert tower.astrology_associations.interpretation_modifier is None
    assert strength.in_plus == ()
    assert strength.in_minus == ()


def test_missing_sect_defaults_to_unknown() -> None:
    request = MahesaGantariCalculationRequest(birth_date=date(1988, 8, 18))
    result = MahesaGantariRwsMethodology().calculate(
        request.birth_date,
        request.sect,
    )

    assert request.sect == Sect.UNKNOWN
    assert result.sect_context.sect == Sect.UNKNOWN
    assert result.sect_context.source == SectSource.UNKNOWN
    assert result.sect_context.interpretation_modifier_active is False
    assert result.sect_context.weighting_rule_version is None


@pytest.mark.parametrize("sect", [Sect.DAY, Sect.NIGHT])
def test_user_provided_day_or_night_sect_is_accepted(sect: Sect) -> None:
    request = MahesaGantariCalculationRequest(
        birth_date=date(1988, 8, 18),
        sect=sect,
    )
    result = MahesaGantariRwsMethodology().calculate(
        request.birth_date,
        request.sect,
    )

    assert result.sect_context.sect == sect
    assert result.sect_context.source == SectSource.USER_PROVIDED
    assert result.sect_context.interpretation_modifier_active is False


def test_invalid_sect_is_rejected() -> None:
    with pytest.raises(ValidationError):
        MahesaGantariCalculationRequest(
            birth_date=date(1988, 8, 18),
            sect="sunrise",  # type: ignore[arg-type]
        )


def test_sect_never_changes_matrix_values() -> None:
    methodology = MahesaGantariRwsMethodology()
    unknown = methodology.calculate(date(1988, 8, 18), Sect.UNKNOWN)
    day = methodology.calculate(date(1988, 8, 18), Sect.DAY)
    night = methodology.calculate(date(1988, 8, 18), Sect.NIGHT)

    assert point_values(unknown) == point_values(day) == point_values(night)
    assert unknown.money_line.values == day.money_line.values == night.money_line.values
    assert purpose_values(unknown) == purpose_values(day) == purpose_values(night)


def test_course_methodology_is_registered_without_replacing_history() -> None:
    assert (
        COURSE_METHODOLOGIES["mahesa-gantari-rws-v0.1"]
        is MahesaGantariRwsMethodology
    )
    assert UnverifiedPlaceholderMethodology.version == "unverified-v0"
    assert (
        ConsecutiveDigitAdditionExperimentalMethodology.version
        == "cda-experimental-v0"
    )
    assert TeacherTeaserMethodology.version == "teacher-teaser-v0.1"
    assert isinstance(MatrixCalculator().methodology, UnverifiedPlaceholderMethodology)


def test_historical_teacher_teaser_fixture_still_matches() -> None:
    result = TeacherTeaserMethodology().calculate(date(1989, 12, 13))
    values = {position.id: position.value for position in result.positions}

    assert values["A"] == 13
    assert values["E"] == 5
    assert {position.verified for position in result.positions} == {False}
