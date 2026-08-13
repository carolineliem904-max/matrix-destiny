# Arcana Content Schema

Arcana semantic content is versioned independently from Matrix calculations.
The initial profile is `rws-mahesa-gantari-v0.1`, sourced from *Matrix of
Destiny Basic 01* page 12 and marked `verified: false`.

## Record Shape

Each Arcana record contains:

- `energy_number`: Matrix energy `1-22`; energy `0` is invalid.
- `arcana_name`: RWS name for the versioned profile.
- `tarot_profile`: semantic ordering identifier.
- `neutral_keywords`: short independently written descriptors.
- `in_plus`, `in_minus`, `karmic_tasks`, `recommendations`: reserved structured
  fields, empty for this milestone.
- `astrology_associations`: structured association fields.
- `source_metadata`: document, page, evidence status, and verification state.
- `language`: language of the independently written content.
- `publication_status`: currently `reference_only`.

## Astrology Associations

The schema keeps these concepts separate:

- `direct_planet_association`
- `zodiac_association`
- `zodiac_ruler_derived`
- `house_association`
- `interpretation_modifier`

Only direct planet or zodiac associations visibly listed on Module 01 page 12
are populated. Zodiac rulers and houses remain empty rather than being inferred
without a selected source rule. Interpretation modifiers remain null.

## RWS Ordering

- 8: Strength
- 11: Justice
- 22: The Fool

This profile differs from Marseille-based ordering. Calculation values do not
change when a semantic profile is selected.

## Sect Context

Sect input accepts `day`, `night`, or `unknown`, defaulting to `unknown`.
Day/night choices are marked `user_provided`; no birth time or location is
required and no date-only inference occurs.

The context exposes placeholders for future directly and indirectly affected
Arcana, contrary-to-sect malefic, rule version, and evidence status. All lists
are empty, the weighting version is null, and
`interpretation_modifier_active` is `false` until an explicit course rule is
documented.

## Source Handling

Private course PDFs and extracted Markdown are excluded through
`/private_sources/`. Repository content must remain independently structured
and concise. Complete course interpretation text must not be copied into public
data files or API responses.
