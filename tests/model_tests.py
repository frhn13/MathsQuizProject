import bcrypt
import pytest
from flask_login import login_user, logout_user, current_user

from quiz import db
from quiz.models import User, QuestionDifficulties, QuestionTopics
from quiz.update_results import update_topic_information, update_difficulty_information, create_new_user, delete_user
from quiz import app as test_app

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

def test_create_new_user(client, app):
    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        username = current_user.username
        email = current_user.email
        password = current_user.password
        delete_user(User.query.filter_by(username="test").first())

        assert username == "test"
        assert email == "test@email.com"
        assert bcrypt.checkpw("123456".encode("utf-8"), password)


def test_delete_new_user(client, app):
    with app.test_request_context():
        user = User("test", "test@email.com", "123456")
        create_new_user(user)

        delete_user(User.query.filter_by(username="test").first())
        deleted_user = User.query.filter_by(username="test").first()
        assert not deleted_user

def test_update_topic_information(client, app):
    topic_counter = {
        "operations": [0, 0],
        "expressions": [1, 1],
        "equations": [2, 2],
        "fractions": [3, 3],
        "sequences": [4, 4],
        "hcf_lcm": [5, 5],
        "percentages": [6, 6],
        "calculus": [7, 7],
        "triangles": [8, 8],
        "circles": [9, 9],
        "graphs": [10, 10]
    }

    with app.test_request_context():
        user = User("test", "test@email.com", "123456")
        db.session.add(user)
        db.session.commit()
        created_user = User.query.filter_by(username="test").first()

        db.session.add(QuestionTopics(user_id=created_user.id))
        db.session.add(QuestionDifficulties(user_id=created_user.id))
        db.session.commit()
        login_user(created_user)
        update_topic_information(topic_counter)
        question_topics = QuestionTopics.query.filter_by(user_id=created_user.id).first()
        question_difficulties = QuestionDifficulties.query.filter_by(user_id=created_user.id).first()

        logout_user()
        db.session.delete(question_topics)
        db.session.delete(question_difficulties)
        db.session.delete(created_user)
        db.session.commit()

        assert question_topics.operations_right == 0
        assert question_topics.operations_wrong == 0
        assert question_topics.expressions_right == 1
        assert question_topics.expressions_wrong == 1
        assert question_topics.equations_right == 2
        assert question_topics.equations_wrong == 2
        assert question_topics.fractions_right == 3
        assert question_topics.fractions_wrong == 3
        assert question_topics.sequences_right == 4
        assert question_topics.sequences_wrong == 4
        assert question_topics.hcf_lcm_right == 5
        assert question_topics.hcf_lcm_wrong == 5
        assert question_topics.percentages_right == 6
        assert question_topics.percentages_wrong == 6
        assert question_topics.calculus_right == 7
        assert question_topics.calculus_wrong == 7
        assert question_topics.triangles_right == 8
        assert question_topics.triangles_wrong == 8
        assert question_topics.circles_right == 9
        assert question_topics.circles_wrong == 9
        assert question_topics.graphs_right == 10
        assert question_topics.graphs_wrong == 10


def test_update_difficulty_information(client, app):
    difficulty_counter = {
        f"level_{x}": [x, x] for x in range(1, 11)
    }

    with app.test_request_context():
        user = User("test", "test@email.com", "123456")
        db.session.add(user)
        db.session.commit()
        created_user = User.query.filter_by(username="test").first()

        db.session.add(QuestionTopics(user_id=created_user.id))
        db.session.add(QuestionDifficulties(user_id=created_user.id))
        db.session.commit()
        login_user(created_user)
        update_difficulty_information(difficulty_counter)
        question_topics = QuestionTopics.query.filter_by(user_id=created_user.id).first()
        question_difficulties = QuestionDifficulties.query.filter_by(user_id=created_user.id).first()

        logout_user()
        db.session.delete(question_topics)
        db.session.delete(question_difficulties)
        db.session.delete(created_user)
        db.session.commit()

        assert question_difficulties.level_one_right == 1
        assert question_difficulties.level_one_wrong == 1
        assert question_difficulties.level_two_right == 2
        assert question_difficulties.level_two_wrong == 2
        assert question_difficulties.level_three_right == 3
        assert question_difficulties.level_three_wrong == 3
        assert question_difficulties.level_four_right == 4
        assert question_difficulties.level_four_wrong == 4
        assert question_difficulties.level_five_right == 5
        assert question_difficulties.level_five_wrong == 5
        assert question_difficulties.level_six_right == 6
        assert question_difficulties.level_six_wrong == 6
        assert question_difficulties.level_seven_right == 7
        assert question_difficulties.level_seven_wrong == 7
        assert question_difficulties.level_eight_right == 8
        assert question_difficulties.level_eight_wrong == 8
        assert question_difficulties.level_nine_right == 9
        assert question_difficulties.level_nine_wrong == 9
        assert question_difficulties.level_ten_right == 10
        assert question_difficulties.level_ten_wrong == 10

"""def test_delete_user(client, app):
    with app.test_request_context():
        created_user = User.query.filter_by(username="test").first()
        question_topics = QuestionTopics.query.filter_by(user_id=created_user.id).first()
        question_difficulties = QuestionDifficulties.query.filter_by(user_id=created_user.id).first()
        db.session.delete(created_user)
        db.session.delete(question_topics)
        db.session.delete(question_difficulties)
        db.session.commit()
        assert True"""