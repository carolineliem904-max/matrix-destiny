from datetime import date

from fastapi.testclient import TestClient

from app.api import experimental_teacher_teaser
from app.core.config import settings
from app.main import app
from app.matrix.calculator import MatrixCalculator
from app.matrix.rules import (
    TEACHER_TEASER_SUPPORTED_POSITIONS,
    TeacherTeaserMethodology,
    UnverifiedPlaceholderMethodology,
)

client = TestClient(app)

TAYLOR_REQUEST = {"birth_date": "1989-12-13", "name": "Taylor Swift"}
COMPATIBILITY_REQUEST = {
    "person_1": {
        "name": "Taylor Swift",
        "birth_date": "1989-12-13",
    },
    "person_2": {
        "name": "Travis Kelce",
        "birth_date": "1989-10-05",
    },
}


def test_experimental_personal_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", True)

    response = client.post(
        "/api/experimental/teacher-teaser/personal",
        json=TAYLOR_REQUEST,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["methodology_version"] == "teacher-teaser-v0.1"
    assert body["verified"] is False
    assert body["birth_date"] == "1989-12-13"
    assert [position["id"] for position in body["supported_positions"]] == list(
        TEACHER_TEASER_SUPPORTED_POSITIONS
    )
    assert all(
        position["verified"] is False
        and position["calculation_trace"]
        for position in body["supported_positions"]
    )
    assert body["unsupported_positions"]
    assert body["warnings"]


def test_experimental_compatibility_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", True)

    response = client.post(
        "/api/experimental/teacher-teaser/compatibility",
        json=COMPATIBILITY_REQUEST,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["methodology_version"] == "teacher-teaser-v0.1"
    assert body["verified"] is False
    assert body["person_1"]["name"] == "Taylor Swift"
    assert body["person_2"]["name"] == "Travis Kelce"
    assert body["person_1"]["verified"] is False
    assert body["person_2"]["verified"] is False
    assert len(body["supported_compatibility_positions"]) == len(
        TEACHER_TEASER_SUPPORTED_POSITIONS
    )
    assert all(
        position["calculation_trace"]
        for position in body["supported_compatibility_positions"]
    )


def test_experimental_endpoints_are_hidden_when_flag_is_disabled(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", False)

    personal = client.post(
        "/api/experimental/teacher-teaser/personal",
        json=TAYLOR_REQUEST,
    )
    compatibility = client.post(
        "/api/experimental/teacher-teaser/compatibility",
        json=COMPATIBILITY_REQUEST,
    )

    assert personal.status_code == 404
    assert compatibility.status_code == 404
    assert "ENABLE_EXPERIMENTAL_METHODOLOGIES" in personal.json()["detail"]


def test_experimental_personal_endpoint_rejects_invalid_birth_dates(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", True)

    malformed = client.post(
        "/api/experimental/teacher-teaser/personal",
        json={"birth_date": "1989-02-30"},
    )
    future = client.post(
        "/api/experimental/teacher-teaser/personal",
        json={"birth_date": "2999-01-01"},
    )

    assert malformed.status_code == 422
    assert future.status_code == 400


def test_experimental_api_delegates_to_existing_methodology(
    monkeypatch,
) -> None:
    monkeypatch.setattr(settings, "enable_experimental_methodologies", True)
    calls: list[date] = []
    original_calculate = TeacherTeaserMethodology.calculate

    def tracked_calculate(
        self: TeacherTeaserMethodology,
        birth_date: date,
    ):
        calls.append(birth_date)
        return original_calculate(self, birth_date)

    monkeypatch.setattr(
        TeacherTeaserMethodology,
        "calculate",
        tracked_calculate,
    )

    response = client.post(
        "/api/experimental/teacher-teaser/personal",
        json=TAYLOR_REQUEST,
    )

    assert response.status_code == 200
    assert calls == [date(1989, 12, 13)]


def test_public_calculator_default_is_unchanged() -> None:
    assert isinstance(MatrixCalculator().methodology, UnverifiedPlaceholderMethodology)
    assert (
        experimental_teacher_teaser.calculator.methodology.version
        == "teacher-teaser-v0.1"
    )
