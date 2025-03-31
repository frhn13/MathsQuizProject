import random
from math import gcd, lcm
from sympy import factorint

from .helper_functions import answer_generation, calculate_difficulty

def hcf_lcm_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question = ""
    answer = 0
    while True:
        question_topic_chosen = random.choice(["hcf", "lcm", "prime_factors"])
        question_type_chosen = random.choice(question_types)
        match question_topic_chosen:
            case "hcf":
                difficulty_factors["maths_topic"][0] = 2
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3
                num1, num2 = random.randint(10, 200), random.randint(10, 200)
                answer = gcd(num1, num2)
                question = f"What is the highest common factor of {num1} and {num2}?"
                if answer == num1 or answer == num2:
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                    difficulty_factors["difficulty_of_values"][0] -= 1
            case "lcm":
                difficulty_factors["maths_topic"][0] = 2
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 2
                difficulty_factors["number_of_steps"][0] = 2
                while True:
                    num1, num2 = random.randint(10, 100), random.randint(10, 100)
                    answer = lcm(num1, num2)
                    question = f"What is the lowest common multiple of {num1} and {num2}?"
                    if answer <= 1000:
                        break
                if answer == num1 or answer == num2:
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                    difficulty_factors["difficulty_of_values"][0] -= 1
            case "prime_factors":
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 4
                num1 = random.randint(50, 200)
                answer = factorint(num1)
                question = f"What are the prime factors of {num1}?"

                if len(answer) == 1:
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                    difficulty_factors["difficulty_of_values"][0] -= 1

        if type(answer) == int:
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
        else:
            question_type_chosen = "free_text"
            difficulty_factors["question_type"][0] = 7
            difficulty_factors["answers_similarity"][0] = 7
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
        print(final_difficulty)

        if final_difficulty == entered_difficulty:
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    match question_type_chosen:
        case "free_text":
            question = question
        case "multiple-choice":
            question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            question = f"{question}\nIs the answer {answers[0]}, answer with True or False."
            if answers[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting

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

#hcf_lcm_question_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)