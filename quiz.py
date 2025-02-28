import random

# Difficulty weighting includes maths topic, type of question, difficulty of values used, similarity of potential answers, ambiguity of how to answer question, adding multiple numbers today, calculator/no calculator
# Type of question: Free text -> multiple-choice -> true/false
# Topic: Calculus -> Trigonometry -> Quadratic questions -> Sequences -> Linear equations -> 3d shapes -> 2d shapes -> fractions and decimals -> operations
# Similarity of answers: How close answers are in MCQs, how close incorrect is to correct in true/false
# Difficulty of values used: How big values used are, whether final answer is whole number

# 30 seconds per question in non-mental maths, 30 * no. of questions is total time, no question-specific time
# 10 seconds per questions in mental maths, question-specific timer

def answer_generation(real_answer : int, difficulty_weighting : int, question_type : str):
    answers = []
    if question_type == "free_text":
        difficulty_weighting += 20
        answers.append(real_answer)

    if question_type == "multiple-choice":
        difficulty_weighting += 10
        while True:
            answers = []
            for i in range(3):
                answers.append(random.randint(real_answer - 20, real_answer + 20))
                if abs(answers[i] - real_answer) >= 10:
                    difficulty_weighting -= 5
            answers.append(real_answer)
            if len(answers) == len(set(answers)):
                random.shuffle(answers)
                break

    elif question_type == "true/false":
        answers = [random.randint(real_answer - 20, real_answer + 20)]
        if abs(answers[0] - real_answer) >= 10:
            difficulty_weighting -= 5

    return answers, difficulty_weighting

def answer_checking():
    pass

def operations_question_generation(entered_difficulty : int, question_types : list):
    # question_topic_chosen = random.choice(question_topics)
    question_type_chosen = random.choice(question_types)
    while True:
        operation = random.choice(["add", "sub", "mul", "div"])
        num1 = 0
        num2 = 1
        difficulty_weighting = 20
        question = ""
        answer = 0
        match operation:
            case "add":
                print("add")
                difficulty_weighting += 5
                num1 = random.randint(0, 200)
                num2 = random.randint(0, 200)
                if num1 <= 10 or num2 <= 10 or num1 % 10 == 0 or num2 % 10 == 0:
                    pass
                elif 10 < num1 <= 30 or 10 < num2 <= 30 or num1 % 5 == 0 or num2 % 5 == 0:
                    difficulty_weighting += 5
                elif 30 < num1 <= 50 or 30 < num2 <= 50:
                    difficulty_weighting += 10
                # elif 50 < num1 <= 80 or 50 < num2 <= 80:
                #     difficulty_weighting += 20
                # elif 80 < num1 <= 140 or 80 < num2 <= 140:
                #     difficulty_weighting += 25
                else:
                    difficulty_weighting += (num1 // 10 + num2 // 10)
                question = f"What is {num1} + {num2}?"
                answer = num1 + num2
            case "sub":
                print("sub")
                difficulty_weighting += 10
                num1 = random.randint(0, 200)
                num2 = random.randint(0, 200)
                if num1 <= 10 or num2 <= 10 or num1 % 10 == 0 or num2 % 10 == 0 or abs(num1 - num2) < 10:
                    pass
                elif 10 < num1 <= 30 or 10 < num2 <= 30 or num1 % 5 == 0 or num2 % 5 == 0:
                    difficulty_weighting += 5
                elif 30 < num1 <= 50 or 30 < num2 <= 50:
                    difficulty_weighting += 10
                # elif 50 < num1 <= 80 or 50 < num2 <= 80:
                #     difficulty_weighting += 20
                # elif 80 < num1 <= 140 or 80 < num2 <= 140:
                #     difficulty_weighting += 25
                else:
                    difficulty_weighting += (num1 // 10 + num2 // 10)
                if num1 < num2:
                    difficulty_weighting += 5
                if num1 - num2 < - 20:
                    difficulty_weighting += 5
                question = f"What is {num1} - {num2}?"
                answer = num1 - num2
            case "mul":
                print("mul")
                difficulty_weighting += 15
                num1 = random.randint(2, 30)
                num2 = random.randint(2, 30)
                if num1 == 10 or num2 == 10 or num1 % 10 == 0 or num2 % 10 == 0 or num1 <= 4 or num2 <= 4:
                    pass
                else:
                    difficulty_weighting += (num1 // 2 + num2 // 2)
                question = f"What is {num1} * {num2}?"
                answer = num1 * num2
            case "div":
                print("div")
                difficulty_weighting += 20
                while num1 % num2 != 0 or num1 == 0:
                    num1 = random.randint(20, 200)
                    num2 = random.randint(2, 20)
                if num2 == 10 or num2 == 2:
                    pass
                else:
                    difficulty_weighting += (num1 // 5 + num2 // 2)
                question = f"What is {num1} / {num2}?"
                answer = num1 / num2
                answer = int(answer)
            case _:
                pass

        answers, difficulty_weighting = answer_generation(answer, difficulty_weighting, question_type_chosen)
        if difficulty_weighting // 20 == entered_difficulty:
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

score = 0
difficulty_range = 50
difficulty_boundary = 20
current_difficulty = 2
user_answer = ""

for x in range(0, 10):
    answer_valid = False
    first_num, second_num, final_question, final_answer, final_difficulty_weighting = operations_question_generation(
        current_difficulty, ["free_text", "multiple-choice", "true/false"])
    print(f"Difficulty Weighting: {final_difficulty_weighting} Difficulty range: {difficulty_range} Difficulty Level: {current_difficulty}")
    while not answer_valid:
        user_answer = input(final_question + "\n")
        try:
            if type(user_answer) != type(final_answer):
                user_answer = int(user_answer)
                answer_valid = True
            else:
                if user_answer == "True" or user_answer == "False":
                    answer_valid = True
                else:
                    print("Please answer with True or False")
        except Exception:
            print("Please enter a number as an answer")
    if final_answer == user_answer:
        score += 1
        print("Correct")
        if current_difficulty > 1:
            difficulty_range += ((final_difficulty_weighting - (current_difficulty*20)) * 2)
            if difficulty_range >= 100:
                current_difficulty += 1
                difficulty_range = 50
    else:
        if current_difficulty < 5:
            difficulty_range -= ((difficulty_boundary - (final_difficulty_weighting - (current_difficulty*20))) * 2)
            if difficulty_range <= 0 and current_difficulty:
                current_difficulty -= 1
                difficulty_range = 50

print(f"{score} out of 10")
