import random
from math import sqrt, degrees, acos, sin

from .helper_functions import calculate_difficulty, answer_generation

def triangles_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    answer = 0
    question = ""
    drawing_failed = False
    while True: # Remains True until a valid question is generated with the entered difficulty
        calculator_needed = False
        question_type_chosen = random.choice(question_types) # Question type randomly chosen
        # Triangles question subtopic randomly chosen from this list
        question_topic_chosen = random.choice(["simple_area_perimeter", "simple_angles", "pythagoras", "trigonometry", "sine_cosine_area"])
        question_subtopic = ""
        time_needed = 60

        match question_topic_chosen:
            case "simple_area_perimeter":
                # Generates question where you must either find the perimeter of area of a right-angled triangle where all the side lengths are known
                difficulty_factors["maths_topic"][0] = 2
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 2
                difficulty_factors["multiple_topics"][0] = 2
                difficulty_factors["difficulty_of_answer"][0] = 2
                difficulty_factors["number_of_steps"][0] = 2
                point_a, point_b, point_c = generate_right_angled_triangle() # Function gets the coordinates for a right-angle triangle
                # Function gets all the details needed to draw the triangle on a webpage for the question
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area, drawing_failed = draw_triangle(point_a, point_b, point_c)
                if random.random() > 0.5:
                    question = "What is the perimeter of this triangle? Answer to the nearest whole number."
                    answer = perimeter
                else:
                    question = "What is the area of this triangle? Answer to the nearest whole number."
                    answer = area
            case "simple_angles":
                # Generates question where you must find a missing angle of a triangle when the other angles are known
                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 3
                difficulty_factors["difficulty_of_answer"][0] = 2
                difficulty_factors["number_of_steps"][0] = 2
                point_a, point_b, point_c = generate_triangle() # Function gets the coordinates for a triangle
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area, drawing_failed = draw_triangle(
            point_a, point_b, point_c)
                question = "What is x? Answer to the nearest whole number."
                answer = angle_c
            case "pythagoras":
                # Generates a question where you must find a missing side using Pythagoras Theorem
                calculator_needed = True
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 4
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 5
                question_subtopic = "missing_side" if random.random() > 0.5 else "missing_hypotenuse"
                point_a, point_b, point_c = generate_right_angled_triangle() # Function gets the coordinates for a right-angle triangle
                # Function gets all the details needed to draw the triangle on a webpage for the question
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area, drawing_failed = draw_triangle(
                    point_a, point_b, point_c)
                question = "What is x? Answer to the nearest whole number."
                answer = length_a if question_subtopic == "missing_side" else length_b
                if question_subtopic == "missing_side":
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
            case "trigonometry":
                # Generates a question where you must find a missing side or angle using trigonometry
                time_needed = 120
                calculator_needed = True
                difficulty_factors["maths_topic"][0] = 5
                difficulty_factors["difficulty_of_values"][0] = 4
                difficulty_factors["depth_of_knowledge"][0] = 6
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 6
                question_subtopic = random.choice(["missing_side", "missing_angle"])
                point_a, point_b, point_c = generate_right_angled_triangle() # Function gets the coordinates for a right-angle triangle
                # Function gets all the details needed to draw the triangle on a webpage for the question
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area, drawing_failed = draw_triangle(
                    point_a, point_b, point_c)
                question = "What is x? Answer to the nearest whole number."
                answer = angle_a if question_subtopic == "missing_angle" else length_c
            case "sine_cosine_area":
                # Generates a question where you must a missing side, angle or area using sine or cosine rule
                time_needed = 180
                calculator_needed = True
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 6
                difficulty_factors["depth_of_knowledge"][0] = 6
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 6
                # Type of sine or cosine rule question randomly generated from this list
                question_subtopic = random.choice(["sine_side", "sine_angle", "cosine_side", "cosine_angle", "area"])
                point_a, point_b, point_c = generate_triangle() # Function gets the coordinates for a triangle
                # Function gets all the details needed to draw the triangle on a webpage for the question
                x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area, drawing_failed = draw_triangle(
                    point_a, point_b, point_c)
                # Assigns the answer for each type of sine or cosine question
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
        answer = int(round(answer, 0))
        # Generates choices for answers for the question if the question type is multiple-choice or true/false
        answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors, True)
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

        if final_difficulty == entered_difficulty and not drawing_failed: # Breaks out of while loop if difficulty level matches entered difficulty
            break

    image_values = { # Dictionary stores all the values needed to draw the triangle for a question on the webpage
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
            # Question changed to display all four potential answers in multiple-choice question
            question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            # Question changed to display all one potential answer in true/false question
            question = f"{question}\nIs the answer {answers[0]}, answer with True or False."
            # Answer changed from number value to True or False in true/false question
            if answers[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting, image_values, calculator_needed, time_needed

def generate_triangle():
    while True: # Will create coordinates for a triangle until it produces a valid one
        point_a = (random.randint(10, 40), random.randint(10, 40))
        point_b = (random.randint(10, 40), random.randint(10, 40))
        point_c = (random.randint(10, 40), random.randint(10, 40))
        list_a = [x for x in range(point_a[0] - 5, point_a[0] + 6)], [y for y in range(point_a[1] - 5, point_a[1] + 6)]
        list_b = [x for x in range(point_b[0] - 5, point_b[0] + 6)], [y for y in range(point_b[1] - 5, point_b[1] + 6)]
        list_c = [x for x in range(point_c[0] - 5, point_c[0] + 6)], [y for y in range(point_c[1] - 5, point_c[1] + 6)]
        # Checks the coordinates are not too close and that they are not all on a straight line
        if (point_a[0] not in list_b[0] and point_a[0] not in list_c[0] and
                point_a[1] not in list_b[1] and point_a[1] not in list_c[1]
                and point_b[0] not in list_c[0] and point_b[1] not in list_c[1] and not
            (point_a[0] == point_b[0] and point_a[0] == point_c[0]) and not (point_a[1] == point_b[1] and point_a[1] == point_c[1])):
            break

    return point_a, point_b, point_c

def generate_right_angled_triangle():
    while True: # Will create coordinates for a right-angle triangle until it produces a valid one
        x1 = random.randint(10, 40)
        y2 = random.randint(10, 40)
        point_a = (x1, random.randint(10, 40))
        point_b = (x1, y2)
        point_c = (random.randint(1, 40), y2)
        list_a = [x for x in range(point_a[0] - 5, point_a[0] + 6)], [y for y in range(point_a[1] - 5, point_a[1] + 6)]
        list_b = [x for x in range(point_b[0] - 5, point_b[0] + 6)], [y for y in range(point_b[1] - 5, point_b[1] + 6)]
        list_c = [x for x in range(point_c[0] - 5, point_c[0] + 6)], [y for y in range(point_c[1] - 5, point_c[1] + 6)]
        # Checks the coordinates are not too close and that they are not all on a straight line
        if point_a[0] not in list_c[0] and \
                point_a[1] not in list_b[1] and not \
                (point_a[0] == point_b[0] and point_a[0] == point_c[0]) and not (
                point_a[1] == point_b[1] and point_a[1] == point_c[1]):
            break

    return point_a, point_b, point_c

def draw_triangle(point_a, point_b, point_c):
    # Function gets the side lengths and angles of a triangle using its passed in coordinates
    drawing_failed = False
    x_coordinates = [point_a[0], point_b[0], point_c[0], point_a[0]]
    y_coordinates = [point_a[1], point_b[1], point_c[1], point_a[1]]

    # Generates the side lengths
    length_c = sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)
    length_b = sqrt((point_a[0] - point_c[0]) ** 2 + (point_a[1] - point_c[1]) ** 2)
    length_a = sqrt((point_b[0] - point_c[0]) ** 2 + (point_b[1] - point_c[1]) ** 2)

    # Will try generate the angles, but will return if this failed
    try:
        angle_a = acos((length_b ** 2 + length_c ** 2 - length_a ** 2) / (2 * length_b * length_c))
        angle_b = acos((length_a ** 2 + length_c ** 2 - length_b ** 2) / (2 * length_a * length_c))
        angle_c = acos((length_a ** 2 + length_b ** 2 - length_c ** 2) / (2 * length_a * length_b))
    except Exception:
        angle_a = 0
        angle_b = 0
        angle_c = 0
        drawing_failed = True

    # Generates the perimeter and area of the triangle
    perimeter = length_c + length_b + length_a
    area = 0.5 * length_a * length_b * sin(angle_c)

    # Converts the angles from radians to degrees
    angle_a = degrees(angle_a)
    angle_b = degrees(angle_b)
    angle_c = degrees(angle_c)

    return x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area, drawing_failed

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
