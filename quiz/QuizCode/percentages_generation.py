import random

from .helper_functions import answer_generation, calculate_difficulty, answer_generation_decimals

# Compound interest, regular interest, reverse percentages, numbers as percentages, percentages of amounts
def percentages_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    answer = 0
    question = ""
    percentage_in_answer = True
    final_difficulty = 0
    while True:
        percentage_topic_chosen = random.choice(["amount_from_percentage", "percentage_from_amount", "compound_interest", "reverse_percentages"])
        question_type_chosen = random.choice(question_types)
        difficulty_factors["maths_topic"][0] = 0
        difficulty_factors["difficulty_of_values"][0] = 0
        difficulty_factors["depth_of_knowledge"][0] = 0
        difficulty_factors["multiple_topics"][0] = 0
        difficulty_factors["difficulty_of_answer"][0] = 0
        difficulty_factors["number_of_steps"][0] = 0

        match percentage_topic_chosen:
            case "reverse_percentages":
                difficulty_factors["maths_topic"][0] = 5
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 4
                answer = random.randint(50, 200)
                if random.random() > 0.5:
                    percentage = random.randint(80, 95)
                    final_amount = answer * (percentage / 100)
                    question = f"The sale price of an item is £{round(final_amount, 2)} when it is {100-percentage}% off, what is the original price?"
                else:
                    percentage = random.randint(5, 20)
                    final_amount = answer * (1 + percentage / 100)
                    question = f"The new price of an item is £{round(final_amount, 2)} when it has been increased by {percentage}%, what is the original price?"
                percentage_in_answer = False

            case "compound_interest":
                difficulty_factors["maths_topic"][0] = 5
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 5
                starting_amount = random.randint(2000, 5000)
                number_of_intervals = random.randint(2, 10)
                percentage_in_answer = False
                if 0 < random.random() < 0.25:
                    interest = 1 + (random.randint(2, 10) / 100)
                    answer = round(starting_amount * (interest ** number_of_intervals), 2)
                    question = (f"If you invest £{starting_amount} into a savings account with a {int((interest - 1)*100)}% interest rate per year."
                                f" Then how much money do you have after {number_of_intervals} years?")
                elif 0.25 <= random.random() < 0.5:
                    difficulty_factors["depth_of_knowledge"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["number_of_steps"][0] += 1
                    interest = 1 + (random.randint(2, 10) / 100)
                    final_amount = round(starting_amount * (interest ** number_of_intervals), 2)
                    answer = number_of_intervals
                    question = (
                        f"If you invest £{starting_amount} into a savings account for n years with a {int((interest - 1) * 100)}% interest rate per year and end up with £{final_amount}."
                        f" Then what is the value of n?")
                elif 0.5 <= random.random() < 0.75:
                    interest = 1 - (random.randint(2, 10) / 100)
                    answer = round(starting_amount * (interest ** number_of_intervals), 2)
                    question = (
                        f"If you buy a car for £{starting_amount} and it depreciates {int((1 - interest) * 100)}% per year."
                        f" Then how much money is it worth after {number_of_intervals} years?")
                else:
                    difficulty_factors["depth_of_knowledge"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["number_of_steps"][0] += 1
                    interest = 1 - (random.randint(2, 10) / 100)
                    final_amount = round(starting_amount * (interest ** number_of_intervals), 2)
                    answer = number_of_intervals
                    question = (
                        f"If you bought a car n years ago for £{starting_amount} and it depreciates {int((1 - interest) * 100)}% per year and is now worth £{final_amount}."
                        f" Then what is the value of n?")

            case "amount_from_percentage":
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 2
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3

                percentage = round((random.randint(1, 100) / 100), 2)
                if not percentage == round(percentage, 1):
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["number_of_steps"][0] += 1
                num1 = random.randint(1, 200)
                answer = num1 * percentage

                if answer == int(answer):
                    answer = int(answer)
                question = f"What is {percentage*100}% of {num1}?"
                percentage_in_answer = False

            case "percentage_from_amount":
                difficulty_factors["maths_topic"][0] = 4
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 2
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3

                percentage = round((random.randint(1, 99) / 100), 2)
                if not percentage == round(percentage, 1):
                    difficulty_factors["difficulty_of_values"][0] += 1
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["number_of_steps"][0] += 1
                num1 = random.randint(1, 200)
                num2 = num1 * percentage

                if num2 == int(num2):
                    num2 = int(num2)
                    answer = int(percentage * 100)
                question = f"What is {num2} as a percentage of {num1}?"
                percentage_in_answer = True
            case _:
                pass

        if ((percentage_topic_chosen == "compound_interest" and type(answer) == int) or
                percentage_topic_chosen == "reverse_percentages" or (percentage_topic_chosen == "amount_from_percentage" and type(answer) == int) or
                (percentage_topic_chosen == "percentage_from_amount" and type(num2) == int)):
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        elif percentage_topic_chosen == "compound_interest" and type(answer) == float:
            answers, difficulty_factors = answer_generation_decimals(answer, question_type_chosen, difficulty_factors)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        if final_difficulty == entered_difficulty:
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    match question_type_chosen:
        case "free_text":
            question = question
        case "multiple-choice":
            question = f"{question}\nIs it {answers[0]}%, {answers[1]}%, {answers[2]}% or {answers[3]}%?" \
                if percentage_in_answer else f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            question = f"{question}\nIs the answer {answers[0]}%, answer with True or False." \
                if percentage_in_answer else f"{question}\nIs the answer {answers[0]}, answer with True or False."
            if answers[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting
