from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_calculate_matrix_returns_reading() -> None:
    response = client.post(
        "/api/matrix/calculate",
        json={"birth_date": "1990-08-16", "language": "en", "name": "Mira"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["methodology_version"] == "unverified-v0"
    assert body["name"] == "Mira"
    assert len(body["positions"]) == 7
    assert body["positions"][0]["position"]["verified"] is False
    assert "reflection" in body["disclaimer"].lower()


def test_calculate_matrix_rejects_future_date() -> None:
    response = client.post(
        "/api/matrix/calculate",
        json={"birth_date": "2999-01-01", "language": "en"},
    )

    assert response.status_code == 400
