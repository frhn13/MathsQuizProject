import random

def operations_question_generation(entered_difficulty : int, question_types : list, difficulty_factors : dict):
    #difficulty_factors["maths_topic"][0] = 2
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

    difficulty_factors["maths_topic"][0] = 2
    difficulty_factors["difficulty_of_values"][0] = 2
    difficulty_factors["depth_of_knowledge"][0] = 4
    difficulty_factors["multiple_concepts"][0] = 3
    difficulty_factors["abstract_vs_concrete"][0] = 3
    difficulty_factors["number_of_steps"][0] = 3

    have_division_chance = random.random()
    while True:
        number_of_values = random.randint(2, 4)
        if have_division_chance > 0.7:
            operations = [random.choice(["+", "-", "*", "/"]) for x in range(number_of_values-1)]
        else:
            operations = [random.choice(["+", "-", "*"]) for x in range(number_of_values - 1)]
        numbers = [random.randint(1, 200) for x in range(number_of_values)]
        question = ""
        for x in range(0, len(numbers)):
            question += str(numbers[x])
            if x < len(numbers) - 1:
                question += operations[x]
        answer = eval(question)
        num1 = 0
        num2 = 1
        num3 = 1
        num4 = 1
        num5 = 1
        #difficulty_factors["maths_topic"][0] = 2
        #difficulty_factors["difficulty_of_values"][0] = 2
        #difficulty_factors["depth_of_knowledge"][0] = 4
        #difficulty_factors["multiple_concepts"][0] = 3
        #difficulty_factors["abstract_vs_concrete"][0] = 3
        #difficulty_factors["number_of_steps"][0] = 3
        if have_division_chance <= 0.7:
            break
        elif have_division_chance > 0.7 and question.find("/") != -1 and answer.is_integer():
            answer = int(answer)
            break
    return question, answer

question, answer = operations_question_generation(1, [], {})
print(question)
print(answer)
