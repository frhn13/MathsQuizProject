import random
from sympy import diff, integrate, symbols, limit, solveset, solve, zoo

from .helper_functions import calculate_difficulty, answer_generation

def calculus_questions_generation(entered_difficulty : int, question_types : list, difficulty_factors: dict):
    while True:
        question_type_chosen = random.choice(question_types)
        question_topic_chosen = random.choice(["differentiation", "integration"])
        calculator_needed = False
        x = symbols("x")
        match question_topic_chosen:
            case "differentiation":
                question_subtopic_chosen = random.choice(["basic_differentiation", "second_order_differentiation", "answer_from_derivative", "finding_x", "tangents", "normals"])
                question, answer, difficulty_factors, is_valid = differentiation_questions(question_subtopic_chosen, difficulty_factors)
                if is_valid:
                    # difficulty_factors["question_type"][0] = 10
                    # difficulty_factors["answers_similarity"][0] = 9
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                    if entered_difficulty == final_difficulty:
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break
                else:
                    pass
            case "integration":
                question_subtopic_chosen = random.choice(
                    ["basic_integration", "definite_integrals", "finding_area", "finding_complex_area"])
                question, answer, difficulty_factors, is_valid = integration_questions(question_subtopic_chosen, difficulty_factors)
                if is_valid:
                    if question_subtopic_chosen in ("definite_integrals", "finding_area", "finding_complex_area"):
                        calculator_needed = True
                    difficulty_factors["question_type"][0] = 10
                    difficulty_factors["answers_similarity"][0] = 9
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                    if entered_difficulty == final_difficulty:
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break
    answer = str(answer)
    return question, answer, difficulty_weighting, calculator_needed


