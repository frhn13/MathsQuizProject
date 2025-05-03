import random
from sympy import diff, integrate, symbols, solve, zoo

from .helper_functions import calculate_difficulty

def calculus_questions_generation(entered_difficulty : int, question_types : list, difficulty_factors: dict):
    while True: # Remains True until a valid question is generated with the entered difficulty
        question_topic_chosen = random.choice(["differentiation", "integration"]) # Randomly chooses between differentiation and integration question
        calculator_needed = False
        time_needed = 60
        match question_topic_chosen:
            case "differentiation":
                # Randomly chooses differentiation topic to make question for
                question_subtopic_chosen = random.choice(["basic_differentiation", "second_order_differentiation", "answer_from_derivative", "finding_x", "tangents", "normals"])
                question, answer, difficulty_factors, is_valid, time_needed = differentiation_questions(question_subtopic_chosen, difficulty_factors)
                if is_valid: # Checks if question generated is valid, otherwise will start again
                    if question_subtopic_chosen in ("answer_from_derivative", "finding_x", "tangents", "normals"):
                        calculator_needed = True
                    difficulty_factors["question_type"][0] = 10 # Assigns values to some difficulty factors
                    difficulty_factors["answers_similarity"][0] = 9
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Gets final difficulty level of question
                    if entered_difficulty == final_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break
                else:
                    pass
            case "integration":
                # Randomly chooses integration topic to make question for
                question_subtopic_chosen = random.choice(
                    ["basic_integration", "definite_integrals", "finding_area", "finding_complex_area"])
                question, answer, difficulty_factors, is_valid, time_needed = integration_questions(question_subtopic_chosen, difficulty_factors)
                if is_valid: # Checks if question generated is valid, otherwise will start again
                    if question_subtopic_chosen in ("definite_integrals", "finding_area", "finding_complex_area"):
                        calculator_needed = True
                    difficulty_factors["question_type"][0] = 10
                    difficulty_factors["answers_similarity"][0] = 9
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Gets final difficulty level of question
                    if entered_difficulty == final_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break
    answer = str(answer)

    new_question = ""
    for x in range(len(question)): # Replaces 1x or 1y in question with x or y
        if question[x] == "1" and x + 1 < len(question) and (question[x + 1] == "x" or question[x + 1] == "y"):
            pass
        else:
            new_question += question[x]

    return new_question, answer, difficulty_weighting, calculator_needed, time_needed


# Function for making differentiation questions of different subtopics
def differentiation_questions(question_subtopic_chosen : str, difficulty_factors : dict):
    time_needed = 60
    question, answer = "", ""
    x = symbols("x")
    # Randomly generates positive, negative or no value for the coefficients in the function
    cubic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    quadratic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    linear_value = random.randint(1, 10) * random.choice([0, 1, -1])
    number_value = random.randint(1, 10) * random.choice([0, 1, -1])
    # Cubic, quadratic or linear coefficient must have a value for question to be generated
    if cubic_value == 0 and quadratic_value == 0 and linear_value == 0:
        return question, answer, difficulty_factors, False, time_needed
    f = cubic_value * x ** 3 + quadratic_value * x ** 2 + linear_value * x + number_value

    difficulty_factors["difficulty_of_values"][0] = 7
    difficulty_factors["difficulty_of_answer"][0] = 7
    difficulty_factors["number_of_steps"][0] = 7

    # Question becomes easier if certain values aren't included in the function
    if cubic_value == 0:
        difficulty_factors["difficulty_of_values"][0] -= 0.5
        difficulty_factors["number_of_steps"][0] -= 0.5
        difficulty_factors["difficulty_of_answer"][0] -= 0.5
    if quadratic_value == 0:
        difficulty_factors["difficulty_of_values"][0] -= 0.5
        difficulty_factors["number_of_steps"][0] -= 0.5
        difficulty_factors["difficulty_of_answer"][0] -= 0.5
    if linear_value == 0:
        difficulty_factors["difficulty_of_values"][0] -= 0.5
        difficulty_factors["number_of_steps"][0] -= 0.5
        difficulty_factors["difficulty_of_answer"][0] -= 0.5

    match question_subtopic_chosen:
        # Makes question to ask for first-order derivative
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
            # If first-order derivative is just a number, then the question is too easy and therefore invalid
            if "x" not in str(answer):
                return "", "", difficulty_factors, False, time_needed

        case "second_order_differentiation":
            # Makes question to ask for second-order derivative
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
            # If second-order derivative is just a number, then the question is too easy and therefore invalid
            if "x" not in str(answer):
                return "", "", difficulty_factors, False, time_needed

        case "answer_from_derivative":
            # Makes question to find value of derivative when x has certain value
            time_needed = 120
            # If cubic value in function, or quadratic or linear value missing from function, then question is invalid
            if cubic_value != 0 or quadratic_value == 0 or linear_value == 0:
                return "", "", difficulty_factors, False, time_needed
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
            # Makes question to find value of x when first-order derivative has certain value
            time_needed = 120
            # If cubic value in function, or quadratic or linear value missing from function, then question is invalid
            if cubic_value != 0 or quadratic_value == 0 or linear_value == 0:
                return "", "", difficulty_factors, False, time_needed
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
            # Makes question to find equation of tangent at a curve using differentiation
            time_needed = 240
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
            # Makes question to find equation of normal at a curve using differentiation
            time_needed = 240
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

    return question, answer, difficulty_factors, True, time_needed


# Function for making integration questions of different subtopics
def integration_questions(question_subtopic_chosen : str, difficulty_factors : dict):
    time_needed = 60
    question, answer = "", ""
    x = symbols("x")
    # Randomly generates positive, negative or no value for the coefficients in the function
    cubic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    quadratic_value = random.randint(1, 10) * random.choice([0, 1, -1])
    linear_value = random.randint(1, 10) * random.choice([0, 1, -1])
    number_value = random.randint(1, 10)

    # Must be at least one of cubic, quadratic or linear coefficients with a value in the function
    if cubic_value == 0 and quadratic_value == 0 and linear_value == 0:
        return question, answer, difficulty_factors, False, time_needed
    f = cubic_value * x ** 3 + quadratic_value * x ** 2 + linear_value * x + number_value

    match question_subtopic_chosen:
        case "basic_integration":
            # Makes question to find integral equation of a function
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
            # Makes question to find definite integral of the function
            time_needed = 180
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
            # Makes question to find area under a curve using integration
            time_needed = 180
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
            # Makes question to find area under a curve where the x value goes more and less than 0 using integration
            time_needed = 240
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

    return question, answer, difficulty_factors, True, time_needed

def simplify_f(f):
    f_str = str(f)
    # Loops through every character in a function for a question and replaces "2*x"
    # with "2x" and "x**2" with "x^2" to make the question more readable for the user
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
