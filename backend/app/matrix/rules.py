from abc import ABC, abstractmethod
from datetime import date

from app.matrix.normalization import ConsecutiveDigitAdditionNormalizer
from app.matrix.models import ChartCoordinates, MatrixCalculation, MatrixPosition
from app.matrix.positions import POSITION_DEFINITIONS

TEACHER_TEASER_SUPPORTED_POSITIONS: tuple[str, ...] = (
    "A",
    "B",
    "C",
    "D",
    "E",
    "earth_line",
    "sky_line",
    "top_left",
    "top_right",
    "bottom_right",
    "bottom_left",
)

TEACHER_TEASER_POSITION_LABELS: dict[str, str] = {
    "A": "Birth Day",
    "B": "Birth Month",
    "C": "Birth Year",
    "D": "Foundation",
    "E": "Soul Searching",
    "earth_line": "Earth Line",
    "sky_line": "Sky Line",
    "top_left": "Top Left",
    "top_right": "Top Right",
    "bottom_right": "Bottom Right",
    "bottom_left": "Bottom Left",
}


class MatrixMethodology(ABC):
    version: str

    @abstractmethod
    def calculate(self, birth_date: date) -> MatrixCalculation:
        """Return deterministic matrix positions for a birth date."""


class UnverifiedPlaceholderMethodology(MatrixMethodology):
    version = "unverified-v0"

    def calculate(self, birth_date: date) -> MatrixCalculation:
        positions = [
            MatrixPosition(
                id=definition.id,
                label=definition.labels["en"],
                value=0,
                verified=False,
                calculation_trace=[
                    "Placeholder: final formula has not been provided",
                    f"Methodology version: {self.version}",
                ],
                coordinates=ChartCoordinates(x=definition.x, y=definition.y),
                interpretation_key=definition.interpretation_key,
            )
            for definition in POSITION_DEFINITIONS
        ]

        return MatrixCalculation(
            methodology_version=self.version,
            birth_date=birth_date,
            positions=positions,
            warnings=[
                "The methodology is incomplete and these values must not be treated as final."
            ],
        )


class ConsecutiveDigitAdditionExperimentalMethodology(MatrixMethodology):
    version = "cda-experimental-v0"

    def __init__(self) -> None:
        self.normalizer = ConsecutiveDigitAdditionNormalizer()

    def calculate(self, birth_date: date) -> MatrixCalculation:
        positions = [
            MatrixPosition(
                id=definition.id,
                label=definition.labels["en"],
                value=0,
                verified=False,
                calculation_trace=[
                    "Experimental normalizer is registered, but position formulas have not been provided.",
                    f"Normalizer: {self.normalizer.name}",
                    f"Methodology version: {self.version}",
                ],
                coordinates=ChartCoordinates(x=definition.x, y=definition.y),
                interpretation_key=definition.interpretation_key,
            )
            for definition in POSITION_DEFINITIONS
        ]

        return MatrixCalculation(
            methodology_version=self.version,
            birth_date=birth_date,
            positions=positions,
            warnings=[
                "Consecutive Digit Addition is experimental and awaiting comparison with the August course methodology.",
                "Position formulas are incomplete and these values must not be treated as final.",
            ],
        )


class TeacherTeaserMethodology(MatrixMethodology):
    version = "teacher-teaser-v0.1"
    status = "transcribed_from_teacher_material"

    def __init__(self) -> None:
        self.normalizer = ConsecutiveDigitAdditionNormalizer()

    def _position(
        self,
        position_id: str,
        raw_value: int,
        trace_prefix: list[str],
        trace_suffix: list[str] | None = None,
    ) -> MatrixPosition:
        normalized = self.normalizer.normalize_with_trace(raw_value)
        return MatrixPosition(
            id=position_id,
            label=TEACHER_TEASER_POSITION_LABELS[position_id],
            value=normalized.value,
            verified=False,
            calculation_trace=[
                *trace_prefix,
                *normalized.calculation_trace,
                *(trace_suffix or []),
            ],
            coordinates=None,
            interpretation_key=None,
        )

    def calculate(self, birth_date: date) -> MatrixCalculation:
        a = self._position(
            "A",
            birth_date.day,
            [f"Birth day = {birth_date.day}"],
        )
        b = self._position(
            "B",
            birth_date.month,
            [f"Birth month = {birth_date.month}"],
        )

        year_digits = [int(digit) for digit in f"{birth_date.year:04d}"]
        year_sum = sum(year_digits)
        c = self._position(
            "C",
            year_sum,
            [
                "Year digits: "
                + " + ".join(str(digit) for digit in year_digits)
                + f" = {year_sum}"
            ],
        )

        foundation_sum = a.value + b.value + c.value
        d = self._position(
            "D",
            foundation_sum,
            [
                f"A + B + C = {a.value} + {b.value} + {c.value} "
                f"= {foundation_sum}"
            ],
        )

        earth_sum = a.value + c.value
        earth_line = self._position(
            "earth_line",
            earth_sum,
            [f"A + C = {a.value} + {c.value} = {earth_sum}"],
        )

        sky_sum = b.value + d.value
        sky_line = self._position(
            "sky_line",
            sky_sum,
            [f"B + D = {b.value} + {d.value} = {sky_sum}"],
        )

        center_sum = earth_line.value + sky_line.value
        equivalent_center_sum = a.value + b.value + c.value + d.value
        e = self._position(
            "E",
            center_sum,
            [
                "Earth Line + Sky Line = "
                f"{earth_line.value} + {sky_line.value} = {center_sum}"
            ],
            [
                "Equivalent under this normalizer: "
                f"A + B + C + D = {a.value} + {b.value} + "
                f"{c.value} + {d.value} = {equivalent_center_sum}"
            ],
        )

        corner_inputs = (
            ("top_left", "A + B", a.value, b.value),
            ("top_right", "B + C", b.value, c.value),
            ("bottom_right", "C + D", c.value, d.value),
            ("bottom_left", "D + A", d.value, a.value),
        )
        corners = [
            self._position(
                position_id,
                left_value + right_value,
                [
                    f"{expression} = {left_value} + {right_value} "
                    f"= {left_value + right_value}"
                ],
            )
            for position_id, expression, left_value, right_value in corner_inputs
        ]

        positions_by_id = {
            position.id: position
            for position in (
                a,
                b,
                c,
                d,
                e,
                earth_line,
                sky_line,
                *corners,
            )
        }
        return MatrixCalculation(
            methodology_version=self.version,
            birth_date=birth_date,
            positions=[
                positions_by_id[position_id]
                for position_id in TEACHER_TEASER_SUPPORTED_POSITIONS
            ],
            warnings=[
                "This provisional methodology is transcribed from teacher teaser material and is not teacher-verified.",
                "Only explicitly supported positions are calculated; internal nodes and forecast outputs remain unsupported.",
            ],
        )


EXPERIMENTAL_METHODOLOGIES: dict[str, type[MatrixMethodology]] = {
    ConsecutiveDigitAdditionExperimentalMethodology.version: ConsecutiveDigitAdditionExperimentalMethodology
}

PROVISIONAL_METHODOLOGIES: dict[str, type[MatrixMethodology]] = {
    TeacherTeaserMethodology.version: TeacherTeaserMethodology
}
