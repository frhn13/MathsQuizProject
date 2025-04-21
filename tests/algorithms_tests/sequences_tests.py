import random

from quiz.QuizCode.sequences_generation import sequences_question_generation

def test_generate_sequence_questions(difficulty_factors, question_types):
    entered_difficulty = random.randint(2, 8)
    question, answer, difficulty_weighting = sequences_question_generation(entered_difficulty=entered_difficulty,
                                                                       question_types=question_types,
                                                                       difficulty_factors=difficulty_factors)

    assert "Find the next term in this" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_linear_sequence_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting = sequences_question_generation(entered_difficulty=3,
                                                                           question_types=question_types,
                                                                           difficulty_factors=difficulty_factors)
        if "Find the next term in this linear sequence" in question: break

    assert "Find the next term in this linear sequence" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_geometric_sequence_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting = sequences_question_generation(entered_difficulty=5,
                                                                           question_types=question_types,
                                                                           difficulty_factors=difficulty_factors)
        if "Find the next term in this geometric sequence" in question: break

    assert "Find the next term in this geometric sequence" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_quadratic_sequence_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting = sequences_question_generation(entered_difficulty=7,
                                                                           question_types=question_types,
                                                                           difficulty_factors=difficulty_factors)
        if "Find the next term in this quadratic sequence" in question: break

    assert "Find the next term in this quadratic sequence" in question and (type(answer) == int or answer in ("True", "False"))
