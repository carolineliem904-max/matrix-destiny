from datetime import date

from app.matrix.models import MatrixCalculation
from app.matrix.rules import MatrixMethodology, UnverifiedPlaceholderMethodology
from app.matrix.validator import validate_birth_date


class MatrixCalculator:
    def __init__(self, methodology: MatrixMethodology | None = None) -> None:
        self.methodology = methodology or UnverifiedPlaceholderMethodology()

    def calculate(self, birth_date: date) -> MatrixCalculation:
        validate_birth_date(birth_date)
        return self.methodology.calculate(birth_date)
