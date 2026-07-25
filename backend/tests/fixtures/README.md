# Methodology Reference Fixtures

This directory stores manually editable reference data for methodology
verification. `synthetic_example.json` demonstrates the schema only. Its values
are invented, unverified, and excluded from verified-methodology acceptance
fixtures.

## Transcribing a Teacher Reference Chart

1. Create a new JSON file with a descriptive case name.
2. Copy the birth date exactly in `YYYY-MM-DD` format.
3. Record the methodology version stated by the course. Do not infer one.
4. Record the source name, source type, and a durable reference such as a
   lesson, page, timestamp, or chart identifier.
5. Add each source position using the teacher's exact label in `source_label`.
   Add `label_en` or `label_id` only when a translation has been reviewed.
6. Transcribe the final value into `expected_value`. Values must be in `1–22`.
   Set `is_raw_intermediate` to `true` only when the source explicitly shows an
   intermediate value before normalization.
7. Copy calculation steps into `calculation_trace` only when the source
   provides them. Do not reconstruct missing steps.
8. Add `chart_coordinates` only after the source position has been mapped to
   the frontend chart. Coordinates use percentages from `0` to `100`.
9. Start each directly copied position at `transcribed`. Use `inferred` when a
   value is reconstructed but cannot be read confidently in the source,
   `independently_checked` after a second person checks it, `teacher_verified`
   only after authoritative confirmation, or `disputed` when sources conflict.
10. For `teacher_verified`, provide non-synthetic source metadata,
    `verified_by`, and `verification_date`.

Synthetic fixtures must set `is_synthetic` to `true` and `source_type` to
`synthetic`. The acceptance-fixture selector always excludes them.

## Teacher Teaser Fixtures

- `teacher_teaser_taylor_swift.json` and
  `teacher_teaser_travis_kelce.json` contain personal example values transcribed
  from the supplied teacher-material requirements.
- `teacher_teaser_compatibility.json` uses the compatibility fixture schema and
  identifies both personal cases and birth dates.
- The compatibility Earth Line and Sky Line values are `inferred`, because the
  original slide was not attached for visual confirmation.
- All other supplied teacher-teaser values are `transcribed`.
- None of these fixtures are `teacher_verified` or acceptance-ready.
