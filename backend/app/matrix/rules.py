from abc import ABC, abstractmethod
from datetime import date

from app.matrix.models import ChartCoordinates, MatrixCalculation, MatrixPosition
from app.matrix.positions import POSITION_DEFINITIONS


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
