# Destiny Matrix Methodology

Public methodology version: `unverified-v0`

The public calculator remains on the intentionally unverified placeholder
methodology. Separately, the repository contains experimental, teaser, and
course-transcribed implementations with explicit version and evidence
boundaries. None is silently promoted to the public default.

For the public `unverified-v0` methodology, concept names remain working
placeholders. The internal course positions have source-backed formulas, but
they have not yet been mapped to the frontend chart's semantic labels such as
Central Energy, Portrait, Talents, Relationship Line, Money Line, Ancestral
Line, or Karmic Tail.

The repository also contains the internal `mahesa-gantari-rws-v0.1`
course-transcribed methodology. It remains `verified: false`, is not the public
default, and does not establish a mapping to the existing public SVG labels.

## Methodology Inventory

| Role | Version | Status | Public default |
| --- | --- | --- | --- |
| Public methodology | `unverified-v0` | Placeholder, `verified: false` | Yes |
| Experimental normalizer | `cda-experimental-v0` | Experimental normalization only | No |
| Teacher teaser | `teacher-teaser-v0.1` | Provisional transcription, `verified: false` | No |
| Course methodology | `mahesa-gantari-rws-v0.1` | `course_transcribed`, `verified: false` | No |

## Course Verification Checklist

This checklist describes `mahesa-gantari-rws-v0.1`; it does not change the
verification status or behavior of the public methodology.

| Proposed concept | Formula supplied | Implemented | Tested | Status |
| --- | --- | --- | --- | --- |
| Value normalization | Yes | Yes | Yes | Course-transcribed; `verified: false` |
| Center | Yes | Yes (`E`) | Yes | Course-transcribed; `verified: false` |
| Top | Yes | Yes (`B`) | Yes | Course-transcribed; `verified: false` |
| Left | Yes | Yes (`A`) | Yes | Course-transcribed; `verified: false` |
| Right | Yes | Yes (`C`) | Yes | Course-transcribed; `verified: false` |
| Bottom | Yes | Yes (`D`) | Yes | Course-transcribed; `verified: false` |
| Karmic tail | Yes | Yes | Yes | Course-transcribed; `verified: false` |
| Relationship line | Yes | Yes | Yes | Course-transcribed; `verified: false` |
| Money line | Yes | Yes | Yes | Course-transcribed; `verified: false` |
| Male generation line | Yes | Yes | Yes | Course-transcribed; `verified: false` |
| Female generation line | Yes | Yes | Yes | Course-transcribed; `verified: false` |
| Age cycles | No | No | No | Awaiting authoritative source |
| Course reference fixture | Yes | Yes | Yes | Course-transcribed; `verified: false` |

## Mahesa Gantari Course Transcription

`mahesa-gantari-rws-v0.1` independently implements formulas supported by
*Matrix of Destiny Basic 02* (Akademi Mahesa Gantari, 2026). The implementation
stores concise labels, traces, numeric fixtures, and source-page evidence. The
complete PDF and extracted course corpus remain private and are not published
through Git or the API.

Evidence statuses are deliberately distinct:

- `explicitly_stated_in_course`: the formula is visibly stated on a cited page.
- `reconstructed_from_course_example`: a value is reproduced from the stated
  formula and course example.
- `reconstructed_from_course_diagram`: a scalar is reconstructed from an
  explicitly ordered course diagram when the scalar formula is not separately
  stated in prose.
- `manually_compared_to_reference_calculator`: reserved for a documented human
  comparison; not automatically assigned.
- `teacher_verified`: reserved for explicit teacher confirmation; currently not
  assigned.

Formula sources:

| Formula group | Course pages |
| --- | --- |
| Normalization and A-E | Module 02 pp. 13-15 |
| F-I generation corners | Module 02 p. 24 |
| J-S and additional nodes | Module 02 p. 40 |
| Ordered lines and purpose values | Module 02 p. 41 |
| Money semantics | Module 02 pp. 31-32 |
| Relationship semantics | Module 02 pp. 34-35 |
| Karmic Tail meanings | Module 02 p. 45 |
| RWS Arcana and astrology associations | Module 01 p. 12 |

The 18 August 1988 fixture reconstructs all implemented points and confirms:

- Money Line: `[13, 20, 7]`
- Relationship Line: `[12, 19, 7]`
- Karmic Tail: `[12, 19, 7]`
- Deepest Desire: `[10, 15]`
- Male Generation Line: `[8, 15]`
- Female Generation Line: `[16, 7]`

The Relationship Line and Karmic Tail are distinct objects despite sharing the
same example values. See `methodology_spec.md` for the full concise formula
table.

Mahesa Gantari uses RWS semantic ordering: energy 8 is Strength, energy 11 is
Justice, and energy 22 represents The Fool. Arcana content is versioned and kept
separate from numeric calculation logic. `matrix-destiny.com` is permitted only
for manual comparison and is not treated as a formula source.

### Deferred Sect Interpretation

Sect is optional user context: `day`, `night`, or `unknown`. Missing input is
`unknown`; selected day/night values record `source: user_provided`. Birth time
and birth location are not required, and sect is never inferred from a birth
date. It does not change Matrix numbers.

No weighting, contrary-to-sect malefic rule, or Arcana interpretation modifier
is active. Unknown sect skips all sect-based interpretation. Mars, Saturn, and
their associated Arcana are not labeled inherently negative. Activation must
wait for a documented teacher rule.

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

### Local Experimental Preview

The provisional methodology is available only through these feature-flagged
experimental endpoints:

- `POST /api/experimental/teacher-teaser/personal`
- `POST /api/experimental/teacher-teaser/compatibility`

They return `404` unless `ENABLE_EXPERIMENTAL_METHODOLOGIES=true`. The setting
defaults to `false`; use it only in a local `backend/.env`, never in committed
credentials. The bilingual visual inspection route is
`/lab/teacher-teaser`. It displays supported values and traces without
interpretations or predictions and does not alter the public calculator.

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

## Public Placeholder Rule

The public `unverified-v0` methodology returns value `0`, `verified: false`, and
a trace stating that its formula has not been provided. Internal versioned
methodologies do not alter that public behavior.
