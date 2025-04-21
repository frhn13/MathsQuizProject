import random

from quiz.QuizCode.circles_generation import circles_question_generation

def test_generate_circles_questions(difficulty_factors, question_types):
    entered_difficulty = random.randint(2, 8)
    question, answer, difficulty_weighting, circle_image_values, calculator_needed = circles_question_generation(
        entered_difficulty=entered_difficulty, difficulty_factors=difficulty_factors, question_types=question_types)

    assert ("If the radius of a circle" in question or "If the diameter of a circle" in question and
            (type(answer) == int or type(answer) == float or answer in ("True", "False")))

def test_generate_circle_area_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, circle_image_values, calculator_needed = circles_question_generation(
            entered_difficulty=3, difficulty_factors=difficulty_factors, question_types=question_types)
        if "then what is its area?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False")): break

    assert "then what is its area?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False"))

def test_generate_circle_circumference_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, circle_image_values, calculator_needed = circles_question_generation(
            entered_difficulty=3, difficulty_factors=difficulty_factors, question_types=question_types)
        if "then what is its circumference?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False")): break

    assert "then what is its circumference?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False"))

def test_generate_circle_sector_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, circle_image_values, calculator_needed = circles_question_generation(
            entered_difficulty=5, difficulty_factors=difficulty_factors, question_types=question_types)
        if "then what is the area of the sector?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False")): break

    assert "then what is the area of the sector?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False"))

def test_generate_circle_arc_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, circle_image_values, calculator_needed = circles_question_generation(
            entered_difficulty=5, difficulty_factors=difficulty_factors, question_types=question_types)
        if "then what is the length of the sector's arc?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False")): break

    assert "then what is the length of the sector's arc?" in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False"))

def test_generate_circle_shaded_area_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, circle_image_values, calculator_needed = circles_question_generation(
            entered_difficulty=6, difficulty_factors=difficulty_factors, question_types=question_types)
        if "then find the area of the semicircle formed by the chord." in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False")): break

    assert "then find the area of the semicircle formed by the chord." in question and (type(answer) == int or type(answer) == float or
                                                     answer in ("True", "False"))