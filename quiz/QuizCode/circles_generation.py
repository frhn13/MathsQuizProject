import random
import math

from .helper_functions import answer_generation, answer_generation_decimals, calculate_difficulty

def circles_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    while True: # Remains True until a valid question is generated with the entered difficulty
        time_needed = 60
        calculator_needed = True # Calculator always needed for circle questions
        # Circles question subtopic randomly chosen from this list
        question_topic_chosen = random.choice(["area", "circumference", "sector", "arc", "area_of_shaded_area"])
        question_type_chosen = random.choice(question_types)
        question = ""
        answer, radius, angle = 0, 0, 0
        match question_topic_chosen:
            case "area":
                # Generates question to find area of circle, using either radius or diameter
                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3
                radius = random.randint(2, 10)
                answer = round(math.pi * math.pow(radius, 2), 2)
                question = f"If the radius of a circle is {radius}, then what is its area? Give your answer correct to 2 decimal places." if random.random() > 0.5 \
                    else f"If the diameter of a circle is {radius*2}, then what is its area? Give your answer correct to 2 decimal places."

            case "circumference":
                # Generates question to find circumference of circle, using either radius or diameter
                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3
                radius = random.randint(2, 10)
                answer = round(math.pi * radius * 2, 2)
                question = f"If the radius of a circle is {radius}, then what is its circumference? Give your answer correct to 2 decimal places." if random.random() > 0.5 \
                    else f"If the diameter of a circle is {radius * 2}, then what is its circumference? Give your answer correct to 2 decimal places."

            case "sector":
                # Generates question to find area of circle's sector, using either radius or diameter
                difficulty_factors["maths_topic"][0] = 5
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 6
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 5
                radius = random.randint(2, 10)
                angle = random.randint(60, 170)
                answer = round((angle/360) * math.pi * math.pow(radius, 2), 2)
                question = (f"If the radius of a circle is {radius}, and the circle has a sector with the angle {angle}°, "
                            f"then what is the area of the sector? Give your answer correct to 2 decimal places.") if random.random() > 0.5 \
                    else (f"If the diameter of a circle is {radius*2}, and the circle has a sector with the angle {angle}°, "
                            f"then what is the area of the sector? Give your answer correct to 2 decimal places.")

            case "arc":
                # Generates question to find length of a sector's arc, using either radius or diameter
                difficulty_factors["maths_topic"][0] = 5
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 6
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 5
                radius = random.randint(2, 10)
                angle = random.randint(60, 170)
                answer = round((angle/360) * math.pi * radius * 2, 2)
                question = (
                    f"If the radius of a circle is {radius}, and the circle has a sector with the angle {angle}°, "
                    f"then what is the length of the sector's arc? Give your answer correct to 2 decimal places.") if random.random() > 0.5 \
                    else (
                    f"If the diameter of a circle is {radius * 2}, and the circle has a sector with the angle {angle}°, "
                    f"then what is the length of the sector's arc? Give your answer correct to 2 decimal places.")

            case "area_of_shaded_area":
                # Generates question to find area between arc and chord of circle, using either radius or diameter
                time_needed = 120
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 6
                difficulty_factors["depth_of_knowledge"][0] = 7
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 6
                difficulty_factors["number_of_steps"][0] = 7
                radius = random.randint(2, 10)
                angle = random.randint(60, 170)
                sector_area = (angle/360) * math.pi * math.pow(radius, 2)
                triangle_area = 0.5 * math.pow(radius, 2) * math.sin(angle)
                answer = round(sector_area - triangle_area, 2)
                question = (f"If the radius of a circle is {radius}, and the circle has a sector with the angle {angle}° "
                            f"then find the area of the semicircle formed by the chord.") if random.random() > 0.5 \
                    else (f"If the diameter of a circle is {radius * 2}, and the circle has a sector with the angle {angle}° "
                     f"then find the area of the semicircle formed by the chord.")

        # Dictionary contains values that are used to draw the circle on the webpage for a question
        circle_image_values = {
            "radius": radius,
            "angle": angle,
            "question_topic": question_topic_chosen,
            "use_diameter": True if "diameter" in question else False
        }

        if "diameter" in question:
            difficulty_factors["number_of_steps"][0] += 1
            difficulty_factors["difficulty_of_values"][0] += 1

        # Generates choices for answers for the question if the question type is multiple-choice or true/false
        if type(answer) == int:
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors, True)
        elif type(answer) == float:
            answers, difficulty_factors = answer_generation_decimals(answer, question_type_chosen, difficulty_factors, True)
        # Finds the final difficulty of a question using all of its factors
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        if final_difficulty == entered_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    match question_type_chosen:
        case "free_text":
            question = question
        # Question changed to display all four potential answers in multiple-choice question
        case "multiple-choice":
            if type(answers[0]) == int:
                question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
            elif type(answers[0]) == float:
                question = f"{question}\nIs it {answers[0]:.2f}, {answers[1]:.2f}, {answers[2]:.2f} or {answers[3]:.2f}?"
        case "true/false":
            # Question changed to display all one potential answer in true/false question
            if (answers[0]) == int:
                question = f"{question}\nIs the answer {answers[0]}, answer with True or False."
            elif (answers[0]) == float:
                question = f"{question}\nIs the answer {answers[0]:.2f}, answer with True or False."
            # Answer changed from number value to True or False in true/false question
            if answers[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting, circle_image_values, calculator_needed, time_needed

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

#circles_question_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)
