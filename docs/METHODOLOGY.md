# Destiny Matrix Methodology

Current methodology version: `unverified-v0`

The definitive Destiny Matrix formulas have not been supplied yet. This document tracks proposed concepts, required formulas, and verification status. The application must not silently choose between competing methods.

The concept names listed in `methodology_spec.md` are working placeholders only. They have not yet been verified against an authoritative Destiny Matrix source, and they have not yet been mapped to the frontend chart's current semantic labels such as Central Energy, Portrait, Talents, Relationship Line, Money Line, Ancestral Line, or Karmic Tail.

## Verification Checklist

| Proposed concept | Formula supplied | Implemented | Tested | Status |
| --- | --- | --- | --- | --- |
| Value normalization | Provisional transcription | Teacher teaser only; public placeholder unchanged | Experimental and teacher-teaser tests | Awaiting teacher verification |
| Center | Provisional transcription | `E` in teacher teaser only | Reconstructed examples | Awaiting teacher verification |
| Top | Provisional transcription | `B` in teacher teaser only | Reconstructed examples | Awaiting teacher verification |
| Left | Provisional transcription | `A` in teacher teaser only | Reconstructed examples | Awaiting teacher verification |
| Right | Provisional transcription | `C` in teacher teaser only | Reconstructed examples | Awaiting teacher verification |
| Bottom | Provisional transcription | `D` in teacher teaser only | Reconstructed examples | Awaiting teacher verification |
| Karmic tail | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Relationship line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Money line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Male ancestral line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Female ancestral line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Age cycles | No | No | No | Awaiting authoritative source |
| Verified reference fixtures | No | Framework only; synthetic example excluded from acceptance | Schema validation tests only | Awaiting authoritative source |

## Experimental Normalization Candidate

- Internal name: Consecutive Digit Addition
- Version: `cda-experimental-v0`
- Status: Experimental, awaiting comparison with the August course methodology
- Preserved range: `1–22`
- Scope: normalization only, separate from matrix-position formulas

Exact repeated digit-addition rule:

1. Valid input must be a positive integer.
2. Values from `1` through `22` inclusive are preserved.
3. For values greater than `22`, sum their decimal digits.
4. If the result remains greater than `22`, repeat the process.
5. Stop as soon as the result is between `1` and `22` inclusive.

Input validation:

- Boolean values must not be accepted as integers.
- Zero and negative integers are invalid.
- Floats, numeric strings, null, and other non-integer values are invalid.

Worked examples:

| Input | Output |
| --- | --- |
| 1 | 1 |
| 9 | 9 |
| 10 | 10 |
| 11 | 11 |
| 22 | 22 |
| 23 | 5 |
| 29 | 11 |
| 44 | 8 |
| 59 | 14 |
| 99 | 18 |
| 199 | 19 |
| 999 | 9 |

Trace examples:

For `22`:

- `22 is within the preserved range 1–22`
- Result: `22`

For `29`:

- `29 is greater than 22`
- `2 + 9 = 11`
- `11 is within the preserved range 1–22`
- Result: `11`

For `999`:

- `999 is greater than 22`
- `9 + 9 + 9 = 27`
- `27 is greater than 22`
- `2 + 7 = 9`
- `9 is within the preserved range 1–22`
- Result: `9`

This normalization rule alone does not define the full matrix. It must not be called universal, classic, or standard until an authoritative source is selected.

## Provisional Teacher Teaser Methodology

- Internal version: `teacher-teaser-v0.1`
- Status: `transcribed_from_teacher_material`
- Verification: Provisional, not teacher-verified
- Public exposure: Internal registry only; not the calculator or API default
- Interpretation data: Unchanged

The supplied implementation requirements transcribed the following formulas
from teacher teaser slides. The original slide image and identifier were not
attached, so this implementation reproduces the supplied examples but cannot
claim independent visual source verification.

