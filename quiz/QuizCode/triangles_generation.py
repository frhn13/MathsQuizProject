import random
from numpy import sqrt, degrees, rad2deg
from numpy.ma.core import arccos, sin, masked

from .helper_functions import calculate_difficulty, answer_generation

# Angles in triangle, area and perimeter, pythagoras, SOHCAHTOA (trig), sine and cosine rule
def triangles_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    answer = 0
    question = ""
    while True:
        question_type_chosen = random.choice(question_types)
        question_topic_chosen = random.choice(["simple_area_perimeter", "simple_angles", "pythagoras", "trigonometry", "sine_cosine_area"])
        question_subtopic = ""

        match question_topic_chosen:
            case "simple_area_perimeter":
                difficulty_factors["maths_topic"][0] = 2
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 2
                difficulty_factors["multiple_topics"][0] = 2
                difficulty_factors["difficulty_of_answer"][0] = 2
                difficulty_factors["number_of_steps"][0] = 2
                point_a, point_b, point_c = generate_right_angled_triangle()
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(point_a, point_b, point_c)
                if random.random() > 0.5:
                    question = "What is the perimeter of this triangle? Answer to the nearest whole number."
                    answer = perimeter
                else:
                    question = "What is the area of this triangle? Answer to the nearest whole number."
                    answer = area
            case "simple_angles":
                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 2
                difficulty_factors["number_of_steps"][0] = 2
                point_a, point_b, point_c = generate_triangle()
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
            point_a, point_b, point_c)
                question = "What is x? Answer to the nearest whole number."
                answer = angle_c
            case "pythagoras":
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 5
                question_subtopic = "missing_side" if random.random() > 0.5 else "missing_hypotenuse"
                point_a, point_b, point_c = generate_right_angled_triangle()
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
                    point_a, point_b, point_c)
                question = "What is x? Answer to the nearest whole number."
                answer = length_a if question_subtopic == "missing_side" else length_b
                if question_subtopic == "missing_side":
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
            case "trigonometry":
                difficulty_factors["maths_topic"][0] = 5
                difficulty_factors["difficulty_of_values"][0] = 4
                difficulty_factors["depth_of_knowledge"][0] = 6
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 6
                question_subtopic = random.choice(["missing_side", "missing_angle"])
                point_a, point_b, point_c = generate_right_angled_triangle()
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
                    point_a, point_b, point_c)
                question = "What is x? Answer to the nearest whole number."
                answer = angle_a if question_subtopic == "missing_angle" else length_c
            case "sine_cosine_area":
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 6
                difficulty_factors["depth_of_knowledge"][0] = 6
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 6
                question_subtopic = random.choice(["sine_side", "sine_angle", "cosine_side", "cosine_angle", "area"])
                point_a, point_b, point_c = generate_triangle()
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
                    point_a, point_b, point_c)
                match question_subtopic:
                    case "sine_side":
                        answer = length_c
                    case "sine_angle":
                        answer = angle_c
                    case "cosine_side":
                        answer = length_a
                        difficulty_factors["difficulty_of_values"][0] += 1
                        difficulty_factors["difficulty_of_answer"][0] += 1
                        difficulty_factors["depth_of_knowledge"][0] += 1
                        difficulty_factors["number_of_steps"][0] += 1
                    case "cosine_angle":
                        answer = angle_a
                        difficulty_factors["difficulty_of_values"][0] += 1
                        difficulty_factors["difficulty_of_answer"][0] += 1
                        difficulty_factors["depth_of_knowledge"][0] += 1
                        difficulty_factors["number_of_steps"][0] += 1
                    case "area":
                        answer = area
                question = "What is the area of this triangle? Answer to the nearest whole number." if question_subtopic == "area" else "What is x? Answer to the nearest whole number."
            case _:
                pass
        if answer is not masked:
            answer = int(round(answer, 0))
        else:
            answer = 0
        answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        if final_difficulty == entered_difficulty:
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    image_values = {
        "point_a": point_a,
        "point_b": point_b,
        "point_c": point_c,
        "length_a": length_a,
        "length_b": length_b,
        "length_c": length_c,
        "angle_a": angle_a,
        "angle_b": angle_b,
        "angle_c": angle_c,
        "question_topic": question_topic_chosen,
        "question_subtopic": question_subtopic
    }

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

    return question, answer, difficulty_weighting, image_values

def generate_triangle():
    while True:
        point_a = (random.randint(10, 40), random.randint(10, 40))
        point_b = (random.randint(10, 40), random.randint(10, 40))
        point_c = (random.randint(10, 40), random.randint(10, 40))
        if point_a != point_b and point_a != point_c and point_b != point_c and not \
            (point_a[0] == point_b[0] and point_a[0] == point_c[0]) and not (point_a[1] == point_b[1] and point_a[1] == point_c[1]):
            break

    return point_a, point_b, point_c

def generate_right_angled_triangle():
    while True:
        x1 = random.randint(10, 40)
        y2 = random.randint(10, 40)
        point_a = (x1, random.randint(10, 40))
        point_b = (x1, y2)
        point_c = (random.randint(1, 40), y2)
        if point_a != point_b and point_a != point_c and point_b != point_c and not \
                (point_a[0] == point_b[0] and point_a[0] == point_c[0]) and not (
                point_a[1] == point_b[1] and point_a[1] == point_c[1]):
            break

    return point_a, point_b, point_c

def draw_triangle(point_a, point_b, point_c):
    x_coordinates = [point_a[0], point_b[0], point_c[0], point_a[0]]
    y_coordinates = [point_a[1], point_b[1], point_c[1], point_a[1]]

    length_c = sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)
    length_b = sqrt((point_a[0] - point_c[0]) ** 2 + (point_a[1] - point_c[1]) ** 2)
    length_a = sqrt((point_b[0] - point_c[0]) ** 2 + (point_b[1] - point_c[1]) ** 2)

    angle_a = arccos((length_b ** 2 + length_c ** 2 - length_a ** 2) / (2 * length_b * length_c))
    angle_b = arccos((length_a ** 2 + length_c ** 2 - length_b ** 2) / (2 * length_a * length_c))
    angle_c = arccos((length_a ** 2 + length_b ** 2 - length_c ** 2) / (2 * length_a * length_b))

    perimeter = length_c + length_b + length_a
    area = 0.5 * length_a * length_b * sin(angle_c)

    angle_a = degrees(angle_a)
    angle_b = degrees(angle_b)
    angle_c = degrees(angle_c)

    return x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area

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

# question, answer, difficulty_weighting, img = triangles_question_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)
