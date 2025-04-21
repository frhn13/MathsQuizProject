from quiz.QuizCode.fractions_generation import fractions_question_generation

def test_generate_fractions_questions(difficulty_factors, question_types):
    question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty=4,
                                                                           question_types=question_types,
                                                                           difficulty_factors=difficulty_factors)

    for char in answer:
        assert char.isnumeric() or char == "/" or char == "x" or char == "-" or answer in ("True", "False")

def test_generate_fraction_conversion_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty=2,
                                                                               question_types=question_types,
                                                                               difficulty_factors=difficulty_factors)
        if "Convert" in question: break

    assert "Convert" in question and ("to a fraction" in question or "to a decimal" in question or "to a percentage" in question)

def test_generate_fraction_addition_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty=4,
                                                                               question_types=question_types,
                                                                               difficulty_factors=difficulty_factors)
        if "/" in question and "+" in question: break

    assert "/" in question and "+" in question and not "x" in question

def test_generate_fraction_subtraction_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty=5,
                                                                               question_types=question_types,
                                                                               difficulty_factors=difficulty_factors)
        if "/" in question and "-" in question: break

    assert "/" in question and "-" in question and not "x" in question

def test_generate_fraction_multiplication_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty=4,
                                                                               question_types=question_types,
                                                                               difficulty_factors=difficulty_factors)
        if "/" in question and "*" in question: break

    assert "/" in question and "*" in question and not "x" in question

def test_generate_fraction_division_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty=4,
                                                                               question_types=question_types,
                                                                               difficulty_factors=difficulty_factors)
        if "/" in question and "/" in question: break

    assert "/" in question and "/" in question and not "x" in question

def test_algebraic_fraction_expression_question(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty=6,
                                                                                 question_types=question_types,
                                                                                 difficulty_factors=difficulty_factors)
        if "/" in question:
            break

    assert "x" in question and "(" not in question and ")" not in question and "/" in question