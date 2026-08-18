from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.matrix.astrology import Sect, SectContext
from app.matrix.arcana_profiles import get_mahesa_gantari_arcana
from app.matrix.normalization import ConsecutiveDigitAdditionNormalizer
from app.matrix.validator import validate_birth_date

METHODOLOGY_VERSION = "mahesa-gantari-rws-v0.1"
METHODOLOGY_STATUS = "course_transcribed"
SOURCE_DOCUMENT = "Matrix of Destiny Basic 02 - Akademi Mahesa Gantari (2026)"


class FormulaEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    methodology_version: Literal["mahesa-gantari-rws-v0.1"] = METHODOLOGY_VERSION
    source_document: str = SOURCE_DOCUMENT
    source_page: int = Field(ge=1)
    evidence_status: Literal[
        "explicitly_stated_in_course",
        "reconstructed_from_course_example",
        "reconstructed_from_course_diagram",
        "reconstructed_from_reference_diagram",
        "reconstructed_from_reference_health_card",
        "manually_compared_to_reference_calculator",
        "teacher_verified",
    ]
    verified: bool = False


class CoursePoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    position_id: str
    label: str
    value: int = Field(ge=1, le=22)
    arcana_number: int = Field(ge=1, le=22)
    arcana_name: str
    calculation_trace: tuple[str, ...]
    evidence: FormulaEvidence


