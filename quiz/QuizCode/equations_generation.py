import random
from sympy import expand, symbols, Eq, solveset, discriminant, solve

from .helper_functions import answer_generation_equations, calculate_difficulty

# Linear equations, quadratic equations, quadratic formula, completing the square, simultaneous equations, quadratic simultaneous equations, inequalities, quadratic inequalities
def equations_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question_type_chosen = "free_text"
    question = ""
    answer = []
    answers = []
    multiple_answers = "No"
    while True:
        equation_type = random.choice(["linear", "whole_quadratic", "floating_quadratic", "linear_simultaneous"])
        question_type_chosen = random.choice(question_types)
        if entered_difficulty >= 8:
            equation_type = "quadratic_simultaneous"

        equation, final_answer = generate_equation(equation_type, difficulty_factors)
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors=difficulty_factors)
        if final_difficulty == entered_difficulty:
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    match question_type_chosen:
        case "free_text":
            match equation_type:
                case "linear":
                    question = f"{equation} \t Find x to 2 decimal places."
                    answer = [round(float(final_answer[0]), 2)]
                case "whole_quadratic":
                    question = f"{equation} \t Find both values of x to 2 decimal places."
                    answer = [round(float(final_answer[0]), 2), round(float(final_answer[1]), 2)]
                    multiple_answers = "TwoSame"
                case "floating_quadratic":
                    question = f"{equation} \t Find both values of x to 2 decimal places."
                    answer = [round(float(final_answer[0]), 2), round(float(final_answer[1]), 2)]
                    multiple_answers = "TwoSame"
                case "linear_simultaneous":
                    question = f"{equation} \t Find the value of x and y to 2 decimal places."
                    answer.append(round(float(final_answer[0][1]), 2))
                    answer.append(round(float(final_answer[1][1]), 2))
                    multiple_answers = "TwoDifferent"
                case "quadratic_simultaneous":
                    question = f"{equation} \t Find both values of x and y to 2 decimal places."
                    answer.append(round(float(final_answer[0][0]), 2))
                    answer.append(round(float(final_answer[0][1]), 2))
                    answer.append(round(float(final_answer[1][0]), 2))
                    answer.append(round(float(final_answer[1][0]), 2))
                    multiple_answers = "FourDifferent"
                case _:
                    pass
        case "multiple-choice":
            question = f"{equation}\n"
        case "true/false":
            question = f"{equation}\n"
            if final_answer[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting, multiple_answers

def generate_equation(equation_type : str, difficulty_factors : dict):
    x = symbols("x")
    y = symbols("y")
    final_answer = 0
    equation = ""

    match equation_type:
        case "linear":
            difficulty_factors["maths_topic"][0] = 4
            difficulty_factors["difficulty_of_values"][0] = 3
            difficulty_factors["depth_of_knowledge"][0] = 4
            difficulty_factors["multiple_topics"][0] = 4
            difficulty_factors["difficulty_of_answer"][0] = 3
            difficulty_factors["number_of_steps"][0] = 3
            linear_value = random.choice([1, -1]) * random.randint(1, 10)
            number_value = random.choice([1, -1]) * random.randint(1, 20)
            final_answer = solveset(linear_value * x + number_value, x)
            equation = f"{linear_value}x + {number_value} = 0"
        case "whole_quadratic":
            difficulty_factors["maths_topic"][0] = 5
            difficulty_factors["difficulty_of_values"][0] = 3
            difficulty_factors["depth_of_knowledge"][0] = 5
            difficulty_factors["multiple_topics"][0] = 5
            difficulty_factors["difficulty_of_answer"][0] = 4
            difficulty_factors["number_of_steps"][0] = 5
            root_1 = random.choice([1, -1]) * random.randint(1, 10)
            root_2 = random.choice([1, -1]) * random.randint(1, 10)
            common_factor = random.randint(1, 3)
            if common_factor > 1:
                difficulty_factors["difficulty_of_values"][0] += 1
                difficulty_factors["difficulty_of_answer"][0] += 1
                difficulty_factors["number_of_steps"][0] += 1
            final_answer = solveset(common_factor * (x+root_1) * (x+root_2), x)
            equation_start = expand(common_factor * (x+root_1) * (x+root_2))
            equation = f"{equation_start.coeff(x, 2)}x**2 + {equation_start.coeff(x, 1)}x + {equation_start.coeff(x, 0)} = 0"
        case "floating_quadratic":
            while True:
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 4
                difficulty_factors["depth_of_knowledge"][0] = 7
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 6
                difficulty_factors["number_of_steps"][0] = 6
                quadratic_value = 1
                linear_value = random.choice([1, -1]) * random.randint(1, 10)
                number_value = random.choice([1, -1]) * random.randint(1, 10)
                common_factor = random.randint(1, 3)
                if common_factor > 1:
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["number_of_steps"][0] += 1
                equation_start = Eq(common_factor * x**2 + linear_value * x + number_value, 0)
                if discriminant(equation_start) >= 0 and not math.sqrt(discriminant(equation_start)).is_integer():
                    equation = f"{quadratic_value}x**2 + {linear_value}x + {number_value} = 0"
                    final_answer = solveset(quadratic_value * x**2 + linear_value * x + number_value, x)
                    break
        case "completing_the_square":
            pass
        # Adapted from https://reliability.readthedocs.io/en/latest/Solving%20simultaneous%20equations%20with%20sympy.html
        case "linear_simultaneous":
            while True:
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 4
                difficulty_factors["depth_of_knowledge"][0] = 5
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 6
                x_value_1 = random.choice([1, -1]) * random.randint(1, 10)
                y_value_1 = random.choice([1, -1]) * random.randint(1, 10)
                number_value_1 = random.choice([1, -1]) * random.randint(1, 30)
                x_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                y_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                number_value_2 = random.choice([1, -1]) * random.randint(1, 30)

                if x_value_1 > 5:
                    difficulty_factors["difficulty_of_values"][0] += 0.5
                    difficulty_factors["difficulty_of_answer"][0] += 0.5
                if x_value_2 > 5:
                    difficulty_factors["difficulty_of_values"][0] += 0.5
                    difficulty_factors["difficulty_of_answer"][0] += 0.5
                if y_value_1 > 5:
                    difficulty_factors["difficulty_of_values"][0] += 0.5
                    difficulty_factors["difficulty_of_answer"][0] += 0.5
                if y_value_1 > 5:
                    difficulty_factors["difficulty_of_values"][0] += 0.5
                    difficulty_factors["difficulty_of_answer"][0] += 0.5

                equation_1 = Eq(x_value_1*x + y_value_1*y, number_value_1)
                equation_2 = Eq(x_value_2*x + y_value_2*y, number_value_2)
                equation = f"{equation_1} \n {equation_2}"

                answers = solve((equation_1, equation_2), (x, y))
                if type(answers) == dict:
                    if list(answers.items())[0][1].is_integer and list(answers.items())[1][1].is_integer:
                        final_answer = list(answers.items())
                        break

        # Adapted from https://reliability.readthedocs.io/en/latest/Solving%20simultaneous%20equations%20with%20sympy.html
        case "quadratic_simultaneous":
            while True:
                difficulty_factors["maths_topic"][0] = 9
                difficulty_factors["difficulty_of_values"][0] = 8
                difficulty_factors["depth_of_knowledge"][0] = 8
                difficulty_factors["multiple_topics"][0] = 8
                difficulty_factors["difficulty_of_answer"][0] = 8
                difficulty_factors["number_of_steps"][0] = 9
                number_value_1 = random.choice([1, -1]) * random.randint(1, 30)
                x_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                y_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                number_value_2 = random.choice([1, -1]) * random.randint(1, 30)

                equation_1 = Eq(x**2 + y**2, number_value_1)
                equation_2 = Eq(x_value_2 * x + y_value_2 * y, number_value_2)
                equation = f"{equation_1} \n {equation_2}"

                final_answer = solve((equation_1, equation_2), (x, y))
                if (len(final_answer) == 2 and len(final_answer[0]) == 2 and len(final_answer[1]) == 2 and final_answer[0][0].is_integer and
                        final_answer[0][1].is_integer and final_answer[1][0].is_integer and final_answer[1][1].is_integer):
                    break
        case _:
            pass
    final_answer = list(final_answer)
    return equation, final_answer

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

# equations_question_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)