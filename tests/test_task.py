import pytest

from app import create_app
from database import db


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Flask",
            "description": "Practice REST APIs",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 1
    assert data["title"] == "Learn Flask"
    assert data["description"] == "Practice REST APIs"
    assert data["completed"] is False

def test_get_tasks(client):
    client.post(
        "/tasks",
        json={
            "title": "Learn Flask",
            "description": "Practice REST APIs",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Practice pytest",
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["title"] == "Learn Flask"
    assert data[1]["title"] == "Write tests"

def test_get_single_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn Flask",
            "description": "Practice REST APIs",
        },
    )

    task_id = create_response.get_json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == task_id
    assert data["title"] == "Learn Flask"
    assert data["description"] == "Practice REST APIs"
    assert data["completed"] is False


def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Task not found"