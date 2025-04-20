from quiz.QuizCode.operations_generation import operations_question_generation

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
