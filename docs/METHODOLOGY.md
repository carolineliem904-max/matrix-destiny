# Destiny Matrix Methodology

Current methodology version: `unverified-v0`

The definitive Destiny Matrix formulas have not been supplied yet. This document tracks proposed concepts, required formulas, and verification status. The application must not silently choose between competing methods.

The concept names listed in `methodology_spec.md` are working placeholders only. They have not yet been verified against an authoritative Destiny Matrix source, and they have not yet been mapped to the frontend chart's current semantic labels such as Central Energy, Portrait, Talents, Relationship Line, Money Line, Ancestral Line, or Karmic Tail.

## Verification Checklist

| Proposed concept | Formula supplied | Implemented | Tested | Status |
| --- | --- | --- | --- | --- |
| Value normalization | No | Experimental strategy only, not final methodology | Experimental normalizer tests only | Awaiting authoritative source |
| Center | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Top | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Left | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Right | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Bottom | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Karmic tail | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Relationship line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Money line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Male ancestral line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Female ancestral line | No | No, placeholder only where applicable | Existing placeholder behavior only | Awaiting authoritative source |
| Age cycles | No | No | No | Awaiting authoritative source |
| Verified reference fixtures | No | No | No, except existing placeholder behavior | Awaiting authoritative source |

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
