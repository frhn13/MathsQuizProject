from quiz.QuizCode.equations_generation import equations_question_generation

def test_generate_equations_questions(difficulty_factors, question_types):
    question, answer, difficulty_weighting, multiple_answers, calculator_needed = equations_question_generation(
                                                                             entered_difficulty=5,
                                                                             question_types=question_types,
                                                                             difficulty_factors=difficulty_factors)
    assert type(answer) == list and (type(answer[0]) == int or type(answer[0]) == float)

def test_generate_linear_equations_questions(difficulty_factors, question_types):
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, multiple_answers, calculator_needed = equations_question_generation(
            entered_difficulty=4,
            question_types=question_types,
            difficulty_factors=difficulty_factors)
        if "Find x to 2 decimal places." in question: break

    assert type(answer) == list and len(answer) == 1

def test_generate_whole_quadratic_equations_questions(difficulty_factors, question_types):
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, multiple_answers, calculator_needed = equations_question_generation(
            entered_difficulty=5,
            question_types=question_types,
            difficulty_factors=difficulty_factors)
        if "Find both values of x to 2 decimal places." in question and answer[0] == int(answer[0]): break

    assert type(answer) == list and (len(answer) == 1 or len(answer) == 2)

def test_generate_floating_point_quadratic_equations_questions(difficulty_factors, question_types):
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, multiple_answers, calculator_needed = equations_question_generation(
            entered_difficulty=6,
            question_types=question_types,
            difficulty_factors=difficulty_factors)
        if "Find both values of x to 2 decimal places." in question and answer[0] != int(answer[0]): break

    assert type(answer) == list and (len(answer) == 1 or len(answer) == 2)

def test_generate_linear_simultaneous_equations_questions(difficulty_factors, question_types):
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, multiple_answers, calculator_needed = equations_question_generation(
            entered_difficulty=6,
            question_types=question_types,
            difficulty_factors=difficulty_factors)
        if "Find the value of x and y to 2 decimal places." in question and answer[0] == int(answer[0]): break

    assert type(answer) == list and len(answer) == 2

def test_generate_quadratic_simultaneous_equations_questions(difficulty_factors, question_types):
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, multiple_answers, calculator_needed = equations_question_generation(
            entered_difficulty=8,
            question_types=question_types,
            difficulty_factors=difficulty_factors)
        if "Find both values of x and y to 2 decimal places." in question and answer[0] == int(answer[0]): break

    assert type(answer) == list and len(answer) == 4