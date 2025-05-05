import random

from .helper_functions import answer_generation, calculate_difficulty, answer_generation_decimals

def percentages_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    answer = 0
    question = ""
    percentage_in_answer = True
    final_difficulty = 0
    while True: # Remains True until a valid question is generated with the entered difficulty
        calculator_needed = False
        time_needed = 60
        # Percentages question subtopic randomly chosen from this list
        percentage_topic_chosen = random.choice(["amount_from_percentage", "percentage_from_amount", "compound_interest", "reverse_percentages"])
        question_type_chosen = random.choice(question_types) # Question type randomly chosen
        difficulty_factors["maths_topic"][0] = 0
        difficulty_factors["difficulty_of_values"][0] = 0
        difficulty_factors["depth_of_knowledge"][0] = 0
        difficulty_factors["multiple_topics"][0] = 0
        difficulty_factors["difficulty_of_answer"][0] = 0
        difficulty_factors["number_of_steps"][0] = 0

        match percentage_topic_chosen:
            case "reverse_percentages":
                # Makes a question where you have to find the original value after a percentage increase or decrease
                calculator_needed = True # Calculator required for question and more time needed to answer it
                time_needed = 120
                difficulty_factors["maths_topic"][0] = 5
                difficulty_factors["difficulty_of_values"][0] = 5
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 5
                difficulty_factors["number_of_steps"][0] = 4
                answer = random.randint(50, 200)
                if random.random() > 0.5:
                    # 50% chance of finding original vale after percentage decrease
                    percentage = random.randint(80, 95)
                    final_amount = answer * (percentage / 100)
                    question = f"The sale price of an item is £{round(final_amount, 2)} when it is {100-percentage}% off, what is the original price?"
                else:
                    # 50% chance of finding original vale after percentage increase
                    percentage = random.randint(5, 20)
                    final_amount = answer * (1 + percentage / 100)
                    question = f"The new price of an item is £{round(final_amount, 2)} when it has been increased by {percentage}%, what is the original price?"
                percentage_in_answer = False

            case "compound_interest":
                # Makes a question where you have to find the new value after the original is increased or decreased through compound interest
                calculator_needed = True # Calculator required for question and more time needed to answer it
                time_needed = 120
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
                    # 25% chance of question where you find new price after compound interest for number of years
                    interest = 1 + (random.randint(2, 10) / 100)
                    answer = round(starting_amount * (interest ** number_of_intervals), 2)
                    question = (f"If you invest £{starting_amount} into a savings account with a {int((interest - 1)*100)}% interest rate per year."
                                f" Then how much money do you have after {number_of_intervals} years?")
                elif 0.25 <= random.random() < 0.5:
                    # 25% chance of question where you find number of years of compound interest it takes to get to new price
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
                    # 25% chance of question where you find new price after compound interest decrease for number of years
                    interest = 1 - (random.randint(2, 10) / 100)
                    answer = round(starting_amount * (interest ** number_of_intervals), 2)
                    question = (
                        f"If you buy a car for £{starting_amount} and it depreciates {int((1 - interest) * 100)}% per year."
                        f" Then how much money is it worth after {number_of_intervals} years?")
                else:
                    # 25% chance of question where you find number of years of compound interest decrease it takes to get to new price
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
                # Generates question where you find the value that is a percentage of another one
                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 2
                difficulty_factors["difficulty_of_answer"][0] = 2
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
                # Generates question where you the percentage that one value is of another one
                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 3
                difficulty_factors["multiple_topics"][0] = 2
                difficulty_factors["difficulty_of_answer"][0] = 2
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

        # Finding percentages and amounts from percentages must have whole number answers
        if ((percentage_topic_chosen == "compound_interest" and type(answer) == int) or
                percentage_topic_chosen == "reverse_percentages" or
                (percentage_topic_chosen == "amount_from_percentage" and type(answer) == int and percentage != 1) or
                (percentage_topic_chosen == "percentage_from_amount" and type(num2) == int and num1 != 100)):
            # Generates choices for answers for the question if the question type is multiple-choice or true/false
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors, True)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

        # Compound interest questions can have decimal answers
        elif percentage_topic_chosen == "compound_interest" and type(answer) == float:
            # Generates choices for answers for the question if the question type is multiple-choice or true/false
            answers, difficulty_factors = answer_generation_decimals(answer, question_type_chosen, difficulty_factors, True)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

        if final_difficulty == entered_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    match question_type_chosen:
        case "free_text":
            question = question
        case "multiple-choice":
            # Question changed to display all four potential answers in multiple-choice question
            question = f"{question}\nIs it {answers[0]}%, {answers[1]}%, {answers[2]}% or {answers[3]}%?" \
                if percentage_in_answer else f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            # Question changed to display all one potential answer in true/false question
            question = f"{question}\nIs the answer {answers[0]}%, answer with True or False." \
                if percentage_in_answer else f"{question}\nIs the answer {answers[0]}, answer with True or False."
            if answers[0] == answer:
                # Answer changed from number value to True or False in true/false question
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting, calculator_needed, time_needed
