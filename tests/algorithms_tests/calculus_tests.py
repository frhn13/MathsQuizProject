import random

from quiz.QuizCode.calculus_generation import calculus_questions_generation

def test_generate_differentiation_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        entered_difficulty = random.randint(7, 10)
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=entered_difficulty, difficulty_factors=difficulty_factors, question_types=question_types)
        if "derivative" in question or ("f(x)" in question and "∫" not in question) or "y=mx+c" in question: break

    assert "derivative" in question or ("f(x)" in question and "∫" not in question) or "y=mx+c" in question

def test_generate_integration_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        entered_difficulty = random.randint(8, 10)
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=entered_difficulty, difficulty_factors=difficulty_factors, question_types=question_types)
        if "∫ f(x)" in question or "What is the area of under the curve y=f(x)" in question: break

    assert "∫ f(x)" in question or "What is the area of under the curve y=f(x)" in question

def test_generate_basic_differentiation_questions(difficulty_factors, question_types):
    question = ""
    answer = ""
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=7, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the first order derivative" in question and "x" in answer: break

    assert "What is the first order derivative" in question and "x" in answer

def test_generate_second_order_differentiation_questions(difficulty_factors, question_types):
    question = ""
    answer = ""
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=8, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the second order derivative" in question and "x" in answer: break

    assert "What is the second order derivative" in question and "x" in answer

def test_generate_answer_from_derivative_differentiation_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=8, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the answer to" in question and "f(x)" in question and not "∫" in question and answer.isnumeric(): break

    assert "What is the answer to" in question and "f(x)" in question and not "∫" in question and answer.isnumeric()


def test_generate_x_from_derivative_differentiation_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=8, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the value of x when f\'(x) = 0 and f(x) =" in question and not "∫" in question: break

    assert "What is the value of x when f\'(x) = 0 and f(x) =" in question and not "∫" in question

def test_generate_tangents_differentiation_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=9, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the equation of the tangent to the curve" in question and "Give your answer in the form y=mx+c" in question and not "∫" in question: break

    assert "What is the equation of the tangent to the curve" in question and "Give your answer in the form y=mx+c" in question and not "∫" in question and "x" in answer and "y" in answer

def test_generate_normals_differentiation_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=10, difficulty_factors=difficulty_factors, question_types=question_types)
        if ("What is the equation of the normal to the curve" in question and
                "Give your answer in the form y=mx+c and give answers in the form of fractions where needed."
                in question and not "∫" in question): break

    assert ("What is the equation of the normal to the curve" in question and
            "Give your answer in the form y=mx+c and give answers in the form of fractions where needed."
            in question and not "∫" in question and "x" in answer and "y" in answer)

def test_generate_basic_integration_questions(difficulty_factors, question_types):
    question = ""
    answer = ""
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=8, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is ∫ f(x) dx when f(x)" in question and "+ c" in answer: break

    assert "What is ∫ f(x) dx when f(x)" in question and "+ c" in answer

def test_generate_definite_integrals_integration_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=9, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is ∫ f(x) from " in question and "Give answers in the form of fractions where needed." in question: break

    assert "What is ∫ f(x) from " in question and "Give answers in the form of fractions where needed." in question

def test_generate_finding_area_integration_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=9, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the area of under the curve y=f(x) over the interval" in question and "Give answers in the form of fractions where needed." in question and "-" not in question: break

    assert "What is the area of under the curve y=f(x) over the interval" in question and "Give answers in the form of fractions where needed." in question and "-" not in question

def test_generate_finding_complex_area_integration_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(
            entered_difficulty=10, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the area of under the curve y=f(x) over the interval" in question and "Give answers in the form of fractions where needed." in question and "-" in question: break

    assert "What is the area of under the curve y=f(x) over the interval" in question and "Give answers in the form of fractions where needed." in question and "-" in question