from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Sect(StrEnum):
    DAY = "day"
    NIGHT = "night"
    UNKNOWN = "unknown"


class SectSource(StrEnum):
    USER_PROVIDED = "user_provided"
    UNKNOWN = "unknown"


class SectContext(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    sect: Sect = Sect.UNKNOWN
    source: SectSource = SectSource.UNKNOWN
    weighting_rule_version: str | None = None
    interpretation_modifier_active: bool = False

    @classmethod
    def from_user_value(cls, sect: Sect = Sect.UNKNOWN) -> "SectContext":
        source = (
            SectSource.USER_PROVIDED
            if sect in (Sect.DAY, Sect.NIGHT)
            else SectSource.UNKNOWN
        )
        return cls(sect=sect, source=source)


class AstrologyInterpretationContext(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    sect_context: SectContext = Field(default_factory=SectContext)
    contrary_to_sect_malefic: str | None = None
    directly_affected_arcana: tuple[int, ...] = ()
    indirectly_affected_arcana: tuple[int, ...] = ()
    rule_version: str | None = None
    evidence_status: str = "deferred_awaiting_course_rule"
