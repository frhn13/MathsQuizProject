import random
from sympy import simplify, factor, expand, symbols

from .helper_functions import generate_expression, generate_complex_expression, answer_generation_fractions, answer_generation, calculate_difficulty, algebraic_fractions

# Expression simplification, factorisation, algebraic fractions
def expressions_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question_type_chosen = random.choice(["free-text"])
    while True:
        x = symbols("x")
        expressions_topic = random.choice(["simplification", "factorisation", "algebraic_fractions", "collecting_like_terms"])
        # expressions_topic = "algebraic_fractions"
        match expressions_topic:
            case "simplification":
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 5
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
                        if quadratic_value != 0:
                            difficulty_factors["difficulty_of_values"][0] += 1
                            difficulty_factors["difficulty_of_answer"][0] += 1
                            difficulty_factors["number_of_steps"][0] += 1
                        if quadratic_value < 0:
                            difficulty_factors["difficulty_of_values"][0] += 1
                            difficulty_factors["difficulty_of_answer"][0] += 1
                else:
                    expression = generate_complex_expression()

                factorised = factor(expression)
                question = f"Expand {factorised}."
                answer = expression
                if expression is None or expression == factorised:
                    pass
                else:
                    answers, difficulty_factors = answer_generation(answer, question_type_chosen,
                                                                    difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                    if final_difficulty == entered_difficulty:
                        break
            case "factorisation":
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 5
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
                        if quadratic_value != 0:
                            difficulty_factors["difficulty_of_values"][0] += 1
                            difficulty_factors["difficulty_of_answer"][0] += 1
                            difficulty_factors["number_of_steps"][0] += 1
                        if quadratic_value < 0:
                            difficulty_factors["difficulty_of_values"][0] += 1
                            difficulty_factors["difficulty_of_answer"][0] += 1
                else:
                    expression = generate_complex_expression()

                question = f"Factorise {expression}."
                answer = factor(expression)
                if expression is None or expression == answer:
                    pass
                else:
                    answers, difficulty_factors = answer_generation(answer, question_type_chosen,
                                                                              difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

                    if final_difficulty == entered_difficulty:
                        break

            case "algebraic_fractions":
                question, answer, question_type_chosen = algebraic_fractions(difficulty_factors)
                answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen,
                                                                          difficulty_factors)
                difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                answer = str(answer)

                if question is not None and answer is not None and final_difficulty == entered_difficulty:
                    print(difficulty_factors)
                    print(difficulty_weighting)
                    break

            case _:
                pass

    match question_type_chosen:
        case "free_text":
            question = question
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
    answer = str(answer)

    return question, answer, difficulty_weighting
