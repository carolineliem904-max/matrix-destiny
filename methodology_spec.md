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

### Center
- Meaning:
- Formula:
- Worked example:

### Top
- Meaning:
- Formula:
- Worked example:

### Left
- Meaning:
- Formula:
- Worked example:

### Right
- Meaning:
- Formula:
- Worked example:

### Bottom
- Meaning:
- Formula:
- Worked example:

## Karmic tail
- Components:
- Formula:
- Order of numbers:
- Worked example:

## Relationship line
- Components:
- Formula:
- Worked example:

## Money line
- Components:
- Formula:
- Worked example:

## Male ancestral line
- Components:
- Formula:
- Worked example:

## Female ancestral line
- Components:
- Formula:
- Worked example:

## Age cycles
- Starting age:
- Interval:
- Formula:
- Boundary rules:
- Worked example:

## Verified example charts

### Example 1
- Birth date:
- Expected positions:
- Source:

### Example 2
- Birth date:
- Expected positions:
- Source:
