import random

from quiz.QuizCode.percentages_generation import percentages_question_generation

def test_generate_percentages_questions(difficulty_factors, question_types):
    entered_difficulty = random.randint(2, 6)
    question, answer, difficulty_weighting = percentages_question_generation(entered_difficulty=entered_difficulty,
                                                                             difficulty_factors=difficulty_factors,
                                                                             question_types=question_types)
    assert type(answer) == int or answer in ("True", "False")

def test_generate_amount_from_percentage_question(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting = percentages_question_generation(entered_difficulty=3,
                                                                                 difficulty_factors=difficulty_factors,
                                                                                 question_types=question_types)
        if "% of" in question: break

    assert "% of" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_percentage_from_amount_question(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting = percentages_question_generation(entered_difficulty=3,
                                                                                 difficulty_factors=difficulty_factors,
                                                                                 question_types=question_types)
        if "as a percentage of" in question: break

    assert "as a percentage of" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_reverse_percentages_question(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting = percentages_question_generation(entered_difficulty=5,
                                                                                 difficulty_factors=difficulty_factors,
                                                                                 question_types=question_types)
        if "what is the original price?" in question: break

    assert "what is the original price?" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_compound_interest_question(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting = percentages_question_generation(entered_difficulty=5,
                                                                                 difficulty_factors=difficulty_factors,
                                                                                 question_types=question_types)
        if "interest rate per year" in question: break

    assert "interest rate per year" in question and (type(answer) == int or type(answer) == float or answer in ("True", "False"))