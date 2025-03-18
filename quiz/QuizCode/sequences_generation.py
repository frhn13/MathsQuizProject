import random

from .helper_functions import answer_generation, calculate_difficulty

# Linear, quadratic, geometric sequences
def sequences_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    while True:
        question_type_chosen = random.choice(question_types)
        question_topic_chosen = random.choice(["linear", "geometric", "quadratic"])

        match question_topic_chosen:
            case "linear":
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3
                nth_term = random.randint(2, 10)
                starting_term = random.randint(1, 20)
                sequence = [x * nth_term + starting_term for x in range(5)]
                answer = 5 * nth_term + starting_term
                question = f"Find the next term in this sequence: {sequence}"
                if nth_term == 10 or nth_term < 5:
                    pass
                else:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
            case "geometric":
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 5
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 5
                multiplier = random.randint(2, 5)
                starting_term = random.randint(1, 10)
                sequence = [starting_term * (multiplier**x) for x in range(0, 5)]
                answer = starting_term * (multiplier**5)
                question = f"Find the next term in this sequence: {sequence}"
                if multiplier > 3:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                if starting_term > 5:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
            case "quadratic":
                print("hey")
                difficulty_factors["maths_topic"][0] = 8
                difficulty_factors["difficulty_of_values"][0] = 7
                difficulty_factors["depth_of_knowledge"][0] = 8
                difficulty_factors["multiple_topics"][0] = 8
                difficulty_factors["difficulty_of_answer"][0] = 7
                difficulty_factors["number_of_steps"][0] = 8
                quadratic_coefficient = random.randint(1, 5)
                linear_coefficient = random.randint(-5, 5)
                number_value = random.randint(-5, 5)
                if quadratic_coefficient > 2:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                if linear_coefficient == 0:
                    difficulty_factors["difficulty_of_values"][0] -= 1
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                elif linear_coefficient < 0:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                sequence = [(quadratic_coefficient * x**2) + (linear_coefficient * x) + number_value for x in range(0, 5)]
                answer = (quadratic_coefficient * 6**2) + (linear_coefficient * 6) + number_value
                question = f"Find the next term in this sequence: {sequence}"
            case _:
                pass

        answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        if final_difficulty == entered_difficulty:
            print(question_topic_chosen)
            print(question)
            print(answer)
            print(difficulty_factors)
            print(difficulty_weighting)
            break

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

sequences_question_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)