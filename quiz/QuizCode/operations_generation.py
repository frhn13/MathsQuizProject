import random

from .helper_functions import answer_generation, calculate_difficulty

# BIDMAS
def operations_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    have_division_chance = random.random()

    while True: # Remains True until a valid question is generated with the entered difficulty
        time_needed = 60
        question_type_chosen = random.choice(question_types) # Question type randomly chosen
        difficulty_factors["maths_topic"][0] = 0
        difficulty_factors["difficulty_of_values"][0] = 1
        difficulty_factors["depth_of_knowledge"][0] = 1
        difficulty_factors["multiple_topics"][0] = 0
        difficulty_factors["difficulty_of_answer"][0] = 1
        difficulty_factors["number_of_steps"][0] = 1

        number_of_values = random.randint(2, 4) # Number of values in question randomly chosen
        # Operations between numbers are randomly selected
        if have_division_chance > 0.7: # 30% chance of division being added to calculation
            operations = [random.choice(["+", "-", "*", "/"]) for x in range(number_of_values - 1)]
        else:
            operations = [random.choice(["+", "-", "*"]) for x in range(number_of_values - 1)]

        # Chooses unique numbers from 1 to 50, with the number of numbers depending on the previous variable
        numbers = random.sample(range(1, 50), number_of_values)
        question = ""
        for x in range(0, len(numbers)): # Loops through each number and operation and combines them make the question calculation
            question += str(numbers[x])
            if x < len(numbers) - 1:
                question += operations[x]
        # If multiplication or division and addition or subtraction are both in the question, then brackets are added to increase the complexity
        if number_of_values > 2 and ("/" in question or "*" in question) and ("-" in question or "+" in question):
            left_bracket_added = False
            right_bracket_added = False
            # For loop adds the left bracket before number that is before + or -
            for x in range(len(question)):
                if question[x] == "+" or question[x] == "-":
                    x1 = x - 1
                    while not left_bracket_added:
                        if x1 == 0:
                            question = f"({question}"
                            left_bracket_added = True
                        elif not question[x1].isnumeric():
                            question = f"{question[0:x1+1]}({question[x1+1:]}"
                            left_bracket_added = True
                        else: x1 -= 1
            # For loop adds the right bracket after number that is after + or -, final result could be (32-23)
            for x in range(len(question)):
                if question[x] == "+" or question[x] == "-":
                    x2 = x + 1
                    while not right_bracket_added:
                        if x2 == len(question) - 1:
                            question = f"{question})"
                            right_bracket_added = True
                        elif not question[x2].isnumeric():
                            question = f"{question[0:x2]}){question[x2:]}"
                            right_bracket_added = True
                        else: x2 += 1
        # 50% chance of square a number in the calculation to increase the difficulty
        for x in range(len(question)):
            if random.random() > 0.5 and question[x].isnumeric() and (x == 0 or (not question[x-1].isnumeric() and not question[x-1] == "*")) \
                    and (x == len(question) - 1 or (not question[x+1].isnumeric() and not question[x+1] == "*")):
                question = f"{question[0:x+1]}**2{question[x+1:]}"
        try: # Finds answer for question unless it tries to divide by 0
            answer = eval(question)
        except ZeroDivisionError:
            answer = None # Answer becomes if zero division error, so new question forced to be generated
        if have_division_chance <= 0.7 or ( # If division_chance is more than 0.7, then division should be included in the question, and answer should be a whole number
                have_division_chance > 0.7 and question.find("/") != -1 and answer is not None and answer.is_integer()):
            answer = int(answer)
            for x in range(number_of_values - 1): # Difficulty increases the more numbers there are in the calculation
                difficulty_factors["number_of_steps"][0] += 1
            # Difficulty increases if knowledge of order of operations is needed
            if ("-" in operations or "+" in operations) and ("/" in operations or "*" in operations):
                difficulty_factors["depth_of_knowledge"][0] += 2
                difficulty_factors["multiple_topics"][0] += 2
            # Difficulty increases as more operations are included in question, and if they are more complex
            for operation in set(operations):
                match operation:
                    case "+":
                        difficulty_factors["maths_topic"][0] += 0
                    case "-":
                        difficulty_factors["maths_topic"][0] += 0.5
                    case "*":
                        difficulty_factors["maths_topic"][0] += 1
                    case "/":
                        difficulty_factors["maths_topic"][0] += 1.5
            # Difficulty increases if powers and brackets are in the question
            if "**" in question:
                difficulty_factors["maths_topic"][0] += 2
                difficulty_factors["depth_of_knowledge"][0] += 1
                difficulty_factors["multiple_topics"][0] += 1
            if "(" in question:
                difficulty_factors["maths_topic"][0] += 1
                difficulty_factors["depth_of_knowledge"][0] += 1
                difficulty_factors["multiple_topics"][0] += 1

            # Difficulty increases as the size of the values in the question increases
            for value in numbers:
                if value == 1:
                    difficulty_factors["difficulty_of_values"][0] //= 2
                if value == 2 or value == 10:
                    pass
                elif value % 5 == 0 or value % 10 == 0:
                    pass
                else:
                    if 10 < value <= 20:
                        difficulty_factors["difficulty_of_values"][0] += 0.5
                    elif 20 < value <= 40:
                        difficulty_factors["difficulty_of_values"][0] += 1
                    elif 40 < value <= 50:
                        difficulty_factors["difficulty_of_values"][0] += 1.5
                    else:
                        difficulty_factors["difficulty_of_values"][0] += 2
            # Difficulty increases as the size of the answer increases
            if abs(answer) > 100:
                difficulty_factors["difficulty_of_answer"][0] += 1
            elif abs(answer) > 500:
                difficulty_factors["difficulty_of_answer"][0] += 1.5
            elif abs(answer) > 1000:
                difficulty_factors["difficulty_of_answer"][0] += 2
            elif abs(answer) > 5000:
                difficulty_factors["difficulty_of_answer"][0] += 2.5

            # Generates choices for answers for the question if the question type is multiple-choice or true/false
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors, False)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

            # Breaks out of while loop if difficulty level matches entered difficulty, the answer is less than 1000 and
            # if none of the operations involve multiplying or dividing by one
            if final_difficulty == entered_difficulty and abs(answers[0]) <= 10000 and "*1" not in question and "1*" not in question and "/1" not in question:
                break
        else:
            pass

    question = str(question)

    # Loops through every character in the equation for a question and replaces every ** with ^ to make powers easier to understand
    for x in range(len(question)):
        if x < len(question) - 1 and question[x] == "*" and question[x + 1] == "*":
            question = f"{question[0:x]}^{question[x + 2:]}"

    match question_type_chosen:
        case "free_text":
            question = f"What is {question}?"
        case "multiple-choice":
            # Question changed to display all four potential answers in multiple-choice question
            question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            # Question changed to display all one potential answer in true/false question
            question = f"{question}\nIs the answer {answers[0]}, answer with True or False."
            if answers[0] == answer:
                # Answer changed from number value to True or False in true/false question
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    if type(answer) == int and abs(answer) > 1000: # If answer is more than 1000 then time to answer the question is doubled
        time_needed = 120

    return question, answer, difficulty_weighting, time_needed
