from quiz.QuizCode.expressions_generation import expressions_question_generation

def test_generate_expressions_question(difficulty_factors, question_types):
    question, answer, difficulty_weighting = expressions_question_generation(entered_difficulty=4,
                                                                             question_types=question_types,
                                                                             difficulty_factors=difficulty_factors)
    assert "x" in answer

def test_factorisation_expression_question(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = expressions_question_generation(entered_difficulty=4,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "(" in question:
            break

    assert "x" in question and "(" in question and ")" in question

def test_simplification_expression_question(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = expressions_question_generation(entered_difficulty=4,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "(" not in question and "/" not in question:
            break

    assert "x" in question and "(" not in question and ")" not in question and "/" not in question

def test_algebraic_fraction_expression_question(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = expressions_question_generation(entered_difficulty=6,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "/" in question:
            break

    assert "x" in question and "(" not in question and ")" not in question and "/" in question

def test_factorisation_expression_question_difficulty_too_high(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = expressions_question_generation(entered_difficulty=6,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "(" in question:
            break

    assert "x" in question and "(" not in question and not ")" in question

def test_simplification_expression_question_difficulty_too_high(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = expressions_question_generation(entered_difficulty=6,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "(" not in question and "/" not in question:
            break

    assert "x" in question and "/" in question

def test_algebraic_fraction_question_difficulty_too_low(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = expressions_question_generation(entered_difficulty=5,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "/" in question:
            break

    assert "x" in question and not "/" in question

