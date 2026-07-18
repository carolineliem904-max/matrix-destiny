# Destiny Matrix Methodology

Current methodology version: `unverified-v0`

The definitive Destiny Matrix formulas have not been supplied yet. This document tracks proposed concepts, required formulas, and verification status. The application must not silently choose between competing methods.

The concept names listed in `methodology_spec.md` are working placeholders only. They have not yet been verified against an authoritative Destiny Matrix source, and they have not yet been mapped to the frontend chart's current semantic labels such as Central Energy, Portrait, Talents, Relationship Line, Money Line, Ancestral Line, or Karmic Tail.

## Verification Checklist

| Proposed concept | Formula supplied | Implemented | Tested | Status |
| --- | --- | --- | --- | --- |
| Value normalization | No | No | No | Awaiting authoritative source |
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
