from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class NormalizationDomainError(ValueError):
    """Raised when a value cannot be normalized within the methodology domain."""


@dataclass(frozen=True)
class NormalizationResult:
    value: int
    calculation_trace: list[str]


class NormalizationStrategy(ABC):
    name: str
    version: str

    @abstractmethod
    def normalize(self, value: Any) -> int:
        """Normalize a methodology-specific integer value."""

    @abstractmethod
    def normalize_with_trace(self, value: Any) -> NormalizationResult:
        """Normalize a value and return trace lines suitable for calculation output."""


class ConsecutiveDigitAdditionNormalizer(NormalizationStrategy):
    name = "Consecutive Digit Addition"
    version = "cda-experimental-v0"
    preserved_min = 1
    preserved_max = 22

    def normalize(self, value: Any) -> int:
        return self.normalize_with_trace(value).value

    def normalize_with_trace(self, value: Any) -> NormalizationResult:
        current = self._validate(value)
        trace: list[str] = []

        while current > self.preserved_max:
            trace.append(f"{current} is greater than {self.preserved_max}")
            digits = [int(digit) for digit in str(current)]
            digit_expression = " + ".join(str(digit) for digit in digits)
            next_value = sum(digits)
            trace.append(f"{digit_expression} = {next_value}")
            current = next_value

        trace.append(
            f"{current} is within the preserved range "
            f"{self.preserved_min}–{self.preserved_max}"
        )
        return NormalizationResult(value=current, calculation_trace=trace)

    def _validate(self, value: Any) -> int:
        if isinstance(value, bool):
            raise NormalizationDomainError(
                "Boolean values are not valid normalization inputs."
            )
        if type(value) is not int:
            received = "null" if value is None else type(value).__name__
            raise NormalizationDomainError(
                f"Normalization value must be an integer; received {received}."
            )
        if value <= 0:
            raise NormalizationDomainError(
                "Normalization value must be a positive integer."
            )
        return value
