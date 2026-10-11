import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add() -> None:
    response = client.get("/add", params={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_add_invalid_input() -> None:
    response = client.get("/add", params={"a": "x", "b": 3})
    assert response.status_code == 422


def test_multiply() -> None:
    response = client.get("/multiply", params={"a": 10, "b": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 50}


def test_multiply_invalid_input() -> None:
    response = client.get("/multiply", params={"a": "A", "b": 5})
    assert response.status_code == 422


def test_chat() -> None:
    response = client.post(
        "/chat", json={"message": "Hello world!", "temperature": 0.5, "top_p": 0.5}
    )
    assert response.status_code == 200
    assert response.json() == {"reply": "Echo: Hello world!", "tokens_estimate": 2}


@pytest.mark.parametrize(
    "payload",
    [
        {"message": ""},
        {"message": "salam", "temperature": 5},
        {"message": "salam", "top_p": 1.5},
    ],
)
def test_chat_invalid_input(payload: dict[str, object]) -> None:
    response = client.post("/chat", json=payload)
    assert response.status_code == 422