| ID | Neutral label | Implemented formula |
| --- | --- | --- |
| A | Birth Day / Left | `normalize(day)` |
| B | Birth Month / Top | `normalize(month)` |
| C | Birth Year / Right | Sum all four year digits, then normalize |
| D | Foundation / Bottom | `normalize(A + B + C)` |
| earth_line | Earth Line | `normalize(A + C)` |
| sky_line | Sky Line | `normalize(B + D)` |
| E | Soul Searching / Center | `normalize(earth_line + sky_line)` |
| top_left | Top Left | `normalize(A + B)` |
| top_right | Top Right | `normalize(B + C)` |
| bottom_right | Bottom Right | `normalize(C + D)` |
| bottom_left | Bottom Left | `normalize(D + A)` |

Every value includes a calculation trace. E also records its equivalent
`normalize(A + B + C + D)` expression under the current normalizer.

The internal compatibility composer applies
`normalize(person_1[position] + person_2[position])` only to these 11 IDs.
Unsupported or missing positions are rejected. No compatibility route or public
default has been added.

Evidence classification:

- `transcribed`: a formula or value appears in the supplied teacher-material
  transcription but has not been independently checked against the slide.
- `inferred`: reconstructed from supplied formulas or examples where the source
  chart value could not be read confidently.
- `teacher_verified`: confirmed against authoritative material by an identified
  verifier on a recorded date. No teacher-teaser fixture has this status.

Taylor Swift and Travis Kelce personal fixtures reconstruct all supplied values.
For their compatibility fixture, Earth Line `9` and Sky Line `8` are marked
`inferred` because the original slide was unavailable; the other supplied
compatibility values are `transcribed`.

Unsupported topics remain: small/internal nodes beyond the stated Earth and Sky
lines, annual energy, monthly energy, age cycles, money output, relationship
output, the Ahmad Sahroni forecast chart, and positions inferred from geometry.

## Reference Fixture Verification Workflow

The backend includes a reference-fixture schema for recording authoritative
example matrices when course material becomes available. The framework validates
transcribed evidence; it does not calculate positions or establish formulas.

Fixture status progresses explicitly:

1. `transcribed`: copied from the identified source but not independently checked.
2. `inferred`: reconstructed from supplied evidence but not confidently visible
   in the original source.
3. `independently_checked`: compared against the source by a second reviewer.
4. `teacher_verified`: confirmed against authoritative course material, with
   source name, source type, source reference, verifier, and verification date.
5. `disputed`: retained for investigation because sources or reviewers disagree.

To transcribe a teacher's chart:

1. Record the case name, exact `YYYY-MM-DD` birth date, stated methodology
   version, and durable source reference.
2. Preserve every teacher-provided position name in `source_label`. English and
   Indonesian labels are optional until translations are reviewed.
3. Record only values visible in the source. Final values must be in `1–22`.
   Values above `22` are accepted only when explicitly marked as raw
   intermediate values.
4. Copy calculation traces only when the source supplies them. Do not infer
   missing steps or formulas.
5. Add chart coordinates only after a source position is deliberately mapped to
   frontend geometry.
6. Have a second reviewer check the transcription, then obtain teacher or
   authoritative-source confirmation before using it as an acceptance fixture.

`backend/tests/fixtures/synthetic_example.json` is intentionally synthetic and
unverified. Its `is_synthetic` marker prevents it from qualifying for
verified-methodology acceptance tests. Detailed editing instructions are in
`backend/tests/fixtures/README.md`.

## Mapping Notes

The current frontend chart and API placeholder positions are implementation scaffolding for the MVP. The proposed names in `methodology_spec.md` must not be treated as equivalent to existing frontend labels until an authoritative source provides:

- The exact formula for each proposed concept.
- The intended semantic meaning of each position.
- The relationship, if any, between source methodology positions and frontend display labels.
- Verified reference fixtures that prove the mapping and calculations.

## Required Formula Documentation Template

When a formula is supplied, document it with:

- Position ID
- Human label in English and Indonesian
- Input components
- Normalization rules
- Exact calculation steps
- Output range
- Edge cases
- Example fixture with date of birth
- Source/status notes

## Placeholder Rule

Until verified formulas are supplied, every position returns value `0`, `verified: false`, and a trace that clearly states the formula has not been provided.
