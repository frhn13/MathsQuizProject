import random
from sympy import factor, symbols

from .helper_functions import calculate_difficulty, algebraic_fractions, factorisation_and_simplification

def expressions_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    while True: # Remains True until a valid question is generated with the entered difficulty
        time_needed = 60
        x = symbols("x")
        # Expressions question subtopic is randomly chosen from this list
        expressions_topic = random.choice(["simplification", "factorisation", "algebraic_fractions"])
        match expressions_topic:
            case "simplification":
                # Calls function to make expression
                difficulty_factors, expression = factorisation_and_simplification(difficulty_factors)
                factorised = factor(expression) # Factorises expression for question

                expression_str = str(factorised)

                # Loops through every character in the equation for a question and replaces "2*x"
                # with "2x" and "x**2" with "x^2" to make the question more readable for the user
                for x in range(len(expression_str)):
                    if x < len(expression_str) - 1 and expression_str[x] == "*" and expression_str[x + 1] == "*":
                        expression_str = f"{expression_str[0:x]}^{expression_str[x + 2:]}"
                    elif x < len(expression_str) - 1 and expression_str[x] == "*":
                        expression_str = f"{expression_str[0:x]}{expression_str[x + 1:]}"

                question = f"Expand {expression_str}."
                answer = expression
                # If factorised and expanded expressions are the same then question is not generated
                if expression is None or expression == factorised:
                    pass
                else:
                    difficulty_factors["question_type"][0] = 5
                    difficulty_factors["answers_similarity"][0] = 5
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

                    if final_difficulty == entered_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break
            case "factorisation":
                # Calls function to make expression
                difficulty_factors, expression = factorisation_and_simplification(difficulty_factors)

                expression_str = str(expression)

                # Loops through every character in the equation for a question and replaces "2*x"
                # with "2x" and "x**2" with "x^2" to make the question more readable for the user
                for x in range(len(expression_str)):
                    if x < len(expression_str) - 1 and expression_str[x] == "*" and expression_str[x + 1] == "*":
                        expression_str = f"{expression_str[0:x]}^{expression_str[x + 2:]}"
                    elif x < len(expression_str) - 1 and expression_str[x] == "*":
                        expression_str = f"{expression_str[0:x]}{expression_str[x + 1:]}"

                question = f"Factorise {expression_str}."
                answer = factor(expression)
                # If factorised and expanded expressions are the same then question is not generated
                if expression is None or expression == answer:
                    pass
                else:
                    difficulty_factors["question_type"][0] = 5
                    difficulty_factors["answers_similarity"][0] = 5
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

                    if final_difficulty == entered_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break

            case "algebraic_fractions":
                time_needed = 120 # Needs more time to answer this question than other subtopics
                # Calls function to make algebraic fraction expression
                question, answer, question_type_chosen = algebraic_fractions(difficulty_factors)
                difficulty_factors["question_type"][0] = 6
                difficulty_factors["answers_similarity"][0] = 6
                difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question
                answer = str(answer)

                # Breaks out of while loop if difficulty level matches entered difficulty
                if question is not None and answer is not None and final_difficulty == entered_difficulty:
                    print(difficulty_factors)
                    print(difficulty_weighting)
                    break

            case _:
                pass

    answer = str(answer)

    new_question = ""
    for x in range(len(question)): # Replaces 1x or 1y in question with x or y
        if question[x] == "1" and x + 1 < len(question) and (question[x + 1] == "x" or question[x + 1] == "y"):
            pass
        else:
            new_question += question[x]

    return new_question, answer, difficulty_weighting, time_needed
