import random

from .operations_generation import operations_question_generation
from .fractions_generation import fractions_question_generation
from .expressions_generation import expressions_question_generation
from .equations_generation import equations_question_generation
from .percentages_generation import percentages_question_generation
from .sequences_generation import sequences_question_generation
from .triangles_generation import triangles_question_generation
from .calculus_generation import calculus_questions_generation
from .graphs_generation import graphs_questions_generation
from .circles_generation import circles_question_generation
from .hcf_lcm_generation import hcf_lcm_question_generation
from .min_and_max_difficulties import *

def question_topic_selection(selected_topics : list, entered_difficulty : int, question_types : list):
    image_values = None
    graph_values = None
    circle_image_values = None
    is_topic_chosen = False
    calculator_needed = False
    multiple_answers = "No"
    time_needed = 60

    difficulty_factors = {
        "maths_topic": [0, 0.2],  # Topic being tested
        "question_type": [0, 0.1],  # Free-text, multiple choice, True/False
        "answers_similarity": [0, 0.15],  # Similarity of potential answers in MCQs
        "difficulty_of_values": [0, 0.15],  # Values used in the question
        "number_of_steps": [0, 0.1],  # Steps needed to find answer
        "depth_of_knowledge": [0, 0.1],  # Extra information needed to answer question, like formulae, certain values
        "difficulty_of_answer": [0, 0.15],  # Value of the answer
        "multiple_topics": [0, 0.1]  # Whether question combines multiple topic ideas
    }
    while not is_topic_chosen:
        chosen_topic = random.choice(selected_topics)
        match chosen_topic:
            case "operations":
                if operations[0] <= entered_difficulty <= operations[1]:
                    question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case "fractions":
                if fractions[0] <= entered_difficulty <= fractions[1]:
                    question, answer, difficulty_weighting, time_needed = fractions_question_generation(entered_difficulty,
                                                                                           question_types,
                                                                                           difficulty_factors)
                    is_topic_chosen = True
            case "calculus":
                if calculus[0] <= entered_difficulty <= calculus[1]:
                    question, answer, difficulty_weighting, calculator_needed, time_needed = calculus_questions_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case "equations":
                if equations[0] <= entered_difficulty <= equations[1]:
                    question, answer, difficulty_weighting, multiple_answers, calculator_needed, time_needed = equations_question_generation(
                        entered_difficulty, question_types, difficulty_factors)
                    is_topic_chosen = True
            case "expressions":
                if expressions[0] <= entered_difficulty <= expressions[1]:
                    question, answer, difficulty_weighting, time_needed = expressions_question_generation(entered_difficulty,
                                                                                             question_types,
                                                                                             difficulty_factors)
                    is_topic_chosen = True
            case "sequences":
                if sequences[0] <= entered_difficulty <= sequences[1]:
                    question, answer, difficulty_weighting, time_needed = sequences_question_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case "hcf_lcm":
                if hcf_lcm[0] <= entered_difficulty <= hcf_lcm[1]:
                    question, answer, difficulty_weighting, time_needed = hcf_lcm_question_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case "percentages":
                if percentages[0] <= entered_difficulty <= percentages[1]:
                    question, answer, difficulty_weighting, calculator_needed, time_needed = percentages_question_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case "triangles":
                if triangles[0] <= entered_difficulty <= triangles[1]:
                    question, answer, difficulty_weighting, image_values, calculator_needed, time_needed = triangles_question_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case "graphs":
                if graphs[0] <= entered_difficulty <= graphs[1]:
                    question, answer, difficulty_weighting, graph_values, multiple_answers, calculator_needed, time_needed = graphs_questions_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case "circles":
                if circles[0] <= entered_difficulty <= circles[1]:
                    question, answer, difficulty_weighting, circle_image_values, calculator_needed, time_needed = circles_question_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True
            case _:
                if operations[0] <= entered_difficulty <= operations[1]:
                    question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty,
                                                                                            question_types,
                                                                                            difficulty_factors)
                    is_topic_chosen = True

    return chosen_topic, question, answer, difficulty_weighting, multiple_answers, image_values, graph_values, circle_image_values, calculator_needed, time_needed
