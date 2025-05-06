import random

from quiz.QuizCode.triangles_generation import triangles_question_generation

def test_triangle_question_generation(difficulty_factors, question_types):
    entered_difficulty = random.randint(2, 7)
    question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
        entered_difficulty=entered_difficulty, difficulty_factors=difficulty_factors, question_types=question_types)
    assert "What is x" in question or "What is the area" in question or "What is the perimeter" in question

def test_triangle_simple_area_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=2, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the area of this triangle? Answer to the nearest whole number." in question and type(answer) == int: break

    assert "What is the area of this triangle? Answer to the nearest whole number." in question and type(answer) == int

def test_triangle_simple_perimeter_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=2, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the perimeter of this triangle? Answer to the nearest whole number." in question and type(answer) == int: break

    assert "What is the perimeter of this triangle? Answer to the nearest whole number." in question and type(answer) == int

def test_triangle_simple_angles_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    image_values = {}
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=2, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is x? Answer to the nearest whole number." in question and answer == int(round(image_values["angle_c"], 0)): break

    assert "What is x? Answer to the nearest whole number." in question and answer == int(round(image_values["angle_c"], 0))

def test_triangle_pythagoras_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    image_values = {}
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=4, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["length_a"], 0)) or answer == int(round(image_values["length_b"], 0))): break

    assert "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["length_a"], 0)) or answer == int(round(image_values["length_b"], 0)))

def test_triangle_trigonometry_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    image_values = {}
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=4, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["angle_a"], 0)) or answer == int(round(image_values["length_c"], 0))): break

    assert "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["angle_a"], 0)) or answer == int(round(image_values["length_c"], 0)))

def test_triangle_sine_rule_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    image_values = {}
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=5, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["angle_c"], 0)) or answer == int(round(image_values["length_c"], 0))): break

    assert "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["angle_c"], 0)) or answer == int(round(image_values["length_c"], 0)))

def test_triangle_cosine_rule_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    image_values = {}
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=6, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["angle_c"], 0)) or answer == int(round(image_values["length_c"], 0))): break

    assert "What is x? Answer to the nearest whole number." in question and (answer == int(round(image_values["angle_c"], 0)) or answer == int(round(image_values["length_c"], 0)))

def test_triangle_complex_area_question_generation(difficulty_factors, question_types):
    question = ""
    answer = 0
    image_values = {}
    for x in range(100):
        question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(
            entered_difficulty=6, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the area of this triangle? Answer to the nearest whole number." in question and type(answer) == int: break

    assert "What is the area of this triangle? Answer to the nearest whole number." in question and (type(answer) == int)
