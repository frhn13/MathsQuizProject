import random
from math import gcd, lcm
from sympy import factorint

from .helper_functions import answer_generation, calculate_difficulty

def hcf_lcm_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question = ""
    answer = 0
    while True: # Remains True until a valid question is generated with the entered difficulty
        time_needed = 120
        # Question subtopic randomly chosen from this list
        question_topic_chosen = random.choice(["hcf", "lcm", "prime_factors"])
        question_type_chosen = random.choice(question_types) # Question type randomly chosen
        match question_topic_chosen:
            case "hcf":
                # Makes question where you have to find the HCF of two numbers
                difficulty_factors["maths_topic"][0] = 2
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3
                # Values for the two numbers are randomly generated
                num1, num2 = random.randint(10, 200), random.randint(10, 200)
                answer = gcd(num1, num2)
                answer = int(answer)
                question = f"What is the highest common factor of {num1} and {num2}?"
                # Question becomes easier if HCF equals one of the numbers
                if answer == num1 or answer == num2:
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                    difficulty_factors["difficulty_of_values"][0] -= 1
            case "lcm":
                # Makes question where you have to find the LCM of two numbers
                difficulty_factors["maths_topic"][0] = 2
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 2
                difficulty_factors["number_of_steps"][0] = 2
                while True:
                    # Values for the two numbers are randomly generated
                    num1, num2 = random.randint(10, 100), random.randint(10, 100)
                    answer = lcm(num1, num2)
                    answer = int(answer)
                    question = f"What is the lowest common multiple of {num1} and {num2}?"
                    # LCM must be lower than 1000 otherwise question is too hard
                    if answer <= 1000:
                        break
                # Question becomes easier if LCM equals one of the numbers
                if answer == num1 or answer == num2:
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                    difficulty_factors["difficulty_of_values"][0] -= 1
            case "prime_factors":
                # Makes question to find all prime factors of a number
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 4
                num1 = random.randint(50, 200)
                answer = factorint(num1)
                question = f"How could {num1} be written as a product of its prime factors? Don't use any exponents in your answer."
                # Question becomes easier if there is only 1 prime factor
                if len(answer) == 1:
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                    difficulty_factors["difficulty_of_values"][0] -= 1


        if type(answer) == int:
            # Generates choices for answers for the question if the question type is multiple-choice or true/false
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors, True)
        else:
            # Prime factor questions are always free-text ones
            question_type_chosen = "free_text"
            difficulty_factors["question_type"][0] = 7
            difficulty_factors["answers_similarity"][0] = 7
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

        if final_difficulty == entered_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
            break

    match question_type_chosen:
        case "free_text":
            question = question
        case "multiple-choice":
            # Question changed to display all four potential answers in multiple-choice question
            question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            # Question changed to display all one potential answer in true/false question
            question = f"{question}\nIs the answer {answers[0]}, answer with True or False."
            if answers[0] == answer:
                # Answer changed from number value to True or False in true/false question
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting, time_needed
