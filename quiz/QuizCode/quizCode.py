import random
# Difficulty weighting includes maths topic, type of question, difficulty of values used, similarity of potential answers,
# ambiguity of how to answer question, conceptual depth (needs fourmulae?), number of steps required, abstract vs concrete, time pressure, images
# Type of question: Free text -> multiple-choice -> true/false
# Topic: Calculus -> Trigonometry -> Quadratic questions -> Sequences -> Linear equations -> 3d shapes -> 2d shapes -> fractions and decimals -> operations
# Similarity of answers: How close answers are in MCQs, how close incorrect is to correct in true/false
# Difficulty of values used: How big values used are, whether final answer is whole number

def calculate_difficulty(difficulty_factors : dict):
    summed_difficulty = 0
    for factor in difficulty_factors.values():
        summed_difficulty += (factor[0] * (factor[1]/0.125))
    summed_difficulty = summed_difficulty / 2
    return summed_difficulty / 8, summed_difficulty // 8

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
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "decimals":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "calculus":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "equations":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "expressions":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "sequences":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "basic_shapes":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "three_d_shapes":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "triangles":
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case _:
            numbers, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)

    return numbers, question, answer, difficulty_weighting

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
        answers = [random.randint(real_answer - 20, real_answer + 20)]
        if abs(answers[0] - real_answer) >= 10:
            difficulty_factors["answers_similarity"][0] -= 2

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

    x = 0
    while x < 10:
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
                if value == 1 or value == 2 or value == 10:
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
                difficulty_factors["difficulty_of_answer"][0] += 2
            elif answer > 500:
                difficulty_factors["difficulty_of_answer"][0] += 3
            elif answer > 1000:
                difficulty_factors["difficulty_of_answer"][0] += 4
            elif answer > 5000:
                difficulty_factors["difficulty_of_answer"][0] += 5
            elif answer > 100000:
                difficulty_factors["difficulty_of_answer"][0] += 6
            elif answer > 1000000:
                difficulty_factors["difficulty_of_answer"][0] += 8

            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
            difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

            x += 1
            if final_difficulty == entered_difficulty:
                print(difficulty_factors)
                print(difficulty_weighting)
                break
        else:
            pass

    match question_type_chosen:
        case "free_text":
            pass
        case "multiple-choice":
            question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            question = f"{question}\nIs the answer {answers[0]}, answer with True or False"
            if answers[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return numbers, question, answer, difficulty_weighting

def decimals_question_generation():
    pass

def calculus_question_generation():
    pass

def equations_question_generation():
    pass

def expressions_question_generation():
    pass

def sequences_question_generation():
    pass

def basic_shapes_question_generation():
    pass

def three_d_shapes_question_generation():
    pass

def triangles_question_generation():
    pass

