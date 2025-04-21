import random

from quiz.QuizCode.graphs_generation import graphs_questions_generation

def test_generate_distance_time_graphs_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        entered_difficulty = random.randint(2, 5)
        question, answer, difficulty_weighting, graph_values = graphs_questions_generation(
            entered_difficulty=entered_difficulty, difficulty_factors=difficulty_factors, question_types=question_types)
        if "distance travelled" in question or "average speed" in question or "How long does the person wait for before continuing?" in question: break

    assert "distance travelled" in question or "average speed" in question or "How long does the person wait for before continuing?" in question

def test_generate_velocity_time_graph_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, graph_values = graphs_questions_generation(
            entered_difficulty=7, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the acceleration for the first" in question or "What is the total distance covered in" in question: break

    assert "What is the acceleration for the first" in question or "What is the total distance covered in" in question

def test_generate_pie_chart_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, graph_values = graphs_questions_generation(
            entered_difficulty=3, difficulty_factors=difficulty_factors, question_types=question_types)
        if "People were asked to choose there favourite sport." in question and "then how many people chose" in question: break

    assert "People were asked to choose there favourite sport." in question and "then how many people chose" in question

def test_generate_graph_transformation_questions(difficulty_factors, question_types):
    question = ""
    for x in range(100):
        question, answer, difficulty_weighting, graph_values = graphs_questions_generation(
            entered_difficulty=8, difficulty_factors=difficulty_factors, question_types=question_types)
        if "is the maximum point of the curve y=f(x) then find the coordinates of the maximum point of the curve with the equation" in question: break

    assert "is the maximum point of the curve y=f(x) then find the coordinates of the maximum point of the curve with the equation" in question

def test_generate_perpendicular_line_graph_questions(difficulty_factors, question_types):
    question = ""
    answer = ""
    for x in range(100):
        question, answer, difficulty_weighting, graph_values = graphs_questions_generation(
            entered_difficulty=8, difficulty_factors=difficulty_factors, question_types=question_types)
        if "What is the equation of a perpendicular line to y" in question and "Give your answer in the form y=mx+c" in question and "x" in answer and "y" in answer: break

    assert "What is the equation of a perpendicular line to y" in question and "Give your answer in the form y=mx+c" in question and "x" in answer and "y" in answer
