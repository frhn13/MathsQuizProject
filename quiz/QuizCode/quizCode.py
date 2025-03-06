import random
# Difficulty weighting includes maths topic, type of question, difficulty of values used, similarity of potential answers,
# ambiguity of how to answer question, conceptual depth (needs fourmulae?), number of steps required, abstract vs concrete, time pressure, images
# Type of question: Free text -> multiple-choice -> true/false
# Topic: Calculus -> Trigonometry -> Quadratic questions -> Sequences -> Linear equations -> 3d shapes -> 2d shapes -> fractions and decimals -> operations
# Similarity of answers: How close answers are in MCQs, how close incorrect is to correct in true/false
# Difficulty of values used: How big values used are, whether final answer is whole number

maths_topic = 0
question_type = 0
answers_similarity = 0
difficulty_of_values = 0
number_of_steps = 0
depth_of_knowledge = 0
abstract_vs_concrete = 0
multiple_concepts = 0

def calculate_difficulty(difficulty_factors : dict):
    summed_difficulty = 0
    for factor in difficulty_factors.values():
        summed_difficulty += (factor[0] * factor[1])
    return summed_difficulty / 5, summed_difficulty // 5

def question_topic_selection(selected_topics : list, entered_difficulty : int, question_types : list):
    difficulty_factors = {
        "maths_topic": [0, 0.2],
        "question_type": [0, 0.1],
        "answers_similarity": [0, 0.2],
        "difficulty_of_values": [0, 0.2],
        "number_of_steps": [0, 0.1],
        "depth_of_knowledge": [0, 0.05],
        "abstract_vs_concrete": [0, 0.05],
        "multiple_concepts": [0, 0.1]
    }
    chosen_topic = random.choice(selected_topics)
    match chosen_topic:
        case "operations":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "decimals":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "calculus":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "equations":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "expressions":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "sequences":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "basic_shapes":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "three_d_shapes":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case "triangles":
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)
        case _:
            num1, num2, question, answer, difficulty_weighting = operations_question_generation(entered_difficulty, question_types, difficulty_factors)

    return num1, num2, question, answer, difficulty_weighting

