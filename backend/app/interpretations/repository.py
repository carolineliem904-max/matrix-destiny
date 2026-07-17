import json
from functools import lru_cache
from pathlib import Path

from app.matrix.models import EnergyInterpretation, LanguageCode, PositionInterpretation

DATA_DIR = Path(__file__).parent / "data"


class InterpretationRepository:
    def get_energy(
        self, energy: int, language: LanguageCode
    ) -> EnergyInterpretation | None:
        return self._load_energies(language).get(energy)

    def get_position(
        self, position_id: str, language: LanguageCode
    ) -> PositionInterpretation | None:
        return self._load_positions(language).get(position_id)

    @staticmethod
    @lru_cache
    def _load_energies(language: LanguageCode) -> dict[int, EnergyInterpretation]:
        path = DATA_DIR / f"energies.{language}.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        return {
            item["energy"]: EnergyInterpretation.model_validate(item)
            for item in records
        }

    @staticmethod
    @lru_cache
    def _load_positions(language: LanguageCode) -> dict[str, PositionInterpretation]:
        path = DATA_DIR / f"positions.{language}.json"
        records = json.loads(path.read_text(encoding="utf-8"))
        return {item["id"]: PositionInterpretation.model_validate(item) for item in records}