class CourseLine(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    line_id: str
    ordered_point_ids: tuple[str, ...]
    values: tuple[int, ...]
    component_labels: tuple[str, ...]
    evidence: FormulaEvidence

    @model_validator(mode="after")
    def validate_components(self) -> "CourseLine":
        component_count = len(self.ordered_point_ids)
        if component_count == 0:
            raise ValueError("CourseLine must contain at least one component.")
        if (
            len(self.values) != component_count
            or len(self.component_labels) != component_count
        ):
            raise ValueError(
                "CourseLine ordered_point_ids, values, and component_labels "
                "must have equal lengths."
            )
        if len(set(self.ordered_point_ids)) != component_count:
            raise ValueError("CourseLine ordered_point_ids must not contain duplicates.")
        return self


class PurposeValues(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    earth: CoursePoint
    sky: CoursePoint
    soul_searching: CoursePoint
    male: CoursePoint
    female: CoursePoint
    socialization: CoursePoint
    spiritual_knowledge: CoursePoint
    age_range_metadata: dict[str, str]


class HealthCardCell(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    column_id: Literal["physics", "energy", "emotions"]
    formula: str
    value: int = Field(ge=1, le=22)
    arcana_number: int = Field(ge=1, le=22)
    arcana_name: str
    calculation_trace: tuple[str, ...]
    evidence: FormulaEvidence
    verified: bool = False


class HealthCardRow(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    row_id: str
    label: str
    physics: HealthCardCell
    energy: HealthCardCell
    emotions: HealthCardCell


class HealthCardResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    physics: HealthCardCell
    energy: HealthCardCell
    emotions: HealthCardCell


class HealthCard(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rows: tuple[HealthCardRow, ...]
    result: HealthCardResult
    verified: bool = False
    warnings: tuple[str, ...]


class MahesaGantariCalculationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    birth_date: date
    sect: Sect = Sect.UNKNOWN


class MahesaGantariCalculation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    methodology_version: Literal["mahesa-gantari-rws-v0.1"]
    status: Literal["course_transcribed"]
    verified: bool
    birth_date: date
    points: tuple[CoursePoint, ...]
    money_line: CourseLine
    relationship_line: CourseLine
    karmic_tail: CourseLine
    deepest_desire: CourseLine
    male_generation: CourseLine
    female_generation: CourseLine
    purpose: PurposeValues
    health_card: HealthCard
    sect_context: SectContext
    warnings: tuple[str, ...]


class MahesaGantariRwsMethodology:
    version = METHODOLOGY_VERSION
    status = METHODOLOGY_STATUS
    verified = False

    def __init__(self) -> None:
        self.normalizer = ConsecutiveDigitAdditionNormalizer()

    def _point(
        self,
        position_id: str,
        label: str,
        raw_value: int,
        trace_prefix: str,
        source_page: int,
        evidence_status: Literal[
            "explicitly_stated_in_course",
            "reconstructed_from_course_example",
            "reconstructed_from_course_diagram",
            "reconstructed_from_reference_diagram",
            "reconstructed_from_reference_health_card",
        ] = "explicitly_stated_in_course",
        source_document: str = SOURCE_DOCUMENT,
    ) -> CoursePoint:
        normalized = self.normalizer.normalize_with_trace(raw_value)
        arcana = get_mahesa_gantari_arcana(normalized.value)
        return CoursePoint(
            position_id=position_id,
            label=label,
            value=normalized.value,
            arcana_number=arcana.energy_number,
            arcana_name=arcana.arcana_name,
            calculation_trace=(trace_prefix, *normalized.calculation_trace),
            evidence=FormulaEvidence(
                source_document=source_document,
                source_page=source_page,
                evidence_status=evidence_status,
                verified=False,
            ),
        )

    @staticmethod
    def _line(
        line_id: str,
        ordered_point_ids: tuple[str, ...],
        values: tuple[int, ...],
        component_labels: tuple[str, ...],
        source_page: int,
    ) -> CourseLine:
        return CourseLine(
            line_id=line_id,
            ordered_point_ids=ordered_point_ids,
            values=values,
            component_labels=component_labels,
            evidence=FormulaEvidence(
                source_page=source_page,
                evidence_status="explicitly_stated_in_course",
                verified=False,
            ),
        )

    def calculate(
        self,
        birth_date: date,
        sect: Sect = Sect.UNKNOWN,
    ) -> MahesaGantariCalculation:
        validate_birth_date(birth_date)

        points: dict[str, CoursePoint] = {}

        def add(
            position_id: str,
            label: str,
            raw_value: int,
            trace_prefix: str,
            source_page: int,
            evidence_status: Literal[
                "explicitly_stated_in_course",
                "reconstructed_from_course_example",
                "reconstructed_from_course_diagram",
                "reconstructed_from_reference_diagram",
                "reconstructed_from_reference_health_card",
            ] = "explicitly_stated_in_course",
            source_document: str = SOURCE_DOCUMENT,
        ) -> CoursePoint:
            point = self._point(
                position_id,
                label,
                raw_value,
                trace_prefix,
                source_page,
                evidence_status,
                source_document,
            )
            points[position_id] = point
            return point

        a = add("A", "Birth Day", birth_date.day, f"Birth day = {birth_date.day}", 14)
        b = add("B", "Birth Month", birth_date.month, f"Birth month = {birth_date.month}", 14)
        year_digits = [int(digit) for digit in f"{birth_date.year:04d}"]
        year_sum = sum(year_digits)
        c = add(
            "C",
            "Birth Year",
            year_sum,
            "Year digits: " + " + ".join(str(digit) for digit in year_digits) + f" = {year_sum}",
            14,
        )
        d_raw = a.value + b.value + c.value
        d = add("D", "Karmic Foundation", d_raw, f"A + B + C = {a.value} + {b.value} + {c.value} = {d_raw}", 14)
        e_raw = a.value + b.value + c.value + d.value
        e = add("E", "Center", e_raw, f"A + B + C + D = {a.value} + {b.value} + {c.value} + {d.value} = {e_raw}", 14)

        f = add("F", "Top Left Generation Corner", a.value + b.value, f"A + B = {a.value} + {b.value} = {a.value + b.value}", 24)
        g = add("G", "Top Right Generation Corner", b.value + c.value, f"B + C = {b.value} + {c.value} = {b.value + c.value}", 24)
        h = add("H", "Bottom Right Generation Corner", c.value + d.value, f"C + D = {c.value} + {d.value} = {c.value + d.value}", 24)
        i = add("I", "Bottom Left Generation Corner", a.value + d.value, f"A + D = {a.value} + {d.value} = {a.value + d.value}", 24)

        j = add("J", "Inner Left", a.value + e.value, f"A + E = {a.value} + {e.value} = {a.value + e.value}", 40)
        k = add("K", "Inner Top", b.value + e.value, f"B + E = {b.value} + {e.value} = {b.value + e.value}", 40)
        l = add("L", "Inner Right", c.value + e.value, f"C + E = {c.value} + {e.value} = {c.value + e.value}", 40)
        m = add("M", "Inner Bottom", d.value + e.value, f"D + E = {d.value} + {e.value} = {d.value + e.value}", 40)
        n = add("N", "Material and Relationship Output", l.value + m.value, f"L + M = {l.value} + {m.value} = {l.value + m.value}", 40)

        o_raw = f.value + g.value + h.value + i.value
        o = add("O", "Deepest Desire", o_raw, f"F + G + H + I = {f.value} + {g.value} + {h.value} + {i.value} = {o_raw}", 40)
        p = add("P", "Shadow Top Left", f.value + o.value, f"F + O = {f.value} + {o.value} = {f.value + o.value}", 40)
        q = add("Q", "Shadow Top Right", g.value + o.value, f"G + O = {g.value} + {o.value} = {g.value + o.value}", 40)
        r = add("R", "Shadow Bottom Right", h.value + o.value, f"H + O = {h.value} + {o.value} = {h.value + o.value}", 40)
        s = add("S", "Shadow Bottom Left", i.value + o.value, f"I + O = {i.value} + {o.value} = {i.value + o.value}", 40)

        additional_specs = (
            ("A_plus_J", "A plus J", a, j),
            ("E_plus_J", "E plus J", e, j),
            ("B_plus_K", "B plus K", b, k),
            ("C_plus_L", "C plus L", c, l),
            ("D_plus_M", "D plus M", d, m),
            ("F_plus_P", "F plus P", f, p),
            ("G_plus_Q", "G plus Q", g, q),
            ("H_plus_R", "H plus R", h, r),
            ("I_plus_S", "I plus S", i, s),
            ("E_plus_K", "E plus K", e, k),
            ("E_plus_O", "E plus O", e, o),
            ("L_plus_N", "L plus N", l, n),
            ("M_plus_N", "M plus N", m, n),
        )
        for position_id, label, left, right in additional_specs:
            raw = left.value + right.value
            is_reference_reconstruction = position_id == "E_plus_J"
            add(
                position_id,
                label,
                raw,
                f"{left.position_id} + {right.position_id} = {left.value} + {right.value} = {raw}",
                1 if is_reference_reconstruction else 40,
                (
                    "reconstructed_from_reference_diagram"
                    if is_reference_reconstruction
                    else "explicitly_stated_in_course"
                ),
                (
                    "Reference calculator diagram (manual comparison, 1990-08-16)"
                    if is_reference_reconstruction
                    else SOURCE_DOCUMENT
                ),
            )

        health_source = "Reference health-card diagram (manual comparison, 1990-08-16)"

        def health_cell(
            column_id: Literal["physics", "energy", "emotions"],
            formula: str,
            raw_value: int,
            trace_prefix: str,
        ) -> HealthCardCell:
            normalized = self.normalizer.normalize_with_trace(raw_value)
            arcana = get_mahesa_gantari_arcana(normalized.value)
            return HealthCardCell(
                column_id=column_id,
                formula=formula,
                value=normalized.value,
                arcana_number=arcana.energy_number,
                arcana_name=arcana.arcana_name,
                calculation_trace=(trace_prefix, *normalized.calculation_trace),
                evidence=FormulaEvidence(
                    source_document=health_source,
                    source_page=1,
                    evidence_status="reconstructed_from_reference_health_card",
                    verified=False,
                ),
                verified=False,
            )

        health_specs = (
            ("sahasrara", "Sahasrara", a, b),
            ("ajna", "Ajna", points["A_plus_J"], j),
            ("vishuddha", "Vishuddha", j, k),
            ("anahata", "Anahata", points["E_plus_J"], points["E_plus_K"]),
            ("manipura", "Manipura", e, e),
            ("svadhisthana", "Svadhisthana", l, m),
            ("muladhara", "Muladhara", c, d),
        )
        health_rows: list[HealthCardRow] = []
        for row_id, label, physics_point, energy_point in health_specs:
            emotion_raw = physics_point.value + energy_point.value
            health_rows.append(
                HealthCardRow(
                    row_id=row_id,
                    label=label,
                    physics=health_cell(
                        "physics",
                        physics_point.position_id,
                        physics_point.value,
                        f"{physics_point.position_id} = {physics_point.value}",
                    ),
                    energy=health_cell(
                        "energy",
                        energy_point.position_id,
                        energy_point.value,
                        f"{energy_point.position_id} = {energy_point.value}",
                    ),
                    emotions=health_cell(
                        "emotions",
                        f"normalize({physics_point.position_id} + {energy_point.position_id})",
                        emotion_raw,
                        f"{physics_point.position_id} + {energy_point.position_id} = {physics_point.value} + {energy_point.value} = {emotion_raw}",
                    ),
                )
            )

        def result_cell(column_id: Literal["physics", "energy", "emotions"]) -> HealthCardCell:
            values = [getattr(row, column_id).value for row in health_rows]
            raw = sum(values)
            joined = " + ".join(str(value) for value in values)
            return health_cell(
                column_id,
                f"normalize(sum({column_id} column))",
                raw,
                f"{column_id} result: {joined} = {raw}",
            )

        earth = self._point("earth", "Earth Line Value", a.value + c.value, f"A + C = {a.value} + {c.value} = {a.value + c.value}", 41)
        sky = self._point("sky", "Sky Line Value", b.value + d.value, f"B + D = {b.value} + {d.value} = {b.value + d.value}", 41)
        soul = self._point("soul_searching", "Soul Searching", earth.value + sky.value, f"earth + sky = {earth.value} + {sky.value} = {earth.value + sky.value}", 41)
        male = self._point(
            "male",
            "Male Purpose Contribution",
            f.value + h.value,
            f"F + H = {f.value} + {h.value} = {f.value + h.value}",
            41,
            "reconstructed_from_course_diagram",
        )
        female = self._point(
            "female",
            "Female Purpose Contribution",
            g.value + i.value,
            f"G + I = {g.value} + {i.value} = {g.value + i.value}",
            41,
            "reconstructed_from_course_diagram",
        )
        social = self._point("socialization", "Socialization", male.value + female.value, f"male + female = {male.value} + {female.value} = {male.value + female.value}", 41)
        spiritual = self._point("spiritual_knowledge", "Spiritual Knowledge", soul.value + social.value, f"soul_searching + socialization = {soul.value} + {social.value} = {soul.value + social.value}", 41)

        return MahesaGantariCalculation(
            methodology_version=self.version,
            status=self.status,
            verified=False,
            birth_date=birth_date,
            points=tuple(points.values()),
            money_line=self._line(
                "money_line",
                ("L", "L_plus_N", "N"),
                (l.value, points["L_plus_N"].value, n.value),
                (
                    "supporting or blocking factor for material potential",
                    "vocation, aspiration, passion, or suitable material activity",
                    "financial objective",
                ),
                31,
            ),
            relationship_line=self._line(
                "relationship_line",
                ("M", "M_plus_N", "N"),
                (m.value, points["M_plus_N"].value, n.value),
                (
                    "relationship obstacle or entry condition",
                    "method of compromise",
                    "partner or output energy attracted",
                ),
                34,
            ),
            karmic_tail=self._line(
                "karmic_tail",
                ("M", "D_plus_M", "D"),
                (m.value, points["D_plus_M"].value, d.value),
                ("social karma", "event karma", "spiritual karma"),
                41,
            ),
            deepest_desire=self._line(
                "deepest_desire",
                ("O", "E_plus_O"),
                (o.value, points["E_plus_O"].value),
                ("deepest desire", "hidden potential"),
                41,
            ),
            male_generation=self._line(
                "male_generation",
                ("F", "H"),
                (f.value, h.value),
                ("male generation start", "male generation end"),
                41,
            ),
            female_generation=self._line(
                "female_generation",
                ("G", "I"),
                (g.value, i.value),
                ("female generation start", "female generation end"),
                41,
            ),
            purpose=PurposeValues(
                earth=earth,
                sky=sky,
                soul_searching=soul,
                male=male,
                female=female,
                socialization=social,
                spiritual_knowledge=spiritual,
                age_range_metadata={
                    "soul_searching": "before or around age 40",
                    "socialization": "approximately ages 40-60",
                    "spiritual_knowledge": "approximately age 60 and later",
                },
            ),
            health_card=HealthCard(
                rows=tuple(health_rows),
                result=HealthCardResult(
                    physics=result_cell("physics"),
                    energy=result_cell("energy"),
                    emotions=result_cell("emotions"),
                ),
                verified=False,
                warnings=(
                    "Health Card formulas are reconstructed from a reference diagram and remain unverified.",
                    "This numerology table is not a medical assessment, diagnosis, or treatment recommendation.",
                ),
            ),
            sect_context=SectContext.from_user_value(sect),
            warnings=(
                "This course-transcribed methodology remains unverified.",
                "Sect is user-provided context only and does not modify Matrix values.",
                "Sect weighting and malefic interpretation remain inactive until a course rule is documented.",
            ),
        )


COURSE_METHODOLOGIES = {
    MahesaGantariRwsMethodology.version: MahesaGantariRwsMethodology
}
