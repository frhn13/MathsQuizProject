import random
from math import gcd, lcm
from fractions import Fraction

from narwhals import Boolean
from sympy import simplify, factor, expand, symbols

# Difficulty weighting includes maths topic, type of question, difficulty of values used, similarity of potential answers,
# ambiguity of how to answer question, conceptual depth (needs fourmulae?), number of steps required, abstract vs concrete, time pressure, images
# Type of question: Free text -> multiple-choice -> true/false
# Topic: Calculus -> Trigonometry -> Quadratic questions -> Sequences -> Linear equations -> 3d shapes -> 2d shapes -> fractions and decimals -> operations
# Similarity of answers: How close answers are in MCQs, how close incorrect is to correct in true/false
# Difficulty of values used: How big values used are, whether final answer is whole number

def question_topic_selection(selected_topics : list, entered_difficulty : int, question_types : list):
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
    chosen_topic = random.choice(selected_topics)
    match chosen_topic:
        case "operations":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "fractions":
            question, answer, difficulty_weighting = fractions_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "calculus":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "equations":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "expressions":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "sequences":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "basic_shapes":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "three_d_shapes":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "triangles":
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case _:
            question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)

    return chosen_topic, question, answer, difficulty_weighting

def calculate_difficulty(difficulty_factors : dict):
    summed_difficulty = 0
    for factor in difficulty_factors.values():
        summed_difficulty += (factor[0] * (factor[1]/0.125))
    summed_difficulty = summed_difficulty / 2
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

def answer_generation(real_answer : int, question_type : str, difficulty_factors : dict):
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

# Difficulty weighting includes maths topic, type of question, difficulty of values used, similarity of potential answers,
# ambiguity of how to answer question, conceptual depth (needs fourmulae?), number of steps required, abstract vs concrete, time pressure, images
# Type of question: Free text -> multiple-choice -> true/false
# Topic: Calculus -> Trigonometry -> Quadratic questions -> Sequences -> Linear equations -> 3d shapes -> 2d shapes -> fractions and decimals -> operations
# Similarity of answers: How close answers are in MCQs, how close incorrect is to correct in true/false
# Difficulty of values used: How big values used are, whether final answer is whole number

def operations_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question_type_chosen = random.choice(question_types)
    have_division_chance = random.random()
    difficulty_weighting = 0
    question = ""
    numbers = []
    answers = []
    answer = 0

    while True:
        difficulty_factors["maths_topic"][0] = 0
        difficulty_factors["difficulty_of_values"][0] = 2
        difficulty_factors["depth_of_knowledge"][0] = 2
        difficulty_factors["multiple_topics"][0] = 3
        difficulty_factors["difficulty_of_answer"][0] = 2
        difficulty_factors["number_of_steps"][0] = 2

        number_of_values = random.randint(2, 4)
        if have_division_chance > 0.7:
            operations = [random.choice(["+", "-", "*", "/"]) for x in range(number_of_values - 1)]
        else:
            operations = [random.choice(["+", "-", "*"]) for x in range(number_of_values - 1)]

        numbers = [random.randint(1, 200) for x in range(number_of_values)]
        question = ""
        for x in range(0, len(numbers)):
            question += str(numbers[x])
            if x < len(numbers) - 1:
                question += operations[x]
        answer = eval(question)
        if have_division_chance <= 0.7 or (
                have_division_chance > 0.7 and question.find("/") != -1 and answer.is_integer()):
            answer = int(answer)
            for x in range(number_of_values - 1):
                difficulty_factors["number_of_steps"][0] += 2
            if ("-" in operations or "+" in operations) and ("/" in operations or "*" in operations):
                difficulty_factors["depth_of_knowledge"][0] += 2
            for operation in set(operations):
                match operation:
                    case "+":
                        difficulty_factors["maths_topic"][0] += 1
                    case "-":
                        difficulty_factors["maths_topic"][0] += 2
                    case "*":
                        difficulty_factors["maths_topic"][0] += 3
                    case "/":
                        difficulty_factors["maths_topic"][0] += 4

            for value in numbers:
                if value == 1:
                    difficulty_factors["difficulty_of_values"][0] //= 2
                if value == 2 or value == 10:
                    pass
                elif value % 5 == 0 or value % 10 == 0:
                    difficulty_factors["difficulty_of_values"][0] += 0.5
                else:
                    if 10 < value <= 30:
                        difficulty_factors["difficulty_of_values"][0] += 1
                    elif 30 < value <= 80:
                        difficulty_factors["difficulty_of_values"][0] += 1.5
                    elif 80 < value <= 150:
                        difficulty_factors["difficulty_of_values"][0] += 2
                    else:
                        difficulty_factors["difficulty_of_values"][0] += 3
            if answer > 100:
                difficulty_factors["difficulty_of_answer"][0] += 3
            elif answer > 500:
                difficulty_factors["difficulty_of_answer"][0] += 4
            elif answer > 1000:
                difficulty_factors["difficulty_of_answer"][0] += 5
            elif answer > 5000:
                difficulty_factors["difficulty_of_answer"][0] += 6

            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

            if final_difficulty == entered_difficulty and answers[0] <= 10000:
                print(difficulty_factors)
                print(difficulty_weighting)
                break
        else:
            pass

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

