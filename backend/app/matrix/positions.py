from dataclasses import dataclass


@dataclass(frozen=True)
class PositionDefinition:
    id: str
    labels: dict[str, str]
    x: float
    y: float
    interpretation_key: str


POSITION_DEFINITIONS: tuple[PositionDefinition, ...] = (
    PositionDefinition(
        id="center",
        labels={"en": "Central Energy", "id": "Energi Pusat"},
        x=50,
        y=50,
        interpretation_key="center",
    ),
    PositionDefinition(
        id="portrait",
        labels={"en": "Portrait", "id": "Potret Diri"},
        x=50,
        y=16,
        interpretation_key="portrait",
    ),
    PositionDefinition(
        id="talents",
        labels={"en": "Talents", "id": "Bakat"},
        x=78,
        y=32,
        interpretation_key="talents",
    ),
    PositionDefinition(
        id="relationship_line",
        labels={"en": "Relationship Line", "id": "Garis Relasi"},
        x=78,
        y=68,
        interpretation_key="relationship_line",
    ),
    PositionDefinition(
        id="money_line",
        labels={"en": "Money Line", "id": "Garis Uang"},
        x=50,
        y=84,
        interpretation_key="money_line",
    ),
    PositionDefinition(
        id="ancestral_line",
        labels={"en": "Ancestral Line", "id": "Garis Leluhur"},
        x=22,
        y=68,
        interpretation_key="ancestral_line",
    ),
    PositionDefinition(
        id="karmic_tail",
        labels={"en": "Karmic Tail", "id": "Ekor Karmis"},
        x=22,
        y=32,
        interpretation_key="karmic_tail",
    ),
)