def differentiation_questions(question_subtopic_chosen : str, difficulty_factors : dict):
    question, answer = "", ""
    x = symbols("x")
    cubic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    quadratic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    linear_value = random.randint(1, 10) * random.choice([0, 1, -1])
    number_value = random.randint(1, 10) * random.choice([0, 1, -1])

    if cubic_value == 0 and quadratic_value == 0 and linear_value == 0:
        return question, answer, difficulty_factors, False
    f = cubic_value * x ** 3 + quadratic_value * x ** 2 + linear_value * x + number_value

    difficulty_factors["difficulty_of_values"][0] = 7
    difficulty_factors["difficulty_of_answer"][0] = 7
    difficulty_factors["number_of_steps"][0] = 7

    if cubic_value == 0:
        difficulty_factors["difficulty_of_values"][0] += 0.5
        difficulty_factors["number_of_steps"][0] += 0.5
        difficulty_factors["difficulty_of_answer"][0] += 0.5
    if quadratic_value == 0:
        difficulty_factors["difficulty_of_values"][0] += 0.5
        difficulty_factors["number_of_steps"][0] += 0.5
        difficulty_factors["difficulty_of_answer"][0] += 0.5
    if linear_value == 0:
        difficulty_factors["difficulty_of_values"][0] += 0.5
        difficulty_factors["number_of_steps"][0] += 0.5
        difficulty_factors["difficulty_of_answer"][0] += 0.5

    match question_subtopic_chosen:
        case "basic_differentiation":
            difficulty_factors["maths_topic"][0] = 8
            difficulty_factors["depth_of_knowledge"][0] = 7
            difficulty_factors["multiple_topics"][0] = 7
            difficulty_factors["question_type"][0] = 7
            difficulty_factors["answers_similarity"][0] = 8
            df = diff(f, x)
            f_str = simplify_f(f)
            answer = df
            question = f"What is the first order derivative of {f_str}?"
            if "x" not in str(answer):
                return "", "", difficulty_factors, False

        case "second_order_differentiation":
            difficulty_factors["difficulty_of_values"][0] += 1
            difficulty_factors["difficulty_of_answer"][0] += 1
            difficulty_factors["number_of_steps"][0] += 1
            difficulty_factors["maths_topic"][0] = 8
            difficulty_factors["depth_of_knowledge"][0] = 7
            difficulty_factors["multiple_topics"][0] = 7
            difficulty_factors["question_type"][0] = 7
            difficulty_factors["answers_similarity"][0] = 8
            d2f = diff(f, x, 2)
            f_str = simplify_f(f)
            answer = d2f
            question = f"What is the second order derivative of {f_str}?"
            if "x" not in str(answer):
                return "", "", difficulty_factors, False

        case "answer_from_derivative":
            difficulty_factors["difficulty_of_values"][0] += 1.5
            difficulty_factors["difficulty_of_answer"][0] += 1.5
            difficulty_factors["number_of_steps"][0] += 1.5
            difficulty_factors["maths_topic"][0] = 8
            difficulty_factors["depth_of_knowledge"][0] = 8
            difficulty_factors["multiple_topics"][0] = 8
            difficulty_factors["question_type"][0] = 10
            difficulty_factors["answers_similarity"][0] = 9
            df = diff(f, x)
            f_str = simplify_f(f)
            x_value = random.randint(1, 5)
            question = f"What is the answer to f\'({x_value}) when f(x) = {f_str}?"
            answer = df.subs(x, x_value)

        case "finding_x":
            if cubic_value != 0:
                difficulty_factors["difficulty_of_values"][0] += 2
                difficulty_factors["difficulty_of_answer"][0] += 2
                difficulty_factors["number_of_steps"][0] += 2
            else:
                difficulty_factors["difficulty_of_values"][0] += 1.5
                difficulty_factors["difficulty_of_answer"][0] += 1.5
                difficulty_factors["number_of_steps"][0] += 1.5
            difficulty_factors["maths_topic"][0] = 8
            difficulty_factors["depth_of_knowledge"][0] = 8
            difficulty_factors["multiple_topics"][0] = 8
            difficulty_factors["question_type"][0] = 10
            difficulty_factors["answers_similarity"][0] = 9
            df = diff(f, x)
            f_str = simplify_f(f)
            question = f"What is the value of x when f\'(x) = 0 and f(x) = {f_str}?"
            answer = solve(df, x)

        case "tangents":
            difficulty_factors["difficulty_of_values"][0] += 2
            difficulty_factors["difficulty_of_answer"][0] += 2
            difficulty_factors["number_of_steps"][0] += 2
            difficulty_factors["maths_topic"][0] = 10
            difficulty_factors["depth_of_knowledge"][0] = 10
            difficulty_factors["multiple_topics"][0] = 10
            difficulty_factors["question_type"][0] = 10
            difficulty_factors["answers_similarity"][0] = 9
            df = diff(f, x)
            x_value = random.randint(1, 5)
            y_value = f.subs(x, x_value)
            gradient = df.subs(x, x_value)
            y_intercept = y_value - (x_value * gradient)
            f_str = simplify_f(f)
            question = f"What is the equation of the tangent to the curve with the equation y={f_str} at the point ({x_value}, {y_value}). Give your answer in the form y=mx+c"
            if y_intercept == zoo or y_intercept == 0:
                answer = f"y={gradient}x"
            elif y_intercept > 0:
                answer = f"y={gradient}x+{y_intercept}"
            else:
                answer = f"y={gradient}x{y_intercept}"

        case "normals":
            difficulty_factors["difficulty_of_values"][0] += 2.5
            difficulty_factors["difficulty_of_answer"][0] += 2.5
            difficulty_factors["number_of_steps"][0] += 2.5
            difficulty_factors["maths_topic"][0] = 11
            difficulty_factors["depth_of_knowledge"][0] = 11
            difficulty_factors["multiple_topics"][0] = 11
            df = diff(f, x)
            x_value = random.randint(1, 5)
            y_value = f.subs(x, x_value)
            gradient = -1 / (df.subs(x, x_value))
            y_intercept = y_value - (x_value * gradient)
            f_str = simplify_f(f)
            question = f"What is the equation of the normal to the curve with the equation y={f_str} at the point ({x_value}, {y_value}). Give your answer in the form y=mx+c and give answers in the form of fractions where needed."
            if y_intercept == zoo or y_intercept == 0:
                answer = f"y={gradient}x"
            elif y_intercept > 0:
                answer = f"y={gradient}x+{y_intercept}"
            else:
                answer = f"y={gradient}x{y_intercept}"
            # answer = f"y={gradient}x+{y_intercept}" if y_intercept > 0 else f"y={gradient}x{y_intercept}"

    return question, answer, difficulty_factors, True

def integration_questions(question_subtopic_chosen : str, difficulty_factors : dict):
    question, answer = "", ""
    x = symbols("x")
    cubic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    quadratic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    linear_value = random.randint(1, 10) * random.choice([0, 1, -1])
    number_value = random.randint(1, 10)

    if cubic_value == 0 and quadratic_value == 0 and linear_value == 0:
        return question, answer, difficulty_factors, False
    f = cubic_value * x ** 3 + quadratic_value * x ** 2 + linear_value * x + number_value

    match question_subtopic_chosen:
        case "basic_integration":
            difficulty_factors["difficulty_of_values"][0] = 7
            difficulty_factors["difficulty_of_answer"][0] = 7
            difficulty_factors["number_of_steps"][0] = 6
            difficulty_factors["maths_topic"][0] = 8
            difficulty_factors["depth_of_knowledge"][0] = 7
            difficulty_factors["multiple_topics"][0] = 7
            answer = f"{integrate(f, x)} + c"
            f_str = simplify_f(f)
            question = f"What is ∫ f(x) dx when f(x) = {f_str}?"

        case "definite_integrals":
            difficulty_factors["difficulty_of_values"][0] = 9
            difficulty_factors["difficulty_of_answer"][0] = 9
            difficulty_factors["number_of_steps"][0] = 8
            difficulty_factors["maths_topic"][0] = 9
            difficulty_factors["depth_of_knowledge"][0] = 8
            difficulty_factors["multiple_topics"][0] = 8
            lower_point = random.randint(0, 3)
            upper_point = random.randint(lower_point+1, 6)
            answer = integrate(f, (x, lower_point, upper_point))
            f_str = simplify_f(f)
            question = f"What is ∫ f(x) from {lower_point} to {upper_point} when f(x) = {f_str}? Give answers in the form of fractions where needed."

        case "finding_area":
            difficulty_factors["difficulty_of_values"][0] = 9
            difficulty_factors["difficulty_of_answer"][0] = 9
            difficulty_factors["number_of_steps"][0] = 9
            difficulty_factors["maths_topic"][0] = 10
            difficulty_factors["depth_of_knowledge"][0] = 10
            difficulty_factors["multiple_topics"][0] = 10
            lower_point = random.randint(0, 3)
            upper_point = random.randint(lower_point + 1, 6)
            answer = abs(integrate(f, (x, lower_point, upper_point)))
            f_str = simplify_f(f)
            question = f"What is the area of under the curve y=f(x) over the interval {lower_point} < x < {upper_point} where f(x) = {f_str}? Give answers in the form of fractions where needed."

        case "finding_complex_area":
            difficulty_factors["difficulty_of_values"][0] = 10
            difficulty_factors["difficulty_of_answer"][0] = 10
            difficulty_factors["number_of_steps"][0] = 11
            difficulty_factors["maths_topic"][0] = 10
            difficulty_factors["depth_of_knowledge"][0] = 11
            difficulty_factors["multiple_topics"][0] = 11
            lower_point = random.randint(-4, 1)
            upper_point = random.randint(1, 4)
            integral_1 = integrate(f, (x, lower_point, 0))
            integral_2 = integrate(f, (x, 0, upper_point))
            answer = abs(integral_1) + abs(integral_2)
            f_str = simplify_f(f)
            question = f"What is the area of under the curve y=f(x) over the interval {lower_point} < x < {upper_point} where f(x) = {f_str}? Give answers in the form of fractions where needed."

    return question, answer, difficulty_factors, True

def simplify_f(f):
    f_str = str(f)
    for x in range(len(f_str)):
        if x < len(f_str) - 1 and f_str[x] == "*" and f_str[x + 1] == "*":
            f_str = f"{f_str[0:x]}^{f_str[x + 2:]}"
        elif x < len(f_str) - 1 and f_str[x] == "*":
            f_str = f"{f_str[0:x]}{f_str[x + 1:]}"
    return f_str

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

# calculus_questions_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)
