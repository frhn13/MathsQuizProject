import random
from sympy import expand, symbols, Eq, solveset, discriminant, solve
import math

from .helper_functions import calculate_difficulty

def equations_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question = ""
    answer = []
    multiple_answers = "No"
    while True: # Remains True until a valid question is generated with the entered difficulty
        time_needed = 60
        calculator_needed = False
        # Equations question subtopic is randomly chosen from this list
        equation_type = random.choice(["linear", "whole_quadratic", "floating_quadratic", "linear_simultaneous"])
        if entered_difficulty >= 8:
            equation_type = "quadratic_simultaneous"

        # Function generates equation based on the question subtopic
        equation, final_answer = generate_equation(equation_type, difficulty_factors)

        equation_str = str(equation)

        # Loops through every character in the equation for a question and replaces "2*x"
        # with "2x" and "x**2" with "x^2" to make the question more readable for the user
        for x in range(len(equation_str)):
            if x < len(equation_str) - 1 and equation_str[x] == "*" and equation_str[x + 1] == "*":
                equation_str = f"{equation_str[0:x]}^{equation_str[x + 2:]}"
            elif x < len(equation_str) - 1 and equation_str[x] == "*":
                equation_str = f"{equation_str[0:x]}{equation_str[x + 1:]}"

        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors=difficulty_factors) # Generates difficulty level of question
        if final_difficulty == entered_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
            break

    match equation_type:
        # Creates question depending on the equation type and puts all values of x and y in a list
        case "linear":
            question = f"{equation_str} \t Find x to 2 decimal places."
            answer = [round(float(final_answer[0]), 2)]
        case "whole_quadratic":
            # The time given to solve a question is increased for some equation types
            time_needed = 120
            question = f"{equation_str} \t Find both values of x."
            if len(final_answer) == 2:
                answer = [round(float(final_answer[0]), 2), round(float(final_answer[1]), 2)]
            else: answer = [round(float(final_answer[0]), 2)]
            multiple_answers = "TwoSame"
        case "floating_quadratic":
            time_needed = 180
            question = f"{equation_str} \t Find both values of x to 2 decimal places."
            calculator_needed = True
            if len(final_answer) == 2:
                answer = [round(float(final_answer[0]), 2), round(float(final_answer[1]), 2)]
            else:
                answer = [round(float(final_answer[0]), 2)]
            multiple_answers = "TwoSame"
        case "linear_simultaneous":
            time_needed = 120
            question = f"{equation_str} \t Find the value of x and y to 2 decimal places."
            answer.append(round(float(final_answer[0][1]), 2))
            answer.append(round(float(final_answer[1][1]), 2))
            multiple_answers = "TwoDifferent"
        case "quadratic_simultaneous":
            time_needed = 300
            question = f"{equation_str} \t Find both values of x and y to 2 decimal places."
            answer.append(round(float(final_answer[0][0]), 2))
            answer.append(round(float(final_answer[0][1]), 2))
            answer.append(round(float(final_answer[1][0]), 2))
            answer.append(round(float(final_answer[1][0]), 2))
            multiple_answers = "FourDifferent"
        case _:
            pass

    new_question = ""
    for x in range(len(question)): # Replaces 1x or 1y in question with x or y
        if question[x] == "1" and x+1 < len(question) and (question[x+1] == "x" or question[x+1] == "y"):
            pass
        else: new_question += question[x]

    return new_question, answer, difficulty_weighting, multiple_answers, calculator_needed, time_needed

def generate_equation(equation_type : str, difficulty_factors : dict):
    # Function generates different types of equations depending on what is passed in
    x = symbols("x")
    y = symbols("y")
    final_answer = 0
    equation = ""

    match equation_type:
        case "linear":
            # Generates a linear equation
            difficulty_factors["maths_topic"][0] = 4
            difficulty_factors["difficulty_of_values"][0] = 3
            difficulty_factors["depth_of_knowledge"][0] = 4
            difficulty_factors["multiple_topics"][0] = 4
            difficulty_factors["difficulty_of_answer"][0] = 3
            difficulty_factors["number_of_steps"][0] = 3
            # Randomly creates linear and number values for linear equation
            linear_value = random.choice([1, -1]) * random.randint(1, 10)
            number_value = random.choice([1, -1]) * random.randint(1, 20)
            final_answer = solveset(linear_value * x + number_value, x) # Finds value of x when linear equation = 0
            equation = f"{linear_value}x + {number_value} = 0"
        case "whole_quadratic":
            # Generates a quadratic equation
            difficulty_factors["maths_topic"][0] = 5
            difficulty_factors["difficulty_of_values"][0] = 3
            difficulty_factors["depth_of_knowledge"][0] = 5
            difficulty_factors["multiple_topics"][0] = 5
            difficulty_factors["difficulty_of_answer"][0] = 4
            difficulty_factors["number_of_steps"][0] = 5
            # Randomly creates roots for quadratic equation, ensuring values of x are whole numbers
            root_1 = random.choice([1, -1]) * random.randint(1, 10)
            root_2 = random.choice([1, -1]) * random.randint(1, 10)
            common_factor = random.randint(1, 3)
            if common_factor > 1: # Questions considered harder if coefficients are larger
                difficulty_factors["difficulty_of_values"][0] += 1
                difficulty_factors["difficulty_of_answer"][0] += 1
                difficulty_factors["number_of_steps"][0] += 1
            # Finds values of x when equation = 0
            final_answer = solveset(common_factor * (x+root_1) * (x+root_2), x)
            # Expanded equation is given to user in question
            equation_start = expand(common_factor * (x+root_1) * (x+root_2))
            equation = f"{equation_start.coeff(x, 2)}x**2 + {equation_start.coeff(x, 1)}x + {equation_start.coeff(x, 0)} = 0"
        case "floating_quadratic":
            while True:
                # Generates a quadratic equation where the values of x are floats and solved by quadratic formula
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 7
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 6
                difficulty_factors["number_of_steps"][0] = 6
                # Randomly creates quadratic, linear and number values for quadratic equation
                quadratic_value = 1
                linear_value = random.choice([1, -1]) * random.randint(1, 10)
                number_value = random.choice([1, -1]) * random.randint(1, 10)
                common_factor = random.randint(1, 3)
                if common_factor > 1: # Questions considered harder if coefficients are larger
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["number_of_steps"][0] += 1
                equation_start = Eq(common_factor * x**2 + linear_value * x + number_value, 0)
                # Checks if discriminant of equation is more than 0, so it can be solved by quadratic formula, otherwise tries to generate equation again
                if discriminant(equation_start) >= 0 and not math.sqrt(discriminant(equation_start)).is_integer():
                    equation = f"{quadratic_value}x**2 + {linear_value}x + {number_value} = 0"
                    final_answer = solveset(quadratic_value * x**2 + linear_value * x + number_value, x)
                    break
        # Adapted from https://reliability.readthedocs.io/en/latest/Solving%20simultaneous%20equations%20with%20sympy.html
        case "linear_simultaneous":
            while True:
                # Generates simultaneous equations which where both equations are linear
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 4
                difficulty_factors["depth_of_knowledge"][0] = 5
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 6
                # Generates number values and coefficients of x and y for both equations
                x_value_1 = random.choice([1, -1]) * random.randint(1, 10)
                y_value_1 = random.choice([1, -1]) * random.randint(1, 10)
                number_value_1 = random.choice([1, -1]) * random.randint(1, 30)
                x_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                y_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                number_value_2 = random.choice([1, -1]) * random.randint(1, 30)

                # Question becomes harder if x and y values are more than 5
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
                equation = f"{x_value_1}x + {y_value_1}y = {number_value_1} | {x_value_2}x + {y_value_2}y = {number_value_2}"

                # Gets answers for x and y and breaks out of loop if they are both whole numbers
                answers = solve((equation_1, equation_2), (x, y))
                if type(answers) == dict:
                    if list(answers.items())[0][1].is_integer and list(answers.items())[1][1].is_integer:
                        final_answer = list(answers.items())
                        break

        # Adapted from https://reliability.readthedocs.io/en/latest/Solving%20simultaneous%20equations%20with%20sympy.html
        case "quadratic_simultaneous":
            while True:
                # Generates simultaneous equations which where one equation is linear and the other is quadratic
                difficulty_factors["maths_topic"][0] = 9
                difficulty_factors["difficulty_of_values"][0] = 8
                difficulty_factors["depth_of_knowledge"][0] = 8
                difficulty_factors["multiple_topics"][0] = 8
                difficulty_factors["difficulty_of_answer"][0] = 8
                difficulty_factors["number_of_steps"][0] = 9
                # Generates number values and coefficients of x and y for both equations
                number_value_1 = random.choice([1, -1]) * random.randint(1, 30)
                x_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                y_value_2 = random.choice([1, -1]) * random.randint(1, 10)
                number_value_2 = random.choice([1, -1]) * random.randint(1, 30)

                equation_1 = Eq(x**2 + y**2, number_value_1)
                equation_2 = Eq(x_value_2 * x + y_value_2 * y, number_value_2)

                equation = f"x^2 + y^2 = {number_value_1} | {x_value_2}x + {y_value_2}y = {number_value_2}"
                # Gets answers for x and y and breaks out of loop if they are all whole numbers
                if discriminant(equation_2) >= 0:
                    final_answer = solve((equation_1, equation_2), (x, y))
                    if (len(final_answer) == 2 and len(final_answer[0]) == 2 and len(final_answer[1]) == 2 and final_answer[0][0].is_integer and
                            final_answer[0][1].is_integer and final_answer[1][0].is_integer and final_answer[1][1].is_integer):
                        break
        case _:
            pass
    final_answer = list(final_answer)
    return equation, final_answer
