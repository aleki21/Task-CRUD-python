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

def test_create_task_requires_title(client):
    response = client.post(
        "/tasks",
        json={
            "description": "A task without a title",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Validation failed"
    assert data["details"]["title"] == "Title is required"


def test_create_task_rejects_empty_title(client):
    response = client.post(
        "/tasks",
        json={
            "title": "   ",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["details"]["title"] == "Title cannot be empty"


def test_create_task_rejects_invalid_title_type(client):
    response = client.post(
        "/tasks",
        json={
            "title": 123,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["details"]["title"] == "Title must be a string"


def test_create_task_rejects_invalid_completed_type(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Flask",
            "completed": "yes",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["details"]["completed"] == "Completed must be a boolean"


def test_create_task_rejects_long_title(client):
    response = client.post(
        "/tasks",
        json={
            "title": "A" * 101,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["details"]["title"] == "Title must not exceed 100 characters"


def test_create_task_rejects_long_description(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Flask",
            "description": "A" * 501,
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["details"]["description"] == (
        "Description must not exceed 500 characters"
    )

def test_create_task_rejects_invalid_json(client):
    response = client.post(
        "/tasks",
        data='{"title": "Learn Flask"',
        content_type="application/json",
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid JSON"
    assert data["message"] == "Request body must contain valid JSON"

def test_create_task_rejects_non_object_json(client):
    response = client.post(
        "/tasks",
        json=["Learn Flask"],
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Validation failed"
    assert data["details"]["body"] == "Request body must be a JSON object"


def test_update_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn Flask",
            "description": "Practice REST APIs",
        },
    )

    task_id = create_response.get_json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Master Flask",
            "description": "Build production-ready APIs",
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == task_id
    assert data["title"] == "Master Flask"
    assert data["description"] == "Build production-ready APIs"
    assert data["completed"] is True

def test_update_nonexistent_task(client):
    response = client.put(
        "/tasks/999",
        json={
            "title": "Updated task",
            "description": "This task does not exist",
            "completed": True,
        },
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Task not found"


def test_update_task_rejects_invalid_data(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn Flask",
        },
    )

    task_id = create_response.get_json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "",
        },
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Validation failed"
    assert data["details"]["title"] == "Title cannot be empty"


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "description": "This task should be removed",
        },
    )

    task_id = create_response.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.data == b""

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404

def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Task not found"