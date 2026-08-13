from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ArcanaSourceMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_document: str
    source_page: int
    evidence_status: str
    verified: bool = False


class AstrologyAssociations(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    direct_planet_association: str | None = None
    zodiac_association: str | None = None
    zodiac_ruler_derived: tuple[str, ...] = ()
    house_association: tuple[int, ...] = ()
    interpretation_modifier: str | None = None


class ArcanaContent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    energy_number: int = Field(ge=1, le=22)
    arcana_name: str
    tarot_profile: Literal["rws-mahesa-gantari-v0.1"]
    neutral_keywords: tuple[str, ...]
    in_plus: tuple[str, ...] = ()
    in_minus: tuple[str, ...] = ()
    karmic_tasks: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    astrology_associations: AstrologyAssociations
    source_metadata: ArcanaSourceMetadata
    language: Literal["en"] = "en"
    publication_status: Literal["reference_only"] = "reference_only"


_SOURCE = ArcanaSourceMetadata(
    source_document="Matrix of Destiny Basic 01 - Akademi Mahesa Gantari (2026)",
    source_page=12,
    evidence_status="explicitly_stated_in_course",
    verified=False,
)

_ARCANA_ROWS = (
    (1, "The Magician", "Mercury", None, ("initiative", "resourcefulness")),
    (2, "The High Priestess", "Moon", None, ("intuition", "reflection")),
    (3, "The Empress", "Venus", None, ("nurture", "creativity")),
    (4, "The Emperor", "Mars", None, ("structure", "leadership")),
    (5, "The Hierophant", None, "Taurus", ("tradition", "learning")),
    (6, "The Lovers", None, "Gemini", ("choice", "connection")),
    (7, "The Chariot", None, "Cancer", ("direction", "resolve")),
    (8, "Strength", None, "Leo", ("courage", "self-command")),
    (9, "The Hermit", None, "Virgo", ("discernment", "solitude")),
    (10, "Wheel of Fortune", "Jupiter", None, ("cycles", "change")),
    (11, "Justice", None, "Libra", ("balance", "accountability")),
    (12, "The Hanged Man", "Neptune", None, ("pause", "perspective")),
    (13, "Death", None, "Scorpio", ("transition", "release")),
    (14, "Temperance", None, "Sagittarius", ("integration", "moderation")),
    (15, "The Devil", None, "Capricorn", ("attachment", "material focus")),
    (16, "The Tower", "Mars", None, ("disruption", "restructuring")),
    (17, "The Star", None, "Aquarius", ("hope", "renewal")),
    (18, "The Moon", None, "Pisces", ("uncertainty", "imagination")),
    (19, "The Sun", "Sun", None, ("clarity", "vitality")),
    (20, "Judgement", "Pluto", None, ("review", "awakening")),
    (21, "The World", "Saturn", None, ("completion", "integration")),
    (22, "The Fool", "Uranus", None, ("beginning", "openness")),
)

MAHESA_GANTARI_RWS_ARCANA: tuple[ArcanaContent, ...] = tuple(
    ArcanaContent(
        energy_number=energy,
        arcana_name=name,
        tarot_profile="rws-mahesa-gantari-v0.1",
        neutral_keywords=keywords,
        astrology_associations=AstrologyAssociations(
            direct_planet_association=planet,
            zodiac_association=zodiac,
        ),
        source_metadata=_SOURCE,
    )
    for energy, name, planet, zodiac, keywords in _ARCANA_ROWS
)

MAHESA_GANTARI_RWS_ARCANA_BY_ENERGY = {
    arcana.energy_number: arcana for arcana in MAHESA_GANTARI_RWS_ARCANA
}


def get_mahesa_gantari_arcana(energy: int) -> ArcanaContent:
    if type(energy) is not int or energy not in MAHESA_GANTARI_RWS_ARCANA_BY_ENERGY:
        raise ValueError("Arcana energy must be an integer from 1 through 22.")
    return MAHESA_GANTARI_RWS_ARCANA_BY_ENERGY[energy]
