import random
from .helper_functions import generate_equation, answer_generation_equations, calculate_difficulty

# Linear equations, quadratic equations, quadratic formula, completing the square, simultaneous equations, quadratic simultaneous equations, inequalities, quadratic inequalities
def equations_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question_type_chosen = random.choice(question_types)
    question_type_chosen = "free_text"
    question = ""
    answer = []
    answers = []
    multiple_answers = "No"
    while True:
        equation_type = random.choice(["linear", "whole_quadratic", "floating_quadratic", "linear_simultaneous"])
        if entered_difficulty >= 4:
            equation_type = "quadratic_simultaneous"

        equation, final_answer = generate_equation(equation_type, difficulty_factors)
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 8
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors=difficulty_factors)
        #print(f"Answers in function: {final_answer}")
        #print(f"Difficulty: {final_difficulty}")
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