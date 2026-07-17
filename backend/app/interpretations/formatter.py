from app.interpretations.repository import InterpretationRepository
from app.matrix.models import (
    InterpretedPosition,
    LanguageCode,
    MatrixCalculation,
    ReadingResponse,
)

DISCLAIMERS: dict[LanguageCode, str] = {
    "en": (
        "This reading is for reflection, education, and entertainment. It is not "
        "scientific proof, professional advice, or a guarantee of future outcomes."
    ),
    "id": (
        "Bacaan ini untuk refleksi, edukasi, dan hiburan. Ini bukan bukti ilmiah, "
        "nasihat profesional, atau jaminan hasil di masa depan."
    ),
}

SUMMARY: dict[LanguageCode, str] = {
    "en": (
        "Your chart is currently generated with an unverified placeholder methodology. "
        "Use the sections below to review the structure and sample interpretation flow, "
        "not as a final Destiny Matrix reading."
    ),
    "id": (
        "Bagan ini saat ini dibuat dengan metodologi placeholder yang belum terverifikasi. "
        "Gunakan bagian di bawah untuk meninjau struktur dan alur interpretasi contoh, "
        "bukan sebagai bacaan Destiny Matrix final."
    ),
}


class ReadingComposer:
    def __init__(self, repository: InterpretationRepository) -> None:
        self.repository = repository

    def compose(
        self,
        calculation: MatrixCalculation,
        language: LanguageCode,
        name: str | None,
        focus: str | None,
    ) -> ReadingResponse:
        interpreted = []
        for position in calculation.positions:
            role = self.repository.get_position(position.id, language)
            energy = (
                self.repository.get_energy(position.value, language)
                if position.value > 0
                else None
            )
            interpreted.append(
                InterpretedPosition(position=position, role=role, energy=energy)
            )

        return ReadingResponse(
            methodology_version=calculation.methodology_version,
            birth_date=calculation.birth_date,
            language=language,
            name=name,
            focus=focus,
            positions=interpreted,
            summary=SUMMARY[language],
            warnings=calculation.warnings,
            disclaimer=DISCLAIMERS[language],
        )
