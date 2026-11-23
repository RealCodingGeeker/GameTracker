import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from database import get_session


@pytest.fixture(name="client")
def client_fixture():
    # A brand-new in-memory database for every test
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


def make_game(client, title="Elden Ring", platform="PC", hours=85.5, completed=True):
    """Helper: create a game and return the response."""
    return client.post(
        "/games",
        json={
            "title": title,
            "platform": platform,
            "hours_played": hours,
            "completed": completed,
        },
    )


# CREATE
def test_create_game(client):
    response = make_game(client)
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Elden Ring"
    assert data["platform"] == "PC"
    assert data["hours_played"] == 85.5
    assert data["completed"] is True
    assert data["id"] == 1


# READ ALL
def test_read_all_games(client):
    make_game(client, title="Elden Ring")
    make_game(client, title="Hades", platform="Switch", hours=30, completed=False)

    response = client.get("/games")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == "Elden Ring"
    assert data[1]["title"] == "Hades"


# READ ONE
def test_read_one_game(client):
    game_id = make_game(client).json()["id"]

    response = client.get(f"/games/{game_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == game_id
    assert data["title"] == "Elden Ring"
    assert data["hours_played"] == 85.5


def test_read_one_game_not_found(client):
    response = client.get("/games/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


# UPDATE
def test_update_game(client):
    game_id = make_game(client).json()["id"]

    response = client.patch(f"/games/{game_id}", json={"hours_played": 90})
    data = response.json()

    assert response.status_code == 200
    assert data["hours_played"] == 90
    # fields we didn't send should be unchanged
    assert data["title"] == "Elden Ring"
    assert data["platform"] == "PC"
    assert data["completed"] is True


# DELETE
def test_delete_game(client):
    game_id = make_game(client).json()["id"]

    response = client.delete(f"/games/{game_id}")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    # confirm it's really gone
    assert client.get(f"/games/{game_id}").status_code == 404


# VALIDATION
def test_create_game_empty_title_rejected(client):
    response = make_game(client, title="")

    assert response.status_code == 422


def test_create_game_negative_hours_rejected(client):
    response = make_game(client, hours=-5)

    assert response.status_code == 422