import random

# Difficulty weighting includes maths topic, type of question, difficulty of values used, similarity of potential answers, ambiguity of how to answer question
# Type of question: Free text -> multiple-choice -> true/false
# Topic: Calculus -> Trigonometry -> Quadratic questions -> Sequences -> Linear equations -> 3d shapes -> 2d shapes -> fractions and decimals -> operations
# Similarity of answers: How close answers are in MCQs, how close incorrect is to correct in true/false
# Difficulty of values used: How big values used are, whether final answer is whole number

def free_text_question_generation(current_difficulty : int, question_types : list):
    difficulty_weighting = 20
    question_type_chosen = random.choice(question_types)
    a = 0
    b = 1
    operation = ""
    question = ""
    answer = 0
    while True:
        if question_type_chosen == "operations":
            operation = random.choice(["add", "sub", "mul", "div"])
            a = 0
            b = 1
            difficulty_weighting = 20
            match operation:
                case "add":
                    print("add")
                    difficulty_weighting += 5
                    a = random.randint(0, 200)
                    b = random.randint(0, 200)
                    if a <= 10 or b <= 10 or a % 10 == 0 or b % 10 == 0:
                        pass
                    elif 10 < a <= 30 or 10 < b <= 30 or a % 5 == 0 or b % 5 == 0:
                        difficulty_weighting += 5
                    elif 30 < a <= 50 or 30 < b <= 50:
                        difficulty_weighting += 10
                    # elif 50 < a <= 80 or 50 < b <= 80:
                    #     difficulty_weighting += 20
                    # elif 80 < a <= 140 or 80 < b <= 140:
                    #     difficulty_weighting += 25
                    else:
                        difficulty_weighting += (a // 10 + b // 10)
                    question = f"What is {a} + {b}?"
                    answer = a + b
                case "sub":
                    print("sub")
                    difficulty_weighting += 10
                    a = random.randint(0, 200)
                    b = random.randint(0, 200)
                    if a <= 10 or b <= 10 or a % 10 == 0 or b % 10 == 0 or abs(a-b) < 10:
                        pass
                    elif 10 < a <= 30 or 10 < b <= 30 or a % 5 == 0 or b % 5 == 0:
                        difficulty_weighting += 5
                    elif 30 < a <= 50 or 30 < b <= 50:
                        difficulty_weighting += 10
                    # elif 50 < a <= 80 or 50 < b <= 80:
                    #     difficulty_weighting += 20
                    # elif 80 < a <= 140 or 80 < b <= 140:
                    #     difficulty_weighting += 25
                    else:
                        difficulty_weighting += (a // 10 + b // 10)
                    if a < b:
                        difficulty_weighting += 5
                    if a - b < - 20:
                        difficulty_weighting += 5
                    question = f"What is {a} - {b}?"
                    answer = a - b
                case "mul":
                    print("mul")
                    difficulty_weighting += 15
                    a = random.randint(2, 30)
                    b = random.randint(2, 30)
                    if a == 10 or b == 10 or a % 10 == 0 or b % 10 == 0 or a <= 4 or b <= 4:
                        pass
                    else:
                        difficulty_weighting += (a // 2 + b // 2)
                    question = f"What is {a} * {b}?"
                    answer = a * b
                case "div":
                    print("div")
                    difficulty_weighting += 20
                    while a % b != 0 or a == 0:
                        a = random.randint(20, 200)
                        b = random.randint(2, 20)
                    if b == 10 or b == 2:
                        pass
                    else:
                        difficulty_weighting += (a // 5 + b // 2)
                    question = f"What is {a} / {b}?"
                    answer = a / b

            if difficulty_weighting // 20 == current_difficulty:
                break
    print(a, b)
    print(difficulty_weighting)
    return a, b, question, answer

def multiple_choice_question_generation(current_difficulty):
    difficulty_weighting = 10

def true_false_question_generation(current_difficulty):
    difficulty_weighting = 0

def generate_question():
    pass

score = 0
for x in range(0, 10):
    a, b, question, answer = free_text_question_generation(2, ["operations"])
    user_answer = int(input(question + "\n"))
    if answer == user_answer:
        score += 1
        print("Correct")

print(f"{score} out of 10")
