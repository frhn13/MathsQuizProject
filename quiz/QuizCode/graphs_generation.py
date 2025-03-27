import random
from matplotlib import pyplot as plt

# from .helper_functions import answer_generation, calculate_difficulty

# DT graphs, VT graphs, pie charts, solving equations graphically, transforming graphs
def graphs_questions_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    while True:
        question = ""
        answer = 0
        question_type_chosen = "free-text"
        question_topic_chosen = random.choice(["VT_graphs"])
        question_subtopic_chosen = ""

        match question_topic_chosen:
            case "DT_graphs":
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
                print(time_values)
                print(distance_values)
                question_subtopic_chosen = random.choice(["distance_travelled", "time_waited", "total_distance", "average_speed"])

                match question_subtopic_chosen:
                    case "distance_travelled":
                        time_travelled = random.randint(1, 4)
                        question = f"What is the distance travelled after {time_travelled} minutes?"
                        answer = time_travelled/time_values[1] * distance_values[1]
                    case "time_waited":
                        if distance_values[1] == distance_values[2]:
                            question = f"How long does the person wait for before continuing?"
                            answer = time_values[2] - time_values[1]
                    case "total_distance":
                        question = "What is the total distance travelled?"
                        answer = max(distance_values) * 2 if distance_values[-1] == 0 else max(distance_values)
                    case "average_speed":
                        if num_datapoints >= 4:
                            question = "What is the average speed at the end?"
                            answer = abs((distance_values[-1] - distance_values[-2]) / (time_values[-1] - time_values[-2]))
                        else:
                            question = "What is the average speed at the start?"
                            answer = abs((distance_values[0] - distance_values[1]) / (time_values[0] - time_values[1]))
                plt.plot(time_values, distance_values, linestyle="-", marker=".", color="blue")
                plt.xlabel("Time in Minutes")
                plt.ylabel("Distance")
                plt.grid()
                plt.show()
                print(question)
                print(answer)
                break

            case "VT_graphs":
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
                        question = f"What is the total distance covered in {time_values[-1]} seconds?"
                        area1 = 0.5 * time_values[1] * (speed_values[0] + speed_values[1])
                        area2 = (speed_values[2] - speed_values[1]) * (time_values[2] - time_values[1])
                        area3 = 0 if num_datapoints == 3 else 0.5 * (time_values[3] - time_values[2]) * (speed_values[2] + speed_values[3])
                        answer = area1 + area2 + area3

                plt.plot(time_values, speed_values, linestyle="-", marker=".", color="blue")
                plt.xlabel("Time in seconds")
                plt.ylabel("Speed")
                plt.grid()
                plt.show()
                print(question)
                print(answer)

            case "pie_charts":
                pass
            case "graph_transformation":
                pass

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

graphs_questions_generation(8, ["free_text", "multiple-choice", "true/false"], difficulty_factors)