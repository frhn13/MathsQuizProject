import random
from fractions import Fraction
from sympy import simplify, expand, symbols


def calculate_difficulty(difficulty_factors : dict):
    summed_difficulty = 0
    for factor in difficulty_factors.values():
        summed_difficulty += (factor[0] * (factor[1]/0.125))
    # summed_difficulty = summed_difficulty / 2
    return summed_difficulty / 8, summed_difficulty // 8

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
    coefficient_1 = random.randint(1, 2) * random.choice([-1, 1])
    coefficient_2 = random.randint(1, 2) * random.choice([-1, 1])
    factorise = (coefficient_1*x + num1) * (coefficient_2*x + num2)
    return expand(factorise), coefficient_1, coefficient_2

def factorisation_and_simplification(difficulty_factors : dict):
    x = symbols("x")
    difficulty_factors["maths_topic"][0] = 4
    difficulty_factors["difficulty_of_values"][0] = 3
    difficulty_factors["depth_of_knowledge"][0] = 4
    difficulty_factors["multiple_topics"][0] = 3
    difficulty_factors["difficulty_of_answer"][0] = 3
    difficulty_factors["number_of_steps"][0] = 3

    common_factor = random.randint(1, 5)

    if random.random() > 0.5:
        quadratic_value, linear_value, number_value = generate_expression(random.choice([True, False]),
                                                                          random.choice([True, False]),
                                                                          random.choice([True, False]))
        if quadratic_value == 0 and linear_value == 0 or quadratic_value == 0 and number_value == 0 \
                or linear_value == 0 and number_value == 0:
            expression = None

        else:
            expression = common_factor * (quadratic_value + linear_value + number_value)
            if expression.coeff(x, 2) != 0:
                difficulty_factors["difficulty_of_values"][0] += 1
                difficulty_factors["difficulty_of_answer"][0] += 1
                difficulty_factors["number_of_steps"][0] += 1
            if expression.coeff(x, 2) < 0:
                difficulty_factors["difficulty_of_values"][0] += 1
                difficulty_factors["difficulty_of_answer"][0] += 1
    else:
        expression, coefficient_1, coefficient_2 = generate_complex_expression()
        difficulty_factors["difficulty_of_values"][0] += 1
        difficulty_factors["difficulty_of_answer"][0] += 1
        difficulty_factors["number_of_steps"][0] += 1
        if coefficient_1 < 0 or coefficient_2 < 0:
            difficulty_factors["difficulty_of_values"][0] += 1
            difficulty_factors["difficulty_of_answer"][0] += 1

    return difficulty_factors, expression

def answer_generation(real_answer : int, question_type : str, difficulty_factors : dict, should_be_positive : bool):
    answers = []
    if question_type == "free_text":
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        answers.append(real_answer)

    elif question_type == "multiple-choice":
        difficulty_factors["question_type"][0] = 5
        while True:
            difficulty_factors["answers_similarity"][0] = 6
            answers = []
            for i in range(3):
                answers.append(random.randint(real_answer - 20, real_answer + 20))
                if abs(answers[i] - real_answer) >= 10:
                    difficulty_factors["answers_similarity"][0] -= 1
            answers.append(real_answer)
            is_positive = True
            for answer in answers:
                if answer <= 0: is_positive = False
            if len(answers) == len(set(answers)) and (not should_be_positive or (should_be_positive and is_positive)):
                random.shuffle(answers)
                break

    elif question_type == "true/false":
        difficulty_factors["question_type"][0] = 2
        difficulty_factors["answers_similarity"][0] = 4
        if random.random() > 0.5:
            while True:
                answers = [random.randint(real_answer - 20, real_answer + 20)]
                if abs(answers[0] - real_answer) >= 10:
                    difficulty_factors["answers_similarity"][0] -= 2
                if not should_be_positive or (should_be_positive and answers[0] > 0):
                    break
        else:
            answers.append(real_answer)

    return answers, difficulty_factors

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
        difficulty_factors["answers_similarity"][0] = 4
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

def answer_generation_decimals(real_answer : float, question_type : str, difficulty_factors : dict, should_be_positive : bool):
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
            is_positive = True
            for answer in answers:
                if answer <= 0: is_positive = False
            if len(answers) == len(set(answers)) and (not should_be_positive or (should_be_positive and is_positive)):
                random.shuffle(answers)
                break

    elif question_type == "true/false":
        difficulty_factors["question_type"][0] = 2
        difficulty_factors["answers_similarity"][0] = 4
        if random.random() > 0.5:
            while True:
                answers = [random.choice([real_answer - 0.5, real_answer - 0.4, real_answer - 0.3,
                                                  real_answer - 0.2, real_answer - 0.1, real_answer + 0.1,
                                                  real_answer + 0.2, real_answer + 0.3, real_answer + 0.4, real_answer + 0.5])]
                if abs(answers[0] - real_answer) >= 0.2:
                    difficulty_factors["answers_similarity"][0] -= 2
                if not should_be_positive or (should_be_positive and answers[0] > 0):
                    break
        else:
            answers.append(real_answer)

    return answers, difficulty_factors

def algebraic_fractions(difficulty_factors : dict):
    difficulty_factors["maths_topic"][0] = 5
    difficulty_factors["difficulty_of_values"][0] = 7
    difficulty_factors["depth_of_knowledge"][0] = 6
    difficulty_factors["multiple_topics"][0] = 5
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

        numerator_str = str(numerator)
        denominator_str = str(denominator)

        for x in range(len(numerator_str)):
            if x < len(numerator_str) - 1 and numerator_str[x] == "*" and numerator_str[x + 1] == "*":
                numerator_str = f"{numerator_str[0:x]}^{numerator_str[x + 2:]}"
            elif x < len(numerator_str) - 1 and numerator_str[x] == "*":
                numerator_str = f"{numerator_str[0:x]}{numerator_str[x + 1:]}"

        for x in range(len(denominator_str)):
            if x < len(denominator_str) - 1 and denominator_str[x] == "*" and denominator_str[x + 1] == "*":
                denominator_str = f"{denominator_str[0:x]}^{denominator_str[x + 2:]}"
            elif x < len(denominator_str) - 1 and denominator_str[x] == "*":
                denominator_str = f"{denominator_str[0:x]}{denominator_str[x + 1:]}"

        question = f"Simplify the fraction ({numerator_str})/({denominator_str})"
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
            difficulty_factors["number_of_steps"][0] -= 1
        if linear_value_denominator == 0:
            difficulty_factors["difficulty_of_values"][0] -= 0.5
            difficulty_factors["number_of_steps"][0] -= 1
        if number_value_numerator == 0:
            difficulty_factors["difficulty_of_values"][0] -= 0.5
            difficulty_factors["number_of_steps"][0] -= 0.5
        if number_value_denominator == 0:
            difficulty_factors["difficulty_of_values"][0] -= 0.5
            difficulty_factors["number_of_steps"][0] -= 0.5
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