# Fraction conversion, fraction operations, algebraic fractions, surds


def fractions_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question_type_chosen = random.choice(question_types)
    # fractions_topic = random.choice(["conversion", "operations", "algebra", "surds"])
    is_division = random.random()
    fractions_topic = "algebra"
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    difficulty_factors["maths_topic"][0] = 2
    difficulty_factors["difficulty_of_values"][0] = 2
    difficulty_factors["depth_of_knowledge"][0] = 2
    difficulty_factors["multiple_topics"][0] = 3
    difficulty_factors["difficulty_of_answer"][0] = 3
    difficulty_factors["number_of_steps"][0] = 2
    answer = ""
    question = ""
    answers = []
    difficulty_weighting = 0

    while True:
        fractions_topic = random.choice(["conversion", "operations", "algebra", "surds"])
        match fractions_topic:
            case "conversion":
                convert = random.choice(["/ to .", "/ to %", "% to .", "% to /", ". to %"])
                fraction_value = f"{num1}/{num2}"
                decimal_value = num1 / num2
                percentage_value = (num1 / num2) * 100
                convert = random.choice(["/ to .", "/ to %", "% to .", "% to /", ". to %"])
                match convert:
                    case "/ to .":
                        pass
                    case _:
                        pass
            case "operations":
                is_valid = True

                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 2

                numerators = [random.randint(1, 20) for x in range(2)]
                denominators = [random.randint(1, 20) for x in range(2)]
                if is_division > 0.75:
                    operation = "/"
                else:
                    operation = random.choice(["+", "-", "*"])

                new_numerators = []
                new_denominators = []

                question = f"What is {numerators[0]}/{denominators[0]} {operation} {numerators[1]}/{denominators[1]}?"

                match operation:
                    case "+":
                        difficulty_factors["maths_topic"][0] += 1
                        if denominators[0] != denominators[1]:
                            difficulty_factors["number_of_steps"][0] += 3
                            difficulty_factors["difficulty_of_values"][0] += 1
                        final_denominator = lcm(denominators[0], denominators[1])

                        for x in range(2):
                            new_numerators.append(int(numerators[x] * (final_denominator / denominators[x])))
                            new_denominators.append(int(final_denominator))
                        if final_denominator > 50:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif final_denominator > 100:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        elif final_denominator > 200:
                            difficulty_factors["difficulty_of_values"][0] += 3
                        if new_numerators[0] <= 10 or new_denominators[1] <= 10:
                            pass
                        elif 10 < new_numerators[0] <= 50 or 10 < new_numerators[1] <= 50:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 50 < new_numerators[0] <= 100 or 50 < new_numerators[1] <= 100:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        elif 100 < new_numerators[0] <= 200 or 100 < new_numerators[1] <= 200:
                            difficulty_factors["difficulty_of_values"][0] += 3
                        else:
                            difficulty_factors["difficulty_of_values"][0] += 4

                        final_numerator = sum(new_numerators)
                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "-":
                        difficulty_factors["maths_topic"][0] += 1
                        if denominators[0] != denominators[1]:
                            difficulty_factors["number_of_steps"][0] += 3
                            difficulty_factors["difficulty_of_values"][0] += 1
                        final_denominator = lcm(denominators[0], denominators[1])
                        for x in range(2):
                            new_numerators.append(int(numerators[x] * (final_denominator / denominators[x])))
                            new_denominators.append(int(final_denominator))

                        if final_denominator > 50:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif final_denominator > 100:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        elif final_denominator > 200:
                            difficulty_factors["difficulty_of_values"][0] += 3
                        if new_numerators[0] <= 10 or new_denominators[1] <= 10:
                            pass
                        elif 10 < new_numerators[0] <= 50 or 10 < new_numerators[1] <= 50:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 50 < new_numerators[0] <= 100 or 50 < new_numerators[1] <= 100:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        elif 100 < new_numerators[0] <= 200 or 100 < new_numerators[1] <= 200:
                            difficulty_factors["difficulty_of_values"][0] += 3
                        else:
                            difficulty_factors["difficulty_of_values"][0] += 4

                        final_numerator = new_numerators[0] - new_numerators[1]
                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "*":
                        difficulty_factors["maths_topic"][0] += 2
                        difficulty_factors["number_of_steps"][0] += 2
                        final_numerator = int(numerators[0] * numerators[1])
                        final_denominator = int(denominators[0] * denominators[1])

                        if numerators[0] == 1 or numerators[1] == 1:
                            pass
                        elif numerators[0] == 2 or numerators[0] == 10 or numerators[1] == 2 or numerators[1] == 10:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 2 < numerators[0] <= 10 or 2 < numerators[1] <= 10:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        elif 10 < numerators[0] <= 20 or 10 < numerators[1] <= 20:
                            difficulty_factors["difficulty_of_values"][0] += 3

                        if denominators[0] == 1 or denominators[1] == 1:
                            pass
                        elif denominators[0] == 2 or numerators[0] == 10 or denominators[1] == 2 or denominators[1] == 10:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 2 < denominators[0] <= 10 or 2 < denominators[1] <= 10:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        elif 10 < denominators[0] <= 20 or 10 < denominators[1] <= 20:
                            difficulty_factors["difficulty_of_values"][0] += 3

                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "/":
                        difficulty_factors["maths_topic"][0] += 2
                        difficulty_factors["depth_of_knowledge"][0] += 2
                        difficulty_factors["number_of_steps"][0] += 2
                        final_numerator = numerators[0] / numerators[1]
                        final_denominator = denominators[0] / denominators[1]
                        if final_numerator.is_integer() and final_denominator.is_integer():

                            if numerators[0] == 1 or numerators[1] == 1:
                                pass
                            elif numerators[0] == 2 or numerators[0] == 10 or numerators[1] == 2 or numerators[1] == 10:
                                difficulty_factors["difficulty_of_values"][0] += 1
                            elif 2 < numerators[0] <= 10 or 2 < numerators[1] <= 10:
                                difficulty_factors["difficulty_of_values"][0] += 2
                            elif 10 < numerators[0] <= 20 or 10 < numerators[1] <= 20:
                                difficulty_factors["difficulty_of_values"][0] += 3

                            if denominators[0] == 1 or denominators[1] == 1:
                                pass
                            elif denominators[0] == 2 or numerators[0] == 10 or denominators[1] == 2 or denominators[1] == 10:
                                difficulty_factors["difficulty_of_values"][0] += 1
                            elif 2 < denominators[0] <= 10 or 2 < denominators[1] <= 10:
                                difficulty_factors["difficulty_of_values"][0] += 2
                            elif 10 < denominators[0] <= 20 or 10 < denominators[1] <= 20:
                                difficulty_factors["difficulty_of_values"][0] += 3

                            hcf = gcd(int(final_numerator), int(final_denominator))
                            final_numerator = int(final_numerator / hcf)
                            final_denominator = int(final_denominator / hcf)
                            answer = f"{final_numerator}/{final_denominator}"
                        else:
                            is_valid = False
                if is_valid:
                    answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen, difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

                    if final_difficulty == entered_difficulty:
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break

            case "algebra":
                difficulty_factors["maths_topic"][0] = 6
                difficulty_factors["difficulty_of_values"][0] = 6
                difficulty_factors["depth_of_knowledge"][0] = 6
                difficulty_factors["multiple_topics"][0] = 6
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 7

                x = symbols("x")
                common_factor = random.randint(1, 3)
                quadratic_value_numerator, linear_value_numerator, number_value_numerator = generate_expression(random.choice([True, False]), random.choice([True, False]), random.choice([True, False]))
                quadratic_value_denominator, linear_value_denominator, number_value_denominator = generate_expression(random.choice([True, False]), random.choice([True, False]), random.choice([True, False]))
                if quadratic_value_numerator == 0 or linear_value_numerator == 0:
                    pass
                elif quadratic_value_denominator == 0 or linear_value_denominator == 0:
                    pass
                else:
                    numerator = common_factor * random.randint(1, 3) * (
                                quadratic_value_numerator + linear_value_numerator + number_value_numerator)
                    denominator = common_factor * random.randint(1, 3) * (
                            quadratic_value_denominator + linear_value_denominator + number_value_denominator)
                    question = f"{numerator}/{denominator}"
                    print(type(numerator))
                    print(type(denominator))
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
                    if quadratic_value_numerator != 0 and numerator_terms[0].coeff(x, numerator.as_ordered_terms()[0].as_poly().degree()) > 1:
                        difficulty_factors["difficulty_of_values"][0] += 0.5
                    if quadratic_value_denominator != 0 and denominator_terms[0].coeff(x, denominator.as_ordered_terms()[0].as_poly().degree()) > 1:
                        difficulty_factors["difficulty_of_values"][0] += 0.5
                    answer = simplify(numerator/denominator)
                    question_type_chosen = "free_text"
                    answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen, difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                    answer = str(answer)

                    if final_difficulty == entered_difficulty:
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break

            case "surds":
                pass
            case _:
                pass

    match question_type_chosen:
        case "free_text":
            question = f"What is {question}?" if not fractions_topic == "algebra" else f"Simplify {question}."
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

# Linear equations, quadratic equations, quadratic formula, completing the square, simultaneous equations, quadratic simultaneous equations, inequalities, quadratic inequalities
def equations_question_generation():
    pass

# Expression simplification, factorisation, algebraic fractions
def expressions_question_generation():
    pass

# Linear, quadratic, geometric sequences
def sequences_question_generation():
    pass

def hcf_lcm_prime_factors():
    pass

# Compound interest, regular interest, reverse percentages, numbers as percentages
def percentages_question_generation():
    pass

def probability_question_generation():
    pass

def calculus_question_generation():
    pass

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

# fractions_question_generation(2, ["free_text", "multiple-choice", "true/false"], difficulty_factors)