import pytest

from quiz.models import User
from quiz import app as test_app
from quiz.update_results import create_new_user, delete_user
from flask_login import current_user

# Adapted from https://flask.palletsprojects.com/en/stable/testing/#logging-in-and-out
@pytest.fixture()
def app():
    app = test_app
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": True
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def temporary_user():
    return User("test", "test@email.com", "123456")

def test_valid_sign_up(client, app, temporary_user):
    with app.test_request_context():
        response = client.post("/register", data={"username": "test",
                                                  "email": "test@email.com",
                                                  "password": "123456",
                                                  "confirm_password": "123456",
                                                  "submit": True}, follow_redirects=True)

        assert response.status_code == 200
        assert b"Cannot have that username." not in response.data
