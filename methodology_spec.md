# Destiny Matrix Methodology Specification

## Method
- School/source:
- Method name:
- Methodology version:
- Source permission/status:

## Experimental normalization candidate
- Internal name: Consecutive Digit Addition
- Version: cda-experimental-v0
- Status: Experimental, awaiting comparison with the August course methodology
- Preserved range: 1–22
- Rule:
  - Valid input must be a positive integer.
  - Values from 1 through 22 inclusive are preserved.
  - For values greater than 22, sum their decimal digits.
  - If the result remains greater than 22, repeat the process.
  - Stop as soon as the result is between 1 and 22 inclusive.
- Input validation:
  - Boolean values are not accepted as integers.
  - Zero and negative integers are invalid.
  - Floats, numeric strings, null, and other non-integer values are invalid.
- Worked examples:
  - 1 -> 1
  - 9 -> 9
  - 10 -> 10
  - 11 -> 11
  - 22 -> 22
  - 23 -> 5
  - 29 -> 11
  - 44 -> 8
  - 59 -> 14
  - 99 -> 18
  - 199 -> 19
  - 999 -> 9
- Important limitation:
  - This normalization rule alone does not define the full Destiny Matrix.
  - It must not be called universal, classic, or standard until an authoritative source is selected.

## Value normalization
- Exact rule:
  - Candidate only: see "Experimental normalization candidate" above.
- Examples:
  - Input 23 -> 5 under cda-experimental-v0
  - Input 29 -> 11 under cda-experimental-v0
  - Input 44 -> 8 under cda-experimental-v0

## Provisional teacher teaser methodology

- Internal version: `teacher-teaser-v0.1`
- Status: `transcribed_from_teacher_material`
- Public default: No
- Verification level: Not teacher-verified
- Normalizer: Existing Consecutive Digit Addition strategy
- Evidence boundary:
  - The formulas and example values below were supplied in the implementation
    request as transcriptions from teacher teaser slides.
  - The original slide image and slide identifier were not attached, so the
    implementation has not been independently checked against the visual source.
  - Taylor Swift and Travis Kelce outputs have been reconstructed from the
    stated formulas and match every supplied expected value.

### Supported personal formulas

For a valid birth date:

| ID | Neutral label | Formula |
| --- | --- | --- |
| A | Left / Birth Day | `normalize(day)` |
| B | Top / Birth Month | `normalize(month)` |
| C | Right / Birth Year | Sum the four individual year digits, then normalize |
| D | Bottom / Foundation | `normalize(A + B + C)` |
| earth_line | Earth Line | `normalize(A + C)` |
| sky_line | Sky Line | `normalize(B + D)` |
| E | Center / Soul Searching | `normalize(earth_line + sky_line)` |
| top_left | Top Left | `normalize(A + B)` |
| top_right | Top Right | `normalize(B + C)` |
| bottom_right | Bottom Right | `normalize(C + D)` |
| bottom_left | Bottom Left | `normalize(D + A)` |

Under the current normalizer, the E calculation is also equivalent to
normalizing `A + B + C + D`. This equivalence is included in the calculation
trace.

### Internal compatibility composer

Compatibility is supported only for the 11 position IDs listed above:

`compatibility[position] = normalize(person_1[position] + person_2[position])`

Unsupported or missing position IDs raise an explicit error. Compatibility is
not exposed through the public API.

### Example reconstruction

| Case | A | B | C | D | Earth | Sky | E | TL | TR | BR | BL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Taylor Swift, 1989-12-13 | 13 | 12 | 9 | 7 | 22 | 19 | 5 | 7 | 21 | 16 | 20 |
| Travis Kelce, 1989-10-05 | 5 | 10 | 9 | 6 | 14 | 16 | 3 | 15 | 19 | 15 | 11 |
| Compatibility | 18 | 22 | 18 | 13 | 9 | 8 | 8 | 22 | 4 | 4 | 4 |

Taylor and Travis personal values are stored as `transcribed`. Compatibility
Earth Line and Sky Line are stored as `inferred` because the original slide
could not be visually checked; the remaining supplied compatibility values are
stored as `transcribed`. None are `teacher_verified`.

### Unsupported topics

The provisional methodology does not calculate:

- Small or internal chart nodes beyond the explicitly listed Earth and Sky lines
- Annual or monthly energy
- Age cycles
- Money output
- Relationship output
- Ahmad Sahroni forecast chart
- Any position inferred only from chart geometry

## Matrix positions

## Mahesa Gantari RWS course methodology

- Internal version: `mahesa-gantari-rws-v0.1`
- Status: `course_transcribed`
- Verified: `false`
- Public default: No
- Calculation source: *Matrix of Destiny Basic 02*, Akademi Mahesa Gantari
  (2026)
- Arcana source: *Matrix of Destiny Basic 01*, Akademi Mahesa Gantari (2026)
- Normalizer: Existing Consecutive Digit Addition strategy, preserving `1-22`

The private course PDFs and extracted Markdown are local source material and are
not redistributed. Only independently implemented formulas, concise labels,
source page references, and numeric fixtures are stored in the repository.

### Formula table

| Output | Formula | Source page |
| --- | --- | --- |
| A | `normalize(day)` | Module 02 p. 14 |
| B | `normalize(month)` | Module 02 p. 14 |
| C | `normalize(sum(four year digits))` | Module 02 p. 14 |
| D | `normalize(A + B + C)` | Module 02 p. 14 |
| E | `normalize(A + B + C + D)` | Module 02 p. 14 |
| F | `normalize(A + B)` | Module 02 p. 24 |
| G | `normalize(B + C)` | Module 02 p. 24 |
| H | `normalize(C + D)` | Module 02 p. 24 |
| I | `normalize(A + D)` | Module 02 p. 24 |
| J | `normalize(A + E)` | Module 02 p. 40 |
| K | `normalize(B + E)` | Module 02 p. 40 |
| L | `normalize(C + E)` | Module 02 p. 40 |
| M | `normalize(D + E)` | Module 02 p. 40 |
| N | `normalize(L + M)` | Module 02 p. 40 |
| O | `normalize(F + G + H + I)` | Module 02 p. 40 |
| P | `normalize(F + O)` | Module 02 p. 40 |
| Q | `normalize(G + O)` | Module 02 p. 40 |
| R | `normalize(H + O)` | Module 02 p. 40 |
| S | `normalize(I + O)` | Module 02 p. 40 |

Additional display nodes are independently identified and normalized:

- `A_plus_J`, `B_plus_K`, `C_plus_L`, `D_plus_M`
- `F_plus_P`, `G_plus_Q`, `H_plus_R`, `I_plus_S`
- `E_plus_K`, `E_plus_O`, `L_plus_N`, `M_plus_N`

The experimental inspection layout also includes `E_plus_J = normalize(E + J)`.
This point is `reconstructed_from_reference_diagram`, remains `verified: false`,
and is not represented as explicitly stated in the course.

These formulas are shown on Module 02 page 40. Every calculated point includes
a trace and evidence metadata with methodology version, document, page,
evidence status, and `verified: false`.

### Ordered domain lines

| Domain object | Ordered point IDs | Source |
| --- | --- | --- |
| Money Line | `L -> L_plus_N -> N` | Module 02 pp. 31-32, 41 |
| Relationship Line | `M -> M_plus_N -> N` | Module 02 pp. 34-35, 41 |
| Karmic Tail | `M -> D_plus_M -> D` | Module 02 pp. 41, 45 |
| Deepest Desire | `O -> E_plus_O` | Module 02 p. 41 |
| Male Generation Line | `F -> H` | Module 02 pp. 24, 41 |
| Female Generation Line | `G -> I` | Module 02 pp. 24, 41 |

Relationship Line and Karmic Tail remain separate domain objects even when a
fixture produces the same numeric sequence.

Purpose values from Module 02 page 41:

- `earth = normalize(A + C)`
- `sky = normalize(B + D)`
- `soul_searching = normalize(earth + sky)`
- `male = normalize(F + H)`
- `female = normalize(G + I)`
- `socialization = normalize(male + female)`
- `spiritual_knowledge = normalize(soul_searching + socialization)`

The `male` and `female` scalar formulas use
`reconstructed_from_course_diagram` evidence: the source explicitly shows the
ordered generation lines and defines Socialization as Male plus Female, but
does not separately state the two scalar formulas in prose. Their formulas and
values remain unchanged and are not teacher-verified.

Course age ranges are metadata only, not scientific claims or guaranteed
predictions.

### Experimental Health Card

The feature-flagged Mahesa Gantari lab exposes a provisional Health Card with
the ordered rows Sahasrara, Ajna, Vishuddha, Anahata, Manipura, Svadhisthana,
and Muladhara, followed by a normalized result row. Physics and Energy cells
reference calculated Matrix points; Emotions normalizes the two row values.
Each result column normalizes the sum of its seven chakra values. These formulas
are `reconstructed_from_reference_health_card`, remain `verified: false`, and
are not medical assessments or interpretations.

### RWS Arcana profile

The versioned profile `rws-mahesa-gantari-v0.1` uses Module 01 page 12. It maps
8 to Strength, 11 to Justice, and Matrix energy 22 to The Fool. Numeric Matrix
calculation and Arcana semantic profiles remain separate modules.

### Optional sect context

Accepted values are `day`, `night`, and `unknown`; missing input defaults to
`unknown`. Day and night are recorded as `user_provided`. The application does
not infer sect from birth date, require birth time or location, or activate any
sect weighting. Sect never changes Matrix values and all sect-based
interpretation is skipped while the value is unknown.

`matrix-destiny.com` may be used only for manual comparison. It is not a source
of formulas and no automated compatibility claim is exposed.

## Legacy source template

The former empty placeholders for Center, Top, Left, Right, Bottom, Karmic
Tail, Relationship Line, Money Line, and generation lines are superseded for
`mahesa-gantari-rws-v0.1` by the formula and ordered-line tables above. They
remain unresolved only for the public `unverified-v0` methodology and must not
be used to imply that the course methodology lacks formulas.

Age-cycle calculations remain unspecified. Course age ranges are descriptive
metadata only. Teacher verification and mapping to the public frontend's
semantic labels also remain pending.
