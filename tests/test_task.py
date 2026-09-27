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