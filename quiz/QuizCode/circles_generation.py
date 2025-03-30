import random
import math

from helper_functions import answer_generation, answer_generation_decimals, calculate_difficulty

def circles_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    while True:
        question_topic_chosen = random.choice(["area", "circumference", "sector", "arc", "area_of_shaded_area"])
        print(question_topic_chosen)
        question_type_chosen = random.choice(question_types)
        question = ""
        answer, radius, angle = 0, 0, 0
        match question_topic_chosen:
            case "area":
                radius = random.randint(2, 10)
                answer = round(math.pi * math.pow(radius, 2), 2)
                question = f"If the radius of a circle is {radius}, then what is its area? Give your answer correct to 2 decimal places." if random.random() > 0.5 \
                    else f"If the diameter of a circle is {radius*2}, then what is its area? Give your answer correct to 2 decimal places."

            case "circumference":
                radius = random.randint(2, 10)
                answer = round(math.pi * radius * 2, 2)
                question = f"If the radius of a circle is {radius}, then what is its circumference? Give your answer correct to 2 decimal places." if random.random() > 0.5 \
                    else f"If the diameter of a circle is {radius * 2}, then what is its circumference? Give your answer correct to 2 decimal places."

            case "sector":
                radius = random.randint(2, 10)
                angle = random.randint(60, 170)
                answer = round((angle/360) * math.pi * math.pow(radius, 2), 2)
                question = (f"If the radius of a circle is {radius}, and the circle has a sector with the angle {angle}°, "
                            f"then what is the area of the sector? Give your answer correct to 2 decimal places.") if random.random() > 0.5 \
                    else (f"If the diameter of a circle is {radius*2}, and the circle has a sector with the angle {angle}°, "
                            f"then what is the area of the sector? Give your answer correct to 2 decimal places.")

            case "arc":
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
                radius = random.randint(2, 10)
                angle = random.randint(60, 170)
                sector_area = (angle/360) * math.pi * math.pow(radius, 2)
                triangle_area = 0.5 * math.pow(radius, 2) * math.sin(angle)
                answer = round(sector_area - triangle_area, 2)
                question = (f"If the radius of a circle is {radius}, and the circle has a sector with the angle {angle}° "
                            f"then find the area of the shaded area")

        circle_image_values = {
            "radius": radius,
            "angle": angle,
            "question_topic": question_topic_chosen
        }

        if type(answer) == int:
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
        elif type(answer) == float:
            answers, difficulty_factors = answer_generation_decimals(answer, question_type_chosen, difficulty_factors)
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        if final_difficulty == entered_difficulty or 1==1:
            print(difficulty_factors)
            print(difficulty_weighting)
            print(question)
            print(answer)
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

    return question, answer, difficulty_weighting, circle_image_values

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

circles_question_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)
