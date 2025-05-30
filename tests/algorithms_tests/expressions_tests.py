import random

from quiz.QuizCode.expressions_generation import expressions_question_generation

def test_generate_expressions_question(difficulty_factors, question_types):
    entered_difficulty = random.randint(3, 6)
    question, answer, difficulty_weighting, time_needed = expressions_question_generation(entered_difficulty=entered_difficulty,
                                                                             question_types=question_types,
                                                                             difficulty_factors=difficulty_factors)
    assert "x" in answer

def test_factorisation_expression_question(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = expressions_question_generation(entered_difficulty=4,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "(" in question:
            break

    assert "x" in question and "(" in question and ")" in question and "/" not in question

def test_simplification_expression_question(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = expressions_question_generation(entered_difficulty=4,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "(" not in question and "/" not in question:
            break

    assert "x" in question and "(" not in question and ")" not in question and "/" not in question

def test_algebraic_fraction_expression_question(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = expressions_question_generation(entered_difficulty=6,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "/" in question:
            break

    assert "x" in question and "/" in question
