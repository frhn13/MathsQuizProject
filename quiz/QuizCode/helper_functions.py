import math
import random
from fractions import Fraction
from sympy import simplify, expand, symbols, roots, Eq, solveset, discriminant, solve


def calculate_difficulty(difficulty_factors : dict):
    summed_difficulty = 0
    for factor in difficulty_factors.values():
        summed_difficulty += (factor[0] * (factor[1]/0.125))
    summed_difficulty = summed_difficulty / 2
    return summed_difficulty / 8, summed_difficulty // 8

def generate_equation(equation_type : str, difficulty_factors : dict):
    x = symbols("x")
    y = symbols("y")
    final_answer = 0
    equation = ""

    match equation_type:
        case "linear":
            difficulty_factors["maths_topic"][0] = 4
            difficulty_factors["difficulty_of_values"][0] = 3
            difficulty_factors["depth_of_knowledge"][0] = 5
            difficulty_factors["multiple_topics"][0] = 5
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
                    #print(type(final_answer[0][0]))
                    #print(final_answer[0][0])
                    #t = int(final_answer[0][0])
                    #print(t)
                    #print(type(t))
                    break
        case _:
            pass
    final_answer = list(final_answer)
    #print(final_answer)
    return equation, final_answer

def generate_expression(quadratic_value_added : bool, linear_value_added : bool, number_value_added : bool):
    x = symbols("x")

    quadratic_value = 0
    linear_value = 0
    number_value = 0

    if quadratic_value_added:
        quadratic_value = x ** 2 * random.choice([-3, -2, -1, 1, 2, 3])
    if linear_value_added:
        linear_value = x * random.choice([-3, -2, -1, 1, 2, 3])
    if number_value_added:
        number_value = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    return quadratic_value, linear_value, number_value

def generate_complex_expression():
    x = symbols("x")
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    coefficient_1 = random.randint(1, 2)
    coefficient_2 = random.randint(1, 2)
    factorise = (coefficient_1*x + num1) * (coefficient_2*x + num2)
    return expand(factorise)

def answer_generation(real_answer : int, question_type : str, difficulty_factors : dict):
    answers = []
    if question_type == "free_text":
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        answers.append(real_answer)

    elif question_type == "multiple-choice":
        difficulty_factors["question_type"][0] = 5
        difficulty_factors["answers_similarity"][0] = 6
        while True:
            answers = []
            for i in range(3):
                answers.append(random.randint(real_answer - 20, real_answer + 20))
                if abs(answers[i] - real_answer) >= 10:
                    difficulty_factors["answers_similarity"][0] -= 1
            answers.append(real_answer)
            if len(answers) == len(set(answers)):
                random.shuffle(answers)
                break

    elif question_type == "true/false":
        difficulty_factors["question_type"][0] = 2
        difficulty_factors["answers_similarity"][0] = 5
        if random.random() > 0.5:
            answers = [random.randint(real_answer - 20, real_answer + 20)]
            if abs(answers[0] - real_answer) >= 10:
                difficulty_factors["answers_similarity"][0] -= 2
        else:
            answers.append(real_answer)

    return answers, difficulty_factors

def answer_generation_equations(real_answer : list, question_type : str, difficulty_factors : dict):
    if question_type == "free_text":
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        return real_answer, difficulty_factors

def answer_generation_fractions(real_answer : str, question_type : str, difficulty_factors : dict):
    answers = []
    if question_type == "free_text":
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        answers.append(real_answer)

    elif question_type == "multiple-choice":
        difficulty_factors["question_type"][0] = 5
        difficulty_factors["answers_similarity"][0] = 6
        numerator = Fraction(real_answer).numerator
        denominator = Fraction(real_answer).denominator
        while True:
            answers_num = []
            for i in range(3):
                answers_num.append([random.randint(numerator - 10, numerator + 10), random.randint(denominator - 10, denominator + 10)])
                if abs(answers_num[i][0] - numerator) >= 5:
                    difficulty_factors["answers_similarity"][0] -= 0.5
                if abs(answers_num[i][1] - denominator) >= 5:
                    difficulty_factors["answers_similarity"][0] -= 0.5
            for i in range(len(answers_num)):
                answers.append(f"{answers_num[i][0]}/{answers_num[i][1]}")
            answers.append(real_answer)
            if len(answers) == len(set(answers)):
                random.shuffle(answers)
                break

    elif question_type == "true/false":
        difficulty_factors["question_type"][0] = 2
        difficulty_factors["answers_similarity"][0] = 5
        numerator = Fraction(real_answer).numerator
        denominator = Fraction(real_answer).denominator
        if random.random() > 0.5:
            answers_num = [
                [random.randint(numerator - 10, numerator + 10), random.randint(denominator - 10, denominator + 10)]]
            if abs(answers_num[0][0] - numerator) >= 5:
                difficulty_factors["answers_similarity"][0] -= 1
            if abs(answers_num[0][1] - denominator) >= 5:
                difficulty_factors["answers_similarity"][0] -= 1
            answers.append(f"{answers_num[0][0]}/{answers_num[0][1]}")
        else:
            answers.append(real_answer)
    return answers, difficulty_factors

