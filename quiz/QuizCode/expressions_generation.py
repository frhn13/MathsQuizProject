import random
from sympy import simplify, factor, expand, symbols

from .helper_functions import (generate_expression, generate_complex_expression, answer_generation_fractions,
                               answer_generation, calculate_difficulty, algebraic_fractions, factorisation_and_simplification)

# Expression simplification, factorisation, algebraic fractions
def expressions_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question_type_chosen = random.choice(["free-text"])
    while True:
        x = symbols("x")
        expressions_topic = random.choice(["simplification", "factorisation", "algebraic_fractions"])
        # expressions_topic = "algebraic_fractions"
        match expressions_topic:
            case "simplification":
                difficulty_factors, expression = factorisation_and_simplification(difficulty_factors)
                factorised = factor(expression)

                expression_str = str(factorised)

                for x in range(len(expression_str)):
                    if x < len(expression_str) - 1 and expression_str[x] == "*" and expression_str[x + 1] == "*":
                        expression_str = f"{expression_str[0:x]}^{expression_str[x + 2:]}"
                    elif x < len(expression_str) - 1 and expression_str[x] == "*":
                        expression_str = f"{expression_str[0:x]}{expression_str[x + 1:]}"

                question = f"Expand {expression_str}."
                answer = expression
                if expression is None or expression == factorised:
                    pass
                else:
                    answers, difficulty_factors = answer_generation(answer, question_type_chosen,
                                                                    difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

                    if final_difficulty == entered_difficulty:
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break
            case "factorisation":
                difficulty_factors, expression = factorisation_and_simplification(difficulty_factors)

                expression_str = str(expression)

                for x in range(len(expression_str)):
                    if x < len(expression_str) - 1 and expression_str[x] == "*" and expression_str[x + 1] == "*":
                        expression_str = f"{expression_str[0:x]}^{expression_str[x + 2:]}"
                    elif x < len(expression_str) - 1 and expression_str[x] == "*":
                        expression_str = f"{expression_str[0:x]}{expression_str[x + 1:]}"

                question = f"Factorise {expression_str}."
                answer = factor(expression)
                if expression is None or expression == answer:
                    pass
                else:
                    answers, difficulty_factors = answer_generation(answer, question_type_chosen,
                                                                              difficulty_factors)
                    difficulty_factors["question_type"][0] = 8
                    difficulty_factors["answers_similarity"][0] = 8
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

                    if final_difficulty == entered_difficulty:
                        print(difficulty_factors)
                        print(difficulty_weighting)
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
