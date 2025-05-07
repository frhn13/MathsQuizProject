import random

from .helper_functions import answer_generation, calculate_difficulty

def sequences_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    while True: # Remains True until a valid question is generated with the entered difficulty
        time_needed = 60
        question_type_chosen = random.choice(question_types) # Question type randomly chosen
        # Sequences question subtopic randomly chosen from this list
        question_topic_chosen = random.choice(["linear", "geometric", "quadratic"])

        match question_topic_chosen:
            case "linear":
                # Generates question asking for next element in linear sequence
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3
                nth_term = random.randint(2, 10)
                starting_term = random.randint(1, 20)
                # Generates linear sequence for first 5 elements
                sequence = [x * nth_term + starting_term for x in range(5)]
                answer = 5 * nth_term + starting_term
                question = f"Find the next term in this linear sequence: {sequence}"
                # Question becomes harder if values in nth term are more complex
                if nth_term == 10 or nth_term < 5:
                    pass
                else:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
            case "geometric":
                # Generates question asking for next element in geometric sequence
                time_needed = 120
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 5
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 5
                multiplier = random.randint(2, 5)
                starting_term = random.randint(1, 10)
                # Generates geometric sequence for first 5 elements
                sequence = [starting_term * (multiplier**x) for x in range(0, 5)]
                answer = starting_term * (multiplier**5)
                question = f"Find the next term in this geometric sequence: {sequence}"
                # Question becomes harder if values in nth term are more complex
                if multiplier > 3:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                if starting_term > 5:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
            case "quadratic":
                # Generates question asking for next element in quadratic sequence
                time_needed = 180
                difficulty_factors["maths_topic"][0] = 8
                difficulty_factors["difficulty_of_values"][0] = 7
                difficulty_factors["depth_of_knowledge"][0] = 8
                difficulty_factors["multiple_topics"][0] = 8
                difficulty_factors["difficulty_of_answer"][0] = 7
                difficulty_factors["number_of_steps"][0] = 8
                quadratic_coefficient = random.randint(1, 5)
                linear_coefficient = random.randint(-5, 5)
                number_value = random.randint(-5, 5)
                # Question becomes harder if values in nth term are more complex
                if quadratic_coefficient > 2:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                if linear_coefficient == 0:
                    difficulty_factors["difficulty_of_values"][0] -= 1
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                elif linear_coefficient < 0:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                # Generates quadratic sequence for first 5 elements
                sequence = [(quadratic_coefficient * x**2) + (linear_coefficient * x) + number_value for x in range(0, 5)]
                answer = (quadratic_coefficient * 5**2) + (linear_coefficient * 5) + number_value
                question = f"Find the next term in this quadratic sequence: {sequence}"
            case _:
                pass

        # Generates choices for answers for the question if the question type is multiple-choice or true/false
        answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors, False)
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
