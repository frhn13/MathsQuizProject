import pytest

from quiz.QuizCode.operations_generation import operations_question_generation
from quiz.QuizCode.fractions_generation import fractions_question_generation

@pytest.fixture()
def difficulty_factors():
    return {
        "maths_topic": [0, 0.2],  # Topic being tested
        "question_type": [0, 0.1],  # Free-text, multiple choice, True/False
        "answers_similarity": [0, 0.15],  # Similarity of potential answers in MCQs
        "difficulty_of_values": [0, 0.15],  # Values used in the question
        "number_of_steps": [0, 0.1],  # Steps needed to find answer
        "depth_of_knowledge": [0, 0.1],  # Extra information needed to answer question, like formulae, certain values
        "difficulty_of_answer": [0, 0.15],  # Value of the answer
        "multiple_topics": [0, 0.1]  # Whether question combines multiple topic ideas
    }

@pytest.fixture()
def question_types():
    return ["free_text", "multiple-choice", "true/false"]

def test_generate_operations_question(difficulty_factors, question_types):
    question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3, question_types=question_types, difficulty_factors=difficulty_factors)
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_addition(difficulty_factors, question_types):
    while True:
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3, question_types=question_types, difficulty_factors=difficulty_factors)
        if "+" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_subtraction(difficulty_factors, question_types):
    while True:
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3, question_types=question_types, difficulty_factors=difficulty_factors)
        if "-" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_multiplication(difficulty_factors, question_types):
    while True:
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3, question_types=question_types, difficulty_factors=difficulty_factors)
        if "*" in question and not "**" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_division(difficulty_factors, question_types):
    while True:
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3, question_types=question_types, difficulty_factors=difficulty_factors)
        if "/" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_brackets(difficulty_factors, question_types):
    while True:
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3, question_types=question_types, difficulty_factors=difficulty_factors)
        if "(" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_indices(difficulty_factors, question_types):
    while True:
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3, question_types=question_types, difficulty_factors=difficulty_factors)
        if "**" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

