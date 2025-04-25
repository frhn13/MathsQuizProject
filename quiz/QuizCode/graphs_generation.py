import random
from sympy import symbols

from .helper_functions import answer_generation, calculate_difficulty, answer_generation_decimals


def increase_graph_difficulty(difficulty_factors: dict):
    difficulty_factors["difficulty_of_answer"][0] += 0.5
    difficulty_factors["number_of_steps"][0] += 0.5
    difficulty_factors["difficulty_of_values"][0] += 0.5
    difficulty_factors["depth_of_knowledge"][0] += 0.5
    return difficulty_factors

def graphs_questions_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    while True:
        calculator_needed = False
        is_valid = True
        question = ""
        answer = 0
        multiple_answers = "No"
        graph_values = {
            "time_values": [],
            "distance_values": [],
            "speed_values": [],
            "pie_chart_values": [],
            "pie_chart_labels": []
        }
        question_topic_chosen = random.choice(["DT_graphs", "VT_graphs", "pie_charts", "perpendicular_lines", "graph_transformation"])

        match question_topic_chosen:
            case "DT_graphs":
                calculator_needed = True
                num_datapoints = random.randint(3, 5)
                time_values = [x*5 for x in range(0, num_datapoints)]
                distance_values = [0, random.randint(5, 20)]
                if num_datapoints == 5:
                    distance_values.append(distance_values[1])
                    distance_values.append(random.randint(12, 30))
                    distance_values.append(0)
                elif num_datapoints == 4:
                    distance_values.append(distance_values[1])
                    distance_values.append(0) if random.random() > 0.5 else distance_values.append(random.randint(12, 30))
                elif num_datapoints == 3:
                    distance_values.append(0) if random.random() > 0.5 else distance_values.append(distance_values[1])
                question_subtopic_chosen = random.choice(["distance_travelled", "time_waited", "total_distance", "average_speed"])

                match question_subtopic_chosen:
                    case "distance_travelled":
                        difficulty_factors["maths_topic"][0] = 2
                        difficulty_factors["difficulty_of_values"][0] = 2
                        difficulty_factors["depth_of_knowledge"][0] = 2
                        difficulty_factors["multiple_topics"][0] = 3
                        difficulty_factors["difficulty_of_answer"][0] = 2
                        difficulty_factors["number_of_steps"][0] = 3
                        time_travelled = random.randint(1, 4)
                        question = f"What is the distance travelled after {time_travelled} minutes?"
                        answer = time_travelled/time_values[1] * distance_values[1]
                    case "time_waited":
                        difficulty_factors["maths_topic"][0] = 2
                        difficulty_factors["difficulty_of_values"][0] = 2
                        difficulty_factors["depth_of_knowledge"][0] = 2
                        difficulty_factors["multiple_topics"][0] = 3
                        difficulty_factors["difficulty_of_answer"][0] = 2
                        difficulty_factors["number_of_steps"][0] = 3
                        if distance_values[1] == distance_values[2]:
                            question = f"How long does the person wait for before continuing?"
                            answer = time_values[2] - time_values[1]
                        else:
                            is_valid = False
                    case "total_distance":
                        difficulty_factors["maths_topic"][0] = 2
                        difficulty_factors["difficulty_of_values"][0] = 3
                        difficulty_factors["depth_of_knowledge"][0] = 3
                        difficulty_factors["multiple_topics"][0] = 3
                        difficulty_factors["difficulty_of_answer"][0] = 3
                        difficulty_factors["number_of_steps"][0] = 3
                        question = "What is the total distance travelled?"
                        answer = max(distance_values) * 2 if distance_values[-1] == 0 else max(distance_values)
                    case "average_speed":
                        difficulty_factors["maths_topic"][0] = 5
                        difficulty_factors["difficulty_of_values"][0] = 5
                        difficulty_factors["depth_of_knowledge"][0] = 4
                        difficulty_factors["multiple_topics"][0] = 5
                        difficulty_factors["difficulty_of_answer"][0] = 4
                        difficulty_factors["number_of_steps"][0] = 5
                        if num_datapoints >= 4:
                            question = "What is the average speed at the end?"
                            answer = abs((distance_values[-1] - distance_values[-2]) / (time_values[-1] - time_values[-2]))
                        else:
                            question = "What is the average speed at the start?"
                            answer = abs((distance_values[0] - distance_values[1]) / (time_values[0] - time_values[1]))

                graph_values["time_values"] = time_values
                graph_values["distance_values"] = distance_values

            case "VT_graphs":
                calculator_needed = True
                difficulty_factors["maths_topic"][0] = 8
                difficulty_factors["difficulty_of_values"][0] = 8
                difficulty_factors["depth_of_knowledge"][0] = 7
                difficulty_factors["multiple_topics"][0] = 7
                difficulty_factors["difficulty_of_answer"][0] = 8
                difficulty_factors["number_of_steps"][0] = 7
                num_datapoints = random.randint(3, 4)
                time_values = [x * 5 for x in range(0, num_datapoints)]
                speed_values = [random.randint(0, 3), random.randint(5, 10)]
                speed_values.append(speed_values[1])
                if num_datapoints == 4:
                    speed_values.append(0) if random.random() > 0.5 else speed_values.append(random.randint(1, 4))

                question_subtopic_chosen = random.choice(["acceleration", "distance"])
                match question_subtopic_chosen:
                    case "acceleration":
                        question = f"What is the acceleration for the first {time_values[1]} seconds?"
                        answer = (speed_values[1] - speed_values[0]) / time_values[1]
                    case "distance":
                        difficulty_factors["number_of_steps"][0] += 2
                        difficulty_factors["multiple_topics"][0] += 2
                        question = f"What is the total distance covered in {time_values[-1]} seconds?"
                        area1 = 0.5 * time_values[1] * (speed_values[0] + speed_values[1])
                        area2 = (speed_values[2] - speed_values[1]) * (time_values[2] - time_values[1])
                        area3 = 0 if num_datapoints == 3 else 0.5 * (time_values[3] - time_values[2]) * (speed_values[2] + speed_values[3])
                        answer = area1 + area2 + area3

                graph_values["time_values"] = time_values
                graph_values["speed_values"] = speed_values

            case "pie_charts":
                calculator_needed = True
                values = [random.randint(13, 18), random.randint(6, 12), random.randint(13, 18), random.randint(6, 12)]
                values.append(60-sum(values))
                multiplier = random.randint(1, 4)
                values = [x*multiplier for x in values]
                labels = ["Football", "Cricket", "Rugby", "Basketball", "Tennis"]

                question_subtopic_chosen = random.choice(["missing_value", "total", "missing_value_from_total"])
                match question_subtopic_chosen:
                    case "missing_value":
                        difficulty_factors["maths_topic"][0] = 2
                        difficulty_factors["difficulty_of_values"][0] = 2
                        difficulty_factors["depth_of_knowledge"][0] = 3
                        difficulty_factors["multiple_topics"][0] = 4
                        difficulty_factors["difficulty_of_answer"][0] = 3
                        difficulty_factors["number_of_steps"][0] = 4
                        question = f"People were asked to choose there favourite sport. If {values[4]} chose {labels[4]}, then how many people chose {labels[0]}?"
                        answer = values[0]
                    case "total":
                        difficulty_factors["maths_topic"][0] = 2
                        difficulty_factors["difficulty_of_values"][0] = 2
                        difficulty_factors["depth_of_knowledge"][0] = 2
                        difficulty_factors["multiple_topics"][0] = 3
                        difficulty_factors["difficulty_of_answer"][0] = 2
                        difficulty_factors["number_of_steps"][0] = 3
                        question = f"People were asked to choose there favourite sport. If {values[4]} chose {labels[4]}, then how many people were asked in total?"
                        answer = sum(values)
                    case "missing_value_from_total":
                        difficulty_factors["maths_topic"][0] = 2
                        difficulty_factors["difficulty_of_values"][0] = 2
                        difficulty_factors["depth_of_knowledge"][0] = 2
                        difficulty_factors["multiple_topics"][0] = 3
                        difficulty_factors["difficulty_of_answer"][0] = 2
                        difficulty_factors["number_of_steps"][0] = 3
                        question = f"People were asked to choose there favourite sport. If {sum(values)} people were asking in total, then how many people chose {labels[0]}?"
                        answer = values[0]

                graph_values["pie_chart_values"] = values
                graph_values["pie_chart_labels"] = labels

            case "graph_transformation":
                difficulty_factors["maths_topic"][0] = 8
                difficulty_factors["difficulty_of_values"][0] = 8
                difficulty_factors["depth_of_knowledge"][0] = 7
                difficulty_factors["multiple_topics"][0] = 8
                difficulty_factors["difficulty_of_answer"][0] = 7
                difficulty_factors["number_of_steps"][0] = 7
                x_coordinate = random.randint(1, 10) * random.choice([-1, 1])
                y_coordinate = random.randint(1, 10) * random.choice([-1, 1])
                x_translation = 0 if random.random() > 0.5 else random.randint(1, 5) * random.choice([-1, 1])
                y_translation = 0 if random.random() > 0.5 else random.randint(1, 5) * random.choice([-1, 1])
                x_enlargement = 1 if random.random() > 0.5 else random.choice([2, 4, 0.5, (1/3), 0.25]) * random.choice([-1, 1])
                y_enlargement = 1 if random.random() > 0.5 else random.choice([2, 3, 4, 0.5, 0.25]) * random.choice([-1, 1])

                if x_translation != 0:
                    difficulty_factors = increase_graph_difficulty(difficulty_factors)
                if y_translation != 0:
                    difficulty_factors = increase_graph_difficulty(difficulty_factors)
                if x_enlargement != 1:
                    difficulty_factors = increase_graph_difficulty(difficulty_factors)
                if y_enlargement != 1:
                    difficulty_factors = increase_graph_difficulty(difficulty_factors)

                new_x = (x_coordinate / x_enlargement) - x_translation
                new_y = (y_coordinate * y_enlargement) + y_translation
                if x_translation == 0:
                    x_translation_str = ""
                elif x_translation < 0:
                    x_translation_str = f"{x_translation}"
                else:
                    x_translation_str = f"+{x_translation}"
                if y_translation == 0:
                    y_translation_str = ""
                elif y_translation < 0:
                    y_translation_str = f"{y_translation}"
                else:
                    y_translation_str = f"+{y_translation}"
                if x_enlargement == 1:
                    x_enlargement_str = ""
                elif abs(x_enlargement) == abs(1/3):
                    x_enlargement_str = f"{x_enlargement:.2f}"
                else:
                    x_enlargement_str = f"{x_enlargement}"
                if y_enlargement == 1:
                    y_enlargement_str = ""
                else:
                    y_enlargement_str = f"{y_enlargement}"

                equation = f"y = {y_enlargement_str}f({x_enlargement_str}x{x_translation_str}){y_translation_str}"
                question = (f"If ({x_coordinate},{y_coordinate}) is the maximum point of the curve y=f(x) then find the "
                            f"coordinates of the maximum point of the curve with the equation: {equation}")
                answer = [new_x, new_y]
                multiple_answers = "TwoDifferent"
                graph_values = None

            case "perpendicular_lines":
                calculator_needed = True
                difficulty_factors["maths_topic"][0] = 8
                difficulty_factors["difficulty_of_values"][0] = 8
                difficulty_factors["depth_of_knowledge"][0] = 8
                difficulty_factors["multiple_topics"][0] = 7
                difficulty_factors["difficulty_of_answer"][0] = 9
                difficulty_factors["number_of_steps"][0] = 8
                x = symbols("x")
                while True:
                    linear_value = random.choice([1, 2, 4, 5, 10, 0.1, 0.2, 0.25, 0.5]) * random.choice([1, -1])
                    number_value = random.randint(1, 10) * random.choice([1, -1])
                    f = linear_value * x + number_value
                    x_value = random.randint(1, 5)
                    y_value = f.subs(x, x_value)
                    gradient = -1 / linear_value
                    y_intercept = y_value - (x_value * gradient)
                    if y_intercept == round(y_intercept, 0):
                        break
                if gradient == int(gradient):
                    gradient = int(gradient)
                if gradient == 1:
                    gradient = ""
                    difficulty_factors["difficulty_of_values"][0] -= 1
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                if gradient == -1:
                    gradient = "-"
                    difficulty_factors["difficulty_of_values"][0] -= 1
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                if linear_value == 1:
                    linear_value = ""
                if linear_value == -1:
                    linear_value = "-"
                question = (f"What is the equation of a perpendicular line to y = {linear_value}x + {number_value:.0f} "
                            f"which passed through the point ({x_value}, {y_value:.0f}). Give your answer in the form y=mx+c "
                            f"and give answers in the form of decimals where needed.")
                if y_intercept == 0:
                    answer = f"y={gradient}x"
                    difficulty_factors["difficulty_of_answer"][0] -= 1
                elif y_intercept < 0:
                    answer = f"y={gradient}x{y_intercept:.0f}"
                else:
                    answer = f"y={gradient}x+{y_intercept:.0f}"
                graph_values = None

        question_type_chosen = random.choice(question_types)
        if type(answer) == int:
            answers, difficulty_factors = answer_generation(answer, question_type_chosen, difficulty_factors)
        elif type(answer) == float:
            answers, difficulty_factors = answer_generation_decimals(answer, question_type_chosen, difficulty_factors)
        else:
            question_type_chosen = "free-text"
            difficulty_factors["question_type"][0] = 8
            difficulty_factors["answers_similarity"][0] = 9
        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

        if final_difficulty == entered_difficulty and is_valid:
            print(difficulty_factors)
            print(difficulty_weighting)
            break

    match question_type_chosen:
        case "free_text":
            question = question
        case "multiple-choice":
            if type(answers[0]) == int:
                question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
            elif type(answers[0]) == float:
                question = f"{question}\nIs it {answers[0]:.2f}, {answers[1]:.2f}, {answers[2]:.2f} or {answers[3]:.2f}?"
        case "true/false":
            question = f"{question}\nIs the answer {answers[0]:.2f}, answer with True or False."
            if answers[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    return question, answer, difficulty_weighting, graph_values, multiple_answers, calculator_needed

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

# graphs_questions_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)
