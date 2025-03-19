from io import BytesIO
import matplotlib.pyplot as plt
import random
from numpy import sqrt, degrees, rad2deg
from numpy.ma.core import arccos, sin

from helper_functions import calculate_difficulty, answer_generation

# Angles in triangle, area and perimeter, pythagoras, SOHCAHTOA (trig), sine and cosine rule
def triangles_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    answer = 0
    question = ""
    while True:
        question_type_chosen = random.choice(question_types)
        question_topic_chosen = random.choice(["simple_area_perimeter", "simple_angles", "pythagoras", "trigonometry", "sine_cosine_area"])

        match question_topic_chosen:
            case "simple_area_perimeter":
                point_a, point_b, point_c = generate_right_angled_triangle()
                triangle_img, x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(point_a, point_b, point_c, question_topic_chosen, "")
                if random.random() > 0.5:
                    question = "What is the perimeter of this triangle? Answer to the nearest whole number."
                    answer = length_a + length_b + length_c
                else:
                    question = "What is the area of this triangle? Answer to the nearest whole number."
                    answer = 0.5 * length_a * length_c
            case "simple_angles":
                point_a, point_b, point_c = generate_triangle()
                triangle_img, x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
            point_a, point_b, point_c, question_topic_chosen, "")
                question = "What is x? Answer to the nearest whole number."
                answer = angle_c
            case "pythagoras":
                question_subtopic = "missing_side" if random.random() > 0.5 else "missing_hypotenuse"
                point_a, point_b, point_c = generate_right_angled_triangle()
                triangle_img, x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
                    point_a, point_b, point_c, question_topic_chosen, question_subtopic)
                question = "What is x? Answer to the nearest whole number."
                answer = length_a if question_subtopic == "missing_side" else length_b
            case "trigonometry":
                question_subtopic = random.choice(["missing_side", "missing_angle"])
                point_a, point_b, point_c = generate_right_angled_triangle()
                triangle_img, x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
                    point_a, point_b, point_c, question_topic_chosen, question_subtopic)
                question = "What is x? Answer to the nearest whole number."
                answer = angle_a if question_subtopic == "missing_angle" else length_c
            case "sine_cosine_area":
                question_subtopic = random.choice(["sine_side", "sine_angle", "cosine_side", "cosine_angle", "area"])
                point_a, point_b, point_c = generate_triangle()
                triangle_img, x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area = draw_triangle(
                    point_a, point_b, point_c, question_topic_chosen, question_subtopic)
                match question_subtopic:
                    case "sine_side":
                        answer = length_c
                    case "sine_angle":
                        answer = angle_c
                    case "cosine_side":
                        answer = length_a
                    case "cosine_angle":
                        answer = angle_a
                    case "area":
                        answer = area
                question = "What is the area of this triangle? Answer to the nearest whole number." if question_subtopic == "area" else "What is x? Answer to the nearest whole number."
            case _:
                pass
        answer = int(answer)
        answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        if final_difficulty == entered_difficulty or 1==1:
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    match question_type_chosen:
        case "free_text":
            question = f"What is {question}?"
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

def generate_triangle():
    while True:
        point_a = (random.randint(1, 10), random.randint(1, 10))
        point_b = (random.randint(1, 10), random.randint(1, 10))
        point_c = (random.randint(1, 10), random.randint(1, 10))
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

def draw_triangle(point_a, point_b, point_c, question_topic, question_subtopic):
    x_coordinates = [point_a[0], point_b[0], point_c[0], point_a[0]]
    y_coordinates = [point_a[1], point_b[1], point_c[1], point_a[1]]

    length_c = sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)
    length_b = sqrt((point_a[0] - point_c[0]) ** 2 + (point_a[1] - point_c[1]) ** 2)
    length_a = sqrt((point_b[0] - point_c[0]) ** 2 + (point_b[1] - point_c[1]) ** 2)

    angle_a = arccos((length_b ** 2 + length_c ** 2 - length_a ** 2) / (2 * length_b * length_c))
    angle_b = arccos((length_a ** 2 + length_c ** 2 - length_b ** 2) / (2 * length_a * length_c))
    angle_c = arccos((length_a ** 2 + length_b ** 2 - length_c ** 2) / (2 * length_a * length_b))
    angle_a = degrees(angle_a)
    angle_b = degrees(angle_b)
    angle_c = degrees(angle_c)

    perimeter = length_c + length_b + length_a
    area = 0.5 * length_a * length_b * sin(angle_c)

    if question_topic == "pythagoras":
        if question_subtopic == "missing_side":
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, "x")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")
        else:
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, f"Side a = {length_a:.2f}cm")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, "x")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")
    elif question_topic == "trigonometry":
        if question_subtopic == "missing_side":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, "x")
        else:
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")
    elif question_topic == "sine_cosine_area":
        if question_subtopic == "sine_side":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, "x")
        elif question_subtopic == "sine_angle":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")
        elif question_subtopic == "cosine_side":
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, "x")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")
        elif question_subtopic == "cosine_angle":
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, f"Side a = {length_a:.2f}cm")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")
        elif question_subtopic == "area":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")

    else:
        plt.text((point_b[0] + point_c[0])/2, (point_b[1] + point_c[1])/2, f"Side a = {length_a:.2f}cm")
        plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm")
        plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm")

    if question_topic == "simple_angles":
        plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°")
        plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°")
        plt.text(point_c[0], point_c[1], "x")
    elif question_topic == "trigonometry":
        if question_subtopic == "missing_side":
            plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°")
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°")
        else:
            plt.text(point_a[0], point_a[1], "x")
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°")
    elif question_topic == "sine_cosine_area":
        if question_subtopic == "sine_side":
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°")
            plt.text(point_c[0], point_c[1], f"Angle C = {angle_c:.2f}°")
        elif question_subtopic == "sine_angle":
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°")
            plt.text(point_c[0], point_c[1], "x")
        elif question_subtopic == "cosine_side":
            plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°")
        elif question_subtopic == "cosine_angle":
            plt.text(point_a[0], point_a[1], "x")
        elif question_subtopic == "area":
            plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°")
    else:
        plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°")
        plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°")
        plt.text(point_c[0], point_c[1], f"Angle C = {angle_c:.2f}°")

    plt.gca().set_aspect("equal", adjustable="box")

    print(question_topic)
    print(f"{angle_a}, {angle_b}, {angle_c}")

    plt.plot(x_coordinates, y_coordinates, color="blue", linestyle="-", marker=".")

    triangle_img = BytesIO()
    plt.savefig(triangle_img, format="png")
    triangle_img.seek(0)
    plt.show()
    return triangle_img, x_coordinates, y_coordinates, length_a, length_b, length_c, angle_a, angle_b, angle_c, perimeter, area

#a, b, c = generate_triangle()
#draw_triangle(a, b, c, "sine_cosine_area", "area")

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

question, answer, difficulty_weighting = triangles_question_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)

print(question)
print(answer)