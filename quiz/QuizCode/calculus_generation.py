import random
from sympy import diff, integrate, symbols, limit, solveset, solve

from .helper_functions import calculate_difficulty, answer_generation

def calculus_questions_generation(entered_difficulty : int, question_types : list, difficulty_factors: dict):
    while True:
        question_type_chosen = random.choice(question_types)
        question_topic_chosen = random.choice(["differentiation"])
        x = symbols("x")
        match question_topic_chosen:
            case "differentiation":
                question_subtopic_chosen = random.choice(["basic_differentiation", "second_order_differentiation"])
                question, answer, difficulty_factors, is_valid = differentiation_questions(question_subtopic_chosen, difficulty_factors)
                if is_valid:
                    difficulty_factors["question_type"][0] = 10
                    difficulty_factors["answers_similarity"][0] = 9
                    calculate_difficulty(difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                    if entered_difficulty == final_difficulty or 1 == 1:
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break
                else:
                    pass
            case "integration":
                integration_questions()
                break
    answer = str(answer)
    return question, answer, difficulty_weighting


def differentiation_questions(question_subtopic_chosen : str, difficulty_factors : dict):
    x = symbols("x")
    cubic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    quadratic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    linear_value = random.randint(1, 10) * random.choice([0, 1, -1])
    number_value = random.randint(1, 10) * random.choice([0, 1, -1])
    if cubic_value == 0 and quadratic_value == 0 and linear_value == 0:
        return "", "", difficulty_factors, False
    f = cubic_value * x ** 3 + quadratic_value * x ** 2 + linear_value * x + number_value
    match question_subtopic_chosen:
        case "basic_differentiation":
            df = diff(f, x)
            answer = df
            question = f"What is the first order derivative of {f}?"
            if "x" not in str(answer):
                return "", "", difficulty_factors, False
        case "second_order_differentiation":
            d2f = diff(f, x, 2)
            answer = d2f
            question = f"What is the second order derivative of {f}?"
            if "x" not in str(answer):
                return "", "", difficulty_factors, False
        case "answer_from_derivative":
            df = diff(f, x)
            x_value = random.randint(1, 5)
            question = f"What is the answer to f\'({x_value}) when f(x) = {f}"
            answer = df.subs(x, x_value)
        case "finding_x":
            df = diff(f, x)
            question = f"What is the value of x when f\'(x) = 0 and f(x) = {f}"
            answer = solve(df, x)
        case "tangents":
            df = diff(f, x)
            x_value = random.randint(1, 5)
            y_value = f.subs(x, x_value)
            gradient = df.subs(x, x_value)
            y_intercept = y_value - (x_value * gradient)
            question = f"What is the equation of the tangent to the curve with the equation y={f} at the point ({x_value}, {y_value}). Give your answer in the form y=mx+c"
            answer = f"y={gradient}x+{y_intercept}" if y_intercept > 0 else f"y={gradient}x{y_intercept}"
        case "normals":
            df = diff(f, x)
            x_value = random.randint(1, 5)
            y_value = f.subs(x, x_value)
            gradient = -1 / (df.subs(x, x_value))
            y_intercept = y_value - (x_value * gradient)
            question = f"What is the equation of the normal to the curve with the equation y={f} at the point ({x_value}, {y_value}). Give your answer in the form y=mx+c and using fractions where needed"
            answer = f"y={gradient}x+{y_intercept}" if y_intercept > 0 else f"y={gradient}x{y_intercept}"

    return question, answer, difficulty_factors, True

def integration_questions():
    x = symbols("x")
    quadratic_value = random.randint(1, 10)
    linear_value = random.randint(1, 10)
    number_value = random.randint(1, 10)
    df = quadratic_value*x**2 + linear_value*x + number_value
    f = integrate(df, x)
    print(f"{df} {type(df)}")
    print(f"{f} + c {type(f)}")

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