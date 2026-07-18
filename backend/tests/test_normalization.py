from datetime import date

import pytest

from app.matrix.calculator import MatrixCalculator
from app.matrix.normalization import (
    ConsecutiveDigitAdditionNormalizer,
    NormalizationDomainError,
)
from app.matrix.rules import (
    ConsecutiveDigitAdditionExperimentalMethodology,
    EXPERIMENTAL_METHODOLOGIES,
    UnverifiedPlaceholderMethodology,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (1, 1),
        (9, 9),
        (10, 10),
        (11, 11),
        (22, 22),
        (23, 5),
        (29, 11),
        (44, 8),
        (59, 14),
        (99, 18),
        (199, 19),
        (999, 9),
    ],
)
def test_consecutive_digit_addition_examples(raw: int, expected: int) -> None:
    assert ConsecutiveDigitAdditionNormalizer().normalize(raw) == expected


def test_consecutive_digit_addition_boundaries() -> None:
    normalizer = ConsecutiveDigitAdditionNormalizer()

    assert normalizer.normalize(1) == 1
    assert normalizer.normalize(22) == 22
    assert normalizer.normalize(23) == 5


def test_consecutive_digit_addition_multi_round_reduction() -> None:
    assert ConsecutiveDigitAdditionNormalizer().normalize(999) == 9


@pytest.mark.parametrize("raw", [0, -1, -999])
def test_consecutive_digit_addition_rejects_non_positive_integers(raw: int) -> None:
    with pytest.raises(NormalizationDomainError, match="positive integer"):
        ConsecutiveDigitAdditionNormalizer().normalize(raw)


@pytest.mark.parametrize("raw", [True, False])
def test_consecutive_digit_addition_rejects_booleans(raw: bool) -> None:
    with pytest.raises(NormalizationDomainError, match="Boolean"):
        ConsecutiveDigitAdditionNormalizer().normalize(raw)


@pytest.mark.parametrize("raw", [1.0, 29.0, "29", None, [], {}])
def test_consecutive_digit_addition_rejects_non_integer_values(raw: object) -> None:
    with pytest.raises(NormalizationDomainError, match="must be an integer"):
        ConsecutiveDigitAdditionNormalizer().normalize(raw)


def test_consecutive_digit_addition_trace_for_preserved_value() -> None:
    result = ConsecutiveDigitAdditionNormalizer().normalize_with_trace(22)

    assert result.value == 22
    assert result.calculation_trace == ["22 is within the preserved range 1–22"]


def test_consecutive_digit_addition_trace_for_single_round() -> None:
    result = ConsecutiveDigitAdditionNormalizer().normalize_with_trace(29)

    assert result.value == 11
    assert result.calculation_trace == [
        "29 is greater than 22",
        "2 + 9 = 11",
        "11 is within the preserved range 1–22",
    ]


def test_consecutive_digit_addition_trace_for_multi_round() -> None:
    result = ConsecutiveDigitAdditionNormalizer().normalize_with_trace(999)

    assert result.value == 9
    assert result.calculation_trace == [
        "999 is greater than 22",
        "9 + 9 + 9 = 27",
        "27 is greater than 22",
        "2 + 7 = 9",
        "9 is within the preserved range 1–22",
    ]


def test_consecutive_digit_addition_is_deterministic() -> None:
    normalizer = ConsecutiveDigitAdditionNormalizer()

    assert [normalizer.normalize(999) for _ in range(5)] == [9, 9, 9, 9, 9]


def test_experimental_methodology_is_registered_but_not_default() -> None:
    assert (
        EXPERIMENTAL_METHODOLOGIES["cda-experimental-v0"]
        is ConsecutiveDigitAdditionExperimentalMethodology
    )
    assert isinstance(MatrixCalculator().methodology, UnverifiedPlaceholderMethodology)


def test_experimental_methodology_remains_unverified_placeholder() -> None:
    result = ConsecutiveDigitAdditionExperimentalMethodology().calculate(
        birth_date=date(1990, 8, 16)
    )

    assert result.methodology_version == "cda-experimental-v0"
    assert {position.value for position in result.positions} == {0}
    assert {position.verified for position in result.positions} == {False}
    assert result.warnings
