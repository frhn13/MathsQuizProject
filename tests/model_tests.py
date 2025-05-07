import bcrypt
import pytest
from flask_login import current_user

from quiz.models import User, QuestionDifficulties, QuestionTopics
from quiz.database_functions import (update_topic_information, update_difficulty_information, create_new_user, delete_user,
                                     get_user_results, get_topic_results, get_difficulty_results)
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

@pytest.fixture()
def topic_counter():
    return {
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

@pytest.fixture()
def topic_counter_different_percentages():
    return {
        "operations": [0, 0],
        "expressions": [1, 1],
        "equations": [3, 1],
        "fractions": [1, 3],
        "sequences": [2, 1],
        "hcf_lcm": [1, 2],
        "percentages": [6, 6],
        "calculus": [3, 5],
        "triangles": [5, 3],
        "circles": [7, 3],
        "graphs": [3, 7]
    }

@pytest.fixture()
def difficulty_counter():
    return {
        f"level_{x}": [x, x] for x in range(1, 11)
    }

@pytest.fixture()
def difficulty_counter_different_percentages():
    return {
        "level_1": [0, 0],
        "level_2": [1, 1],
        "level_3": [3, 1],
        "level_4": [1, 3],
        "level_5": [2, 1],
        "level_6": [1, 2],
        "level_7": [3, 5],
        "level_8": [5, 3],
        "level_9": [7, 3],
        "level_10": [3, 7]
    }

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

def test_update_topic_information(client, app, topic_counter):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter)
        question_topics = QuestionTopics.query.filter_by(user_id=current_user.id).first()
        delete_user(User.query.filter_by(username="test").first())

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


def test_update_difficulty_information(client, app, difficulty_counter):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter)
        question_difficulties = QuestionDifficulties.query.filter_by(user_id=current_user.id).first()
        delete_user(User.query.filter_by(username="test").first())

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

def test_get_user_results(client, app, difficulty_counter):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter)
        answers_correct, answers_incorrect, answers_percentage = get_user_results(current_user)
        delete_user(User.query.filter_by(username="test").first())

        assert answers_correct == 55
        assert answers_incorrect == 55
        assert answers_percentage == 50

def test_get_different_user_results(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_user_results(current_user)
        delete_user(User.query.filter_by(username="test").first())

        assert answers_correct == 26
        assert answers_incorrect == 26
        assert answers_percentage == 50

def test_get_topic_results_operations(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "operations")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 0
        assert answers_incorrect == 0
        assert answers_percentage == 0

def test_get_topic_results_expressions(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "expressions")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 1
        assert answers_incorrect == 1
        assert answers_percentage == 50

def test_get_topic_results_equations(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "equations")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 3
        assert answers_incorrect == 1
        assert answers_percentage == 75

def test_get_topic_results_fractions(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "fractions")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 1
        assert answers_incorrect == 3
        assert answers_percentage == 25

def test_get_topic_results_sequences(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "sequences")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 2
        assert answers_incorrect == 1
        assert answers_percentage == 67

def test_get_topic_results_hcf_lcm(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "hcf_lcm")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 1
        assert answers_incorrect == 2
        assert answers_percentage == 33

def test_get_topic_results_percentages(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "percentages")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 6
        assert answers_incorrect == 6
        assert answers_percentage == 50

def test_get_topic_results_calculus(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "calculus")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 3
        assert answers_incorrect == 5
        assert answers_percentage == 38

def test_get_topic_results_triangles(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "triangles")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 5
        assert answers_incorrect == 3
        assert answers_percentage == 62

def test_get_topic_results_circles(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "circles")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 7
        assert answers_incorrect == 3
        assert answers_percentage == 70

def test_get_topic_results_graphs(client, app, topic_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_topic_information(topic_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_topic_results(current_user, "graphs")
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 3
        assert answers_incorrect == 7
        assert answers_percentage == 30

def test_get_difficulty_results_level_one(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 1)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 0
        assert answers_incorrect == 0
        assert answers_percentage == 0

def test_get_difficulty_results_level_two(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 2)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 1
        assert answers_incorrect == 1
        assert answers_percentage == 50

def test_get_difficulty_results_level_three(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 3)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 3
        assert answers_incorrect == 1
        assert answers_percentage == 75

def test_get_difficulty_results_level_four(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 4)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 1
        assert answers_incorrect == 3
        assert answers_percentage == 25

def test_get_difficulty_results_level_five(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 5)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 2
        assert answers_incorrect == 1
        assert answers_percentage == 67

def test_get_difficulty_results_level_six(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 6)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 1
        assert answers_incorrect == 2
        assert answers_percentage == 33

def test_get_difficulty_results_level_seven(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 7)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 3
        assert answers_incorrect == 5
        assert answers_percentage == 38

def test_get_difficulty_results_level_eight(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 8)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 5
        assert answers_incorrect == 3
        assert answers_percentage == 62

def test_get_difficulty_results_level_nine(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 9)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 7
        assert answers_incorrect == 3
        assert answers_percentage == 70

def test_get_difficulty_results_level_ten(client, app, difficulty_counter_different_percentages):

    with app.test_request_context():
        create_new_user(User("test", "test@email.com", "123456"))
        update_difficulty_information(difficulty_counter_different_percentages)
        answers_correct, answers_incorrect, answers_percentage = get_difficulty_results(current_user, 10)
        delete_user(User.query.filter_by(username="test").first())
        assert answers_correct == 3
        assert answers_incorrect == 7
        assert answers_percentage == 30