def answer_generation_decimals(real_answer : float, question_type : str, difficulty_factors : dict):
    answers = []
    if question_type == "free_text":
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        answers.append(real_answer)

    if question_type == "multiple-choice":
        difficulty_factors["question_type"][0] = 5
        difficulty_factors["answers_similarity"][0] = 6
        while True:
            answers = []
            for i in range(3):
                answers.append(random.choice([real_answer - 0.5, real_answer - 0.4, real_answer - 0.3,
                                              real_answer - 0.2, real_answer - 0.1, real_answer + 0.1,
                                              real_answer + 0.2, real_answer + 0.3, real_answer + 0.4, real_answer + 0.5]))
                if abs(answers[i] - real_answer) >= 10:
                    difficulty_factors["answers_similarity"][0] -= 1
            answers.append(real_answer)
            if len(answers) == len(set(answers)):
                random.shuffle(answers)
                break

    elif question_type == "true/false":
        difficulty_factors["question_type"][0] = 2
        difficulty_factors["answers_similarity"][0] = 5
        if random.random() > 0.5:
            answers = [random.choice([real_answer - 0.5, real_answer - 0.4, real_answer - 0.3,
                                              real_answer - 0.2, real_answer - 0.1, real_answer + 0.1,
                                              real_answer + 0.2, real_answer + 0.3, real_answer + 0.4, real_answer + 0.5])]
            if abs(answers[0] - real_answer) >= 10:
                difficulty_factors["answers_similarity"][0] -= 2
        else:
            answers.append(real_answer)

    return answers, difficulty_factors

def algebraic_fractions(difficulty_factors : dict):
    difficulty_factors["maths_topic"][0] = 6
    difficulty_factors["difficulty_of_values"][0] = 6
    difficulty_factors["depth_of_knowledge"][0] = 6
    difficulty_factors["multiple_topics"][0] = 6
    difficulty_factors["difficulty_of_answer"][0] = 5
    difficulty_factors["number_of_steps"][0] = 7

    question_type_chosen = "free_text"
    question = None
    answer = None

    x = symbols("x")
    common_factor = random.randint(1, 3)
    quadratic_value_numerator, linear_value_numerator, number_value_numerator = generate_expression(
        random.choice([True, False]), random.choice([True, False]), random.choice([True, False]))
    quadratic_value_denominator, linear_value_denominator, number_value_denominator = generate_expression(
        random.choice([True, False]), random.choice([True, False]), random.choice([True, False]))
    if quadratic_value_numerator == 0 or linear_value_numerator == 0:
        return question, answer, question_type_chosen
    elif quadratic_value_denominator == 0 or linear_value_denominator == 0:
        return question, answer, question_type_chosen
    else:
        numerator = common_factor * random.randint(1, 3) * (
                quadratic_value_numerator + linear_value_numerator + number_value_numerator)
        denominator = common_factor * random.randint(1, 3) * (
                quadratic_value_denominator + linear_value_denominator + number_value_denominator)
        question = f"Simplify {numerator}/{denominator}"
        numerator_terms = numerator.as_ordered_terms()
        denominator_terms = denominator.as_ordered_terms()
        if quadratic_value_numerator == 0:
            difficulty_factors["difficulty_of_values"][0] -= 1
            difficulty_factors["number_of_steps"][0] -= 1
        if quadratic_value_denominator == 0:
            difficulty_factors["difficulty_of_values"][0] -= 1
            difficulty_factors["number_of_steps"][0] -= 1
        if linear_value_numerator == 0:
            difficulty_factors["difficulty_of_values"][0] -= 0.5
        if linear_value_denominator == 0:
            difficulty_factors["difficulty_of_values"][0] -= 0.5
        if quadratic_value_numerator != 0 and numerator_terms[0].coeff(x, numerator.as_ordered_terms()[
            0].as_poly().degree()) > 1:
            difficulty_factors["difficulty_of_values"][0] += 0.5
        if quadratic_value_denominator != 0 and denominator_terms[0].coeff(x, denominator.as_ordered_terms()[
            0].as_poly().degree()) > 1:
            difficulty_factors["difficulty_of_values"][0] += 0.5
        answer = simplify(numerator / denominator)
        return question, answer, question_type_chosen

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

#generate_equation("linear_simultaneous", difficulty_factors)
#generate_equation("floating_quadratic", difficulty_factors)
#generate_equation("quadratic_simultaneous", difficulty_factors)
