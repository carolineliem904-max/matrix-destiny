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
