import random

from .helper_functions import answer_generation, calculate_difficulty

# BIDMAS
def operations_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    have_division_chance = random.random()
    difficulty_weighting = 0
    question = ""
    numbers = []
    answers = []
    answer = 0

    while True:
        time_needed = 60
        question_type_chosen = random.choice(question_types)
        difficulty_factors["maths_topic"][0] = 0
        difficulty_factors["difficulty_of_values"][0] = 1
        difficulty_factors["depth_of_knowledge"][0] = 1
        difficulty_factors["multiple_topics"][0] = 0
        difficulty_factors["difficulty_of_answer"][0] = 1
        difficulty_factors["number_of_steps"][0] = 1

        number_of_values = random.randint(2, 4)
        if have_division_chance > 0.7:
            operations = [random.choice(["+", "-", "*", "/"]) for x in range(number_of_values - 1)]
        else:
            operations = [random.choice(["+", "-", "*"]) for x in range(number_of_values - 1)]

        numbers = random.sample(range(1, 50), number_of_values) # Chooses series of unique numbers from 1 - 50
        question = ""
        for x in range(0, len(numbers)):
            question += str(numbers[x])
            if x < len(numbers) - 1:
                question += operations[x]
        if number_of_values > 2 and ("/" in question or "*" in question) and ("-" in question or "+" in question):
            left_bracket_added = False
            right_bracket_added = False
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
        for x in range(len(question)):
            if random.random() > 0.5 and question[x].isnumeric() and (x == 0 or (not question[x-1].isnumeric() and not question[x-1] == "*")) \
                    and (x == len(question) - 1 or (not question[x+1].isnumeric() and not question[x+1] == "*")):
                question = f"{question[0:x+1]}**2{question[x+1:]}"
        try:
            answer = eval(question)
        except ZeroDivisionError:
            answer = 20000
        if have_division_chance <= 0.7 or (
                have_division_chance > 0.7 and question.find("/") != -1 and answer.is_integer()):
            answer = int(answer)
            for x in range(number_of_values - 1):
                difficulty_factors["number_of_steps"][0] += 1
            if ("-" in operations or "+" in operations) and ("/" in operations or "*" in operations):
                difficulty_factors["depth_of_knowledge"][0] += 2
                difficulty_factors["multiple_topics"][0] += 2
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
            if "**" in question:
                difficulty_factors["maths_topic"][0] += 2
                difficulty_factors["depth_of_knowledge"][0] += 1
                difficulty_factors["multiple_topics"][0] += 1
            if "(" in question:
                difficulty_factors["maths_topic"][0] += 1
                difficulty_factors["depth_of_knowledge"][0] += 1
                difficulty_factors["multiple_topics"][0] += 1

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
            if answer > 100:
                difficulty_factors["difficulty_of_answer"][0] += 1
            elif answer > 500:
                difficulty_factors["difficulty_of_answer"][0] += 1.5
            elif answer > 1000:
                difficulty_factors["difficulty_of_answer"][0] += 2
            elif answer > 5000:
                difficulty_factors["difficulty_of_answer"][0] += 2.5

            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

            if final_difficulty == entered_difficulty and -10000 <= answers[0] <= 10000 and "*1" not in question and "1*" not in question and "/1" not in question:
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

    if type(answer) == int and abs(answer) > 1000:
        time_needed = 120

    return question, answer, difficulty_weighting, time_needed

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

# operations_question_generation(5, ["free_text", "multiple-choice", "true/false"], difficulty_factors)
