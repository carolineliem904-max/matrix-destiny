from app.interpretations.repository import InterpretationRepository


def test_position_interpretations_load_in_both_languages() -> None:
    repository = InterpretationRepository()

    assert repository.get_position("center", "en") is not None
    assert repository.get_position("center", "id") is not None


def test_sample_energy_schema_loads() -> None:
    repository = InterpretationRepository()

    energy = repository.get_energy(1, "en")

    assert energy is not None
    assert energy.energy == 1
    assert energy.source_status == "draft"