def answer_generation(real_answer : int, question_type : str, difficulty_factors : dict):
    answers = []
    if question_type == "free_text":
        difficulty_factors["question_type"][0] = 8
        difficulty_factors["answers_similarity"][0] = 10
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
# ambiguity of how to answer question, conceptual depth (needs fourmulae?), number of steps required, abstract vs concrete, distractors
def operations_question_generation(entered_difficulty : int, question_types : list, difficulty_factors : dict):
    difficulty_factors["maths_topic"][0] = 2
    question_type_chosen = random.choice(question_types)
    while True:
        operation = random.choice(["add", "sub", "mul", "div"])
        number_of_values = random.randint(2, 5)
        operations = []
        numbers = []
        for i in range(0, number_of_values-1):
            operations.append(random.choice(["+", "-", "*", "/"]))
        num1 = 0
        num2 = 1
        num3 = 1
        num4 = 1
        num5 = 1
        difficulty_factors["maths_topic"][0] = 2
        difficulty_factors["difficulty_of_values"][0] = 2
        difficulty_factors["depth_of_knowledge"][0] = 4
        difficulty_factors["multiple_concepts"][0] = 3
        difficulty_factors["abstract_vs_concrete"][0] = 3
        difficulty_factors["number_of_steps"][0] = 3
        question = ""
        answer = 0
        for i in range(0, number_of_values-1):
            match operations[i]:
                case "+":
                    difficulty_factors["maths_topic"][0] += 1
                    if len(numbers) == 0:
                        numbers.append(random.randint(0, 200))
                        numbers.append(random.randint(0, 200))
                        if numbers[0] <= 10 or numbers[1] <= 10 or numbers[0] % 10 == 0 or numbers[1] % 10 == 0:
                            pass
                        elif 10 < numbers[0] <= 30 or 10 < num2 <= 30 or numbers[0] % 5 == 0 or numbers[1] % 5 == 0:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 30 < numbers[0] <= 50 or 30 < numbers[1] <= 50:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        # elif 50 < num1 <= 80 or 50 < num2 <= 80:
                        #     difficulty_weighting += 20
                        # elif 80 < num1 <= 140 or 80 < num2 <= 140:
                        #     difficulty_weighting += 25
                        else:
                            difficulty_factors["difficulty_of_values"][0] += (numbers[0] // 50 + numbers[1] // 50)
                        question = f"What is {numbers[0]} + {numbers[1]}?"
                        answer = numbers[0] + numbers[1]
                    else:
                        numbers.append(random.randint(0, 200))
                        if numbers[len(numbers)-1] <= 10 or numbers[len(numbers)-1] % 10 == 0:
                            pass
                        elif 10 < numbers[len(numbers)-1] <= 30 or numbers[len(numbers)-1] % 5 == 0:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 30 < numbers[len(numbers)-1] <= 50:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        # elif 50 < num1 <= 80 or 50 < num2 <= 80:
                        #     difficulty_weighting += 20
                        # elif 80 < num1 <= 140 or 80 < num2 <= 140:
                        #     difficulty_weighting += 25
                        else:
                            difficulty_factors["difficulty_of_values"][0] += (numbers[len(numbers)-1] // 50)
                        question = f"What is {numbers[0]} + {numbers[1]}?"
                        answer += numbers[len(numbers)-1]

                case "-":
                    difficulty_factors["maths_topic"][0] += 2
                    num1 = random.randint(0, 200)
                    num2 = random.randint(0, 200)
                    if num1 <= 10 or num2 <= 10 or num1 % 10 == 0 or num2 % 10 == 0 or abs(num1 - num2) < 10:
                        pass
                    elif 10 < num1 <= 30 or 10 < num2 <= 30 or num1 % 5 == 0 or num2 % 5 == 0:
                        difficulty_factors["difficulty_of_values"][0] += 1
                    elif 30 < num1 <= 50 or 30 < num2 <= 50:
                        difficulty_factors["difficulty_of_values"][0] += 2
                    # elif 50 < num1 <= 80 or 50 < num2 <= 80:
                    #     difficulty_weighting += 20
                    # elif 80 < num1 <= 140 or 80 < num2 <= 140:
                    #     difficulty_weighting += 25
                    else:
                        difficulty_factors["difficulty_of_values"][0] += (num1 // 50 + num2 // 50)
                    if num1 < num2:
                        difficulty_factors["difficulty_of_values"][0] += 1
                    if num1 - num2 < - 20:
                        difficulty_factors["difficulty_of_values"][0] += 1
                    question = f"What is {num1} - {num2}?"
                    answer = num1 - num2
                case "*":
                    difficulty_factors["maths_topic"][0] += 3
                    num1 = random.randint(2, 30)
                    num2 = random.randint(2, 30)
                    if num1 == 10 or num2 == 10 or num1 % 10 == 0 or num2 % 10 == 0 or num1 <= 4 or num2 <= 4:
                        pass
                    else:
                        difficulty_factors["difficulty_of_values"][0] += (num1 // 10 + num2 // 10)
                    question = f"What is {num1} * {num2}?"
                    answer = num1 * num2
                case "/":
                    difficulty_factors["maths_topic"][0] += 4
                    while num1 % num2 != 0 or num1 == 0:
                        num1 = random.randint(21, 200)
                        num2 = random.randint(2, 20)
                    if num2 == 10 or num2 == 2 or num2 == 5:
                        pass
                    else:
                        difficulty_factors["difficulty_of_values"][0] += (num1 // 30 + num2 // 5)
                    question = f"What is {num1} / {num2}?"
                    answer = num1 / num2
                    answer = int(answer)
                case _:
                    pass

        answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
        if final_difficulty == entered_difficulty:
            print(f"Final Difficulty: {final_difficulty}")
            print(f"Difficulty Weighting: {difficulty_weighting}")
            break
    # print(a, num2)
    # print(difficulty_weighting)
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

    return num1, num2, question, answer, difficulty_weighting

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

