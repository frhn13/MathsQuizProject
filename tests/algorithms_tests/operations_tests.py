import random

from quiz.QuizCode.operations_generation import operations_question_generation

def test_generate_operations_question(difficulty_factors, question_types):
    entered_difficulty = random.randint(1, 5)
    question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=entered_difficulty,
                                                                                         question_types=question_types,
                                                                                         difficulty_factors=difficulty_factors)
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_addition(difficulty_factors, question_types):
    answer = 0
    time_needed = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3,
                                                                                             question_types=question_types,
                                                                                             difficulty_factors=difficulty_factors)
        if "+" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_subtraction(difficulty_factors, question_types):
    answer = 0
    time_needed = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3,
                                                                                             question_types=question_types,
                                                                                             difficulty_factors=difficulty_factors)
        if "-" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_multiplication(difficulty_factors, question_types):
    answer = 0
    time_needed = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3,
                                                                                             question_types=question_types,
                                                                                             difficulty_factors=difficulty_factors)
        if "*" in question and not "**" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_division(difficulty_factors, question_types):
    answer = 0
    time_needed = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3,
                                                                                             question_types=question_types,
                                                                                             difficulty_factors=difficulty_factors)
        if "/" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_brackets(difficulty_factors, question_types):
    answer = 0
    time_needed = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3,
                                                                                             question_types=question_types,
                                                                                             difficulty_factors=difficulty_factors)
        if "(" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60

def test_generate_operations_question_with_indices(difficulty_factors, question_types):
    answer = 0
    time_needed = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=3,
                                                                                             question_types=question_types,
                                                                                             difficulty_factors=difficulty_factors)
        if "**" in question:
            break
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60
