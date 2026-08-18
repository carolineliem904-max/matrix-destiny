import importlib

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def post(client: TestClient, payload: dict | None = None):
    return client.post(
        "/api/experimental/mahesa-gantari/personal",
        json=payload or {"birth_date": "1988-08-18"},
    )


def test_disabled_returns_404(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", False)
    assert post(client).status_code == 404


@pytest.mark.parametrize("sect", ["day", "night", "unknown"])
def test_complete_response_and_inactive_sect(
    client: TestClient, monkeypatch, sect: str
) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", True)
    response = post(client, {"birth_date": "1988-08-18", "sect": sect})
    assert response.status_code == 200
    body = response.json()
    assert body["methodology_version"] == "mahesa-gantari-rws-v0.1"
    assert body["status"] == "course_transcribed"
    assert body["verified"] is False
    assert len(body["points"]) == 32
    assert body["sect_context"]["sect"] == sect
    assert body["sect_context"]["interpretation_modifier_active"] is False
    assert body["sect_context"]["weighting_rule_version"] is None
    by_value = {point["value"]: point["arcana_name"] for point in body["points"]}
    assert by_value[8] == "Strength"
    assert by_value[22] == "The Fool"
    assert body["money_line"]["ordered_point_ids"] == ["L", "L_plus_N", "N"]
    assert body["relationship_line"]["line_id"] != body["karmic_tail"]["line_id"]
    assert body["purpose"]["spiritual_knowledge"]["calculation_trace"]
    assert body["health_card"]["verified"] is False


def test_default_sect_and_invalid_inputs(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", True)
    assert post(client).json()["sect_context"]["sect"] == "unknown"
    assert post(client, {"birth_date": "not-a-date"}).status_code == 422
    assert post(client, {"birth_date": "1988-08-18", "sect": "dawn"}).status_code == 422
    assert post(client, {"birth_date": "2999-01-01"}).status_code == 400
