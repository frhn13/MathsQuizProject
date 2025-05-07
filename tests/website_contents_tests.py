import pytest

from quiz.models import User
from quiz import app as test_app
from quiz.database_functions import create_new_user, delete_user

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

def test_anonymous_navbar_register(client):
    response = client.get("/register", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign Up" in response.data
    assert b"Login" in response.data

def test_anonymous_navbar_login(client):
    response = client.get("/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign Up" in response.data
    assert b"Login" in response.data

def test_logged_in_navbar_quiz_selection_quiz_selection(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/quiz-selection", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert response.status_code == 200
        assert b"Select Quiz" in response.data
        assert b"Tutorial" in response.data
        assert b"Results" in response.data
        assert b"Maximum Results" in response.data
        assert b"Leaderboard" in response.data
        assert b"Log Out" in response.data
        assert b"Delete Account" in response.data
        assert b"Now logged in as test" in response.data


def test_logged_in_navbar_quiz_selection_tutorial(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/tutorial", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert response.status_code == 200
        assert b"Select Quiz" in response.data
        assert b"Tutorial" in response.data
        assert b"Results" in response.data
        assert b"Maximum Results" in response.data
        assert b"Leaderboard" in response.data
        assert b"Log Out" in response.data
        assert b"Delete Account" in response.data
        assert b"Now logged in as test" in response.data

def test_logged_in_navbar_quiz_selection_quiz_results(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/view-results", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert response.status_code == 200
        assert b"Select Quiz" in response.data
        assert b"Tutorial" in response.data
        assert b"Results" in response.data
        assert b"Maximum Results" in response.data
        assert b"Leaderboard" in response.data
        assert b"Log Out" in response.data
        assert b"Delete Account" in response.data
        assert b"Now logged in as test" in response.data

def test_logged_in_navbar_quiz_selection_max_results(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/view-max-results", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert response.status_code == 200
        assert b"Select Quiz" in response.data
        assert b"Tutorial" in response.data
        assert b"Results" in response.data
        assert b"Maximum Results" in response.data
        assert b"Leaderboard" in response.data
        assert b"Log Out" in response.data
        assert b"Delete Account" in response.data
        assert b"Now logged in as test" in response.data

def test_logged_in_navbar_quiz_selection_leaderboard(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/leaderboard", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert response.status_code == 200
        assert b"Select Quiz" in response.data
        assert b"Tutorial" in response.data
        assert b"Results" in response.data
        assert b"Maximum Results" in response.data
        assert b"Leaderboard" in response.data
        assert b"Log Out" in response.data
        assert b"Delete Account" in response.data
        assert b"Now logged in as test" in response.data

def test_logged_in_navbar_quiz_selection_delete_account(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/delete-account", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert response.status_code == 200
        assert b"Select Quiz" in response.data
        assert b"Tutorial" in response.data
        assert b"Results" in response.data
        assert b"Maximum Results" in response.data
        assert b"Leaderboard" in response.data
        assert b"Log Out" in response.data
        assert b"Delete Account" in response.data
        assert b"Now logged in as test" in response.data

def test_signup_page(client):
    response = client.get("/register", follow_redirects=True)
    assert response.status_code == 200
    assert b"<h1>Create an Account</h1>" in response.data
    assert b"Username" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm Password" in response.data

def test_alternate_signup_page(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"<h1>Create an Account</h1>" in response.data
    assert b"Username" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Confirm Password" in response.data

def test_login_page(client):
    response = client.get("/login", follow_redirects=True)
    assert b"<h1>Login</h1>" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data
    assert b"Email" not in response.data
    assert b"Confirm Password" not in response.data
    assert b"<h1>Create an Account</h1>" not in response.data

def test_quiz_selection_page(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/quiz-selection", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert b"<h1>Quiz Selection</h1>" in response.data
        assert b"Operations, Difficulty: 1-5" in response.data
        assert b"Fractions, Difficulty: 2-6" in response.data
        assert b"Calculus, Difficulty: 7-10" in response.data
        assert b"Equations, Difficulty: 4-8" in response.data
        assert b"Expressions, Difficulty: 3-6" in response.data
        assert b"Sequences, Difficulty: 3-8" in response.data
        assert b"HCF, LCM and Prime Factors, Difficulty: 2-5" in response.data
        assert b"Percentages, Difficulty: 3-6" in response.data
        assert b"Triangles, Difficulty: 2-7" in response.data
        assert b"Circles, Difficulty: 3-7" in response.data
        assert b"Graphs, Difficulty: 2-8" in response.data

        assert b"Enter the number of questions to answers:" in response.data
        assert b"Enter the starting difficulty of the questions:" in response.data
        assert b"Submit" in response.data

def test_tutorial_page(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/tutorial", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert b"<h1>Tutorial Page</h1>" in response.data
        assert b"<h3>Basics of Website</h3>" in response.data
        assert b"<h3>Question Selection</h3>" in response.data
        assert b"<h3>Question Types and Topics</h3>" in response.data
        assert b"<h3>Answering Questions</h3>" in response.data
        assert b"<h3>Viewing Results</h3>" in response.data
        assert b"<h3>Deleting Account</h3>" in response.data

def test_results_page(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/view-results", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert b"<h1>Results Page</h1>" in response.data
        assert b"Choose results to return:" in response.data
        assert b"All Results" in response.data
        assert b"All results for a specific Difficulty" in response.data
        assert b"All results for a specific Topic" in response.data
        assert b"Select User:" in response.data
        assert b"Compare Results with Another Person?" in response.data
        assert b"Submit" in response.data

def test_max_results_page(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/view-max-results", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert b"<h1>Highest Results Page</h1>" in response.data
        assert b"Choose whether you want to see the players with the highest number or the highest percentage of correct questions:" in response.data
        assert b"Highest Number" in response.data
        assert b"Highest Percentage" in response.data
        assert b"Choose results to return" in response.data
        assert b"All Results" in response.data
        assert b"All results for a specific Difficulty" in response.data
        assert b"All results for a specific Topic" in response.data
        assert b"Submit" in response.data

def test_leaderboard_page(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/leaderboard", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert b"Leaderboard" in response.data
        assert b"Choose whether you want the leaderboard to display the players by their number of correct answers or by their percentage of correct answers." in response.data
        assert b"Highest Number" in response.data
        assert b"Highest Percentage" in response.data
        assert b"Choose results to return" in response.data
        assert b"All Results" in response.data
        assert b"All results for a specific Difficulty" in response.data
        assert b"All results for a specific Topic" in response.data
        assert b"Submit" in response.data

def test_delete_account_page(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        response = client.get("/delete-account", follow_redirects=True)
        delete_user(User.query.filter_by(username="test").first())

        assert b"<h1>To Delete your Account enter your Username and Password</h1>" in response.data
        assert b"Username:" in response.data
        assert b"Password:" in response.data
        assert b"Confirm Deletion" in response.data
