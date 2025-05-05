import random
from math import gcd, lcm

from .helper_functions import answer_generation_decimals, answer_generation, answer_generation_fractions, calculate_difficulty, algebraic_fractions

def fractions_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    is_division = random.random() # Random chance that an operations question is a division one, used because otherwise division questions were rarely generated
    answer = ""
    question = ""
    answers = []

    while True: # Remains True until a valid question is generated with the entered difficulty
        time_needed = 60
        # Fractions question subtopic is randomly chosen from this list
        fractions_topic = random.choice(["conversion", "operations", "algebra"])
        question_type_chosen = random.choice(question_types) # Question type randomly chosen
        match fractions_topic:
            case "conversion":
                # Generates a conversion question using fractions, decimals and percentages
                difficulty_factors["maths_topic"][0] = 1
                difficulty_factors["difficulty_of_values"][0] = 1
                difficulty_factors["depth_of_knowledge"][0] = 2
                difficulty_factors["multiple_topics"][0] = 1
                difficulty_factors["difficulty_of_answer"][0] = 1
                difficulty_factors["number_of_steps"][0] = 1

                num1 = random.randint(1, 100)
                num2 = random.randint(1, 100)
                # Creates fraction, decimal and percentage values depending on randomised numbers
                fraction_value = f"{num1}/{num2}"
                decimal_value = num1 / num2
                percentage_value = (num1 / num2) * 100
                # Type of conversion question made selected randomly from this list
                convert = random.choice(["/ to .", "/ to %", "% to /", ". to /"])

                # Question becomes harder if certain criteria are met
                if round(decimal_value, 1) != decimal_value:
                    difficulty_factors["difficulty_of_answer"][0] += 1
                if num1 > num2:
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["difficulty_of_values"][0] += 2
                match convert:
                    case "/ to .":
                        # Generates conversion question from fraction to decimal
                        answer = decimal_value
                        question = f"Convert {fraction_value} to a decimal."
                        # Generates choices for answers for the question if the question type is multiple-choice or true/false
                        answers, difficulty_factors = answer_generation_decimals(answer, question_type_chosen,
                                                                                  difficulty_factors, False)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question
                        # Will break out of while loop if criteria are met
                        if percentage_value.is_integer()  and final_difficulty == entered_difficulty and num1 != num2:
                            break
                    case "/ to %":
                        # Generates conversion question from fraction to decimal
                        difficulty_factors["number_of_steps"][0] += 2
                        question = f"Convert {fraction_value} to a percentage."
                        answer = percentage_value
                        # Generates choices for answers for the question if the question type is multiple-choice or true/false
                        answers, difficulty_factors = answer_generation(int(answer), question_type_chosen,
                                                                                 difficulty_factors, False)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question
                        # Will break out of while loop if criteria are met
                        if percentage_value.is_integer() and final_difficulty == entered_difficulty and num1 != num2:
                            answer = int(percentage_value)
                            break
                    case ". to /":
                        # Generates conversion question from decimal to fraction
                        hcf = gcd(num1, num2)
                        final_numerator = int(num1 / hcf)
                        final_denominator = int(num2 / hcf)
                        answer = f"{final_numerator}/{final_denominator}"
                        question = f"Convert {decimal_value} to a fraction. Make sure you simplify your answer."
                        # Generates choices for answers for the question if the question type is multiple-choice or true/false
                        answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen,
                                                                                 difficulty_factors)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question
                        # Will break out of while loop if criteria are met
                        if percentage_value.is_integer() and final_difficulty == entered_difficulty and num1 != num2:
                            break
                    case "% to /":
                        # Generates conversion question from percentage to fraction
                        difficulty_factors["number_of_steps"][0] += 2
                        hcf = gcd(num1, num2)
                        final_numerator = int(num1 / hcf)
                        final_denominator = int(num2 / hcf)
                        answer = f"{final_numerator}/{final_denominator}"
                        question = f"Convert {percentage_value}% to a fraction. Make sure you simplify your answer."
                        # Generates choices for answers for the question if the question type is multiple-choice or true/false
                        answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen,
                                                                                 difficulty_factors)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question
                        # Will break out of while loop if criteria are met
                        if percentage_value.is_integer() and final_difficulty == entered_difficulty and num1 != num2:
                            break
                    case _:
                        pass
            case "operations":
                # Generates an operations question involving two fractions
                time_needed = 120 # Needs more time to answer this question than other subtopics
                is_valid = True

                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 3
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 3

                numerators = [random.randint(1, 20) for x in range(2)]
                denominators = [random.randint(1, 20) for x in range(2)]
                if is_division > 0.75:
                    operation = "/"
                else:
                    operation = random.choice(["+", "-", "*"])

                new_numerators = []
                new_denominators = []

                question = f"What is ({numerators[0]}/{denominators[0]}) {operation} ({numerators[1]}/{denominators[1]})? Make sure you simplify your answer."

                match operation:
                    case "+":
                        # Generates an addition question for fractions
                        difficulty_factors["maths_topic"][0] += 1
                        if denominators[0] != denominators[1]:
                            difficulty_factors["number_of_steps"][0] += 2
                            difficulty_factors["difficulty_of_values"][0] += 1
                        final_denominator = lcm(denominators[0], denominators[1])

                        for x in range(2):
                            new_numerators.append(int(numerators[x] * (final_denominator / denominators[x])))
                            new_denominators.append(int(final_denominator))

                        # Questions becomes more difficult if the fractions' numerators and denominators are larger
                        if final_denominator > 50:
                            difficulty_factors["difficulty_of_values"][0] += 0.5
                        elif final_denominator > 100:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif final_denominator > 200:
                            difficulty_factors["difficulty_of_values"][0] += 1.5
                        if new_numerators[0] <= 50 or new_denominators[1] <= 50:
                            pass
                        elif 50 < new_numerators[0] <= 100 or 50 < new_numerators[1] <= 100:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 100 < new_numerators[0] <= 200 or 100 < new_numerators[1] <= 200:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        else:
                            difficulty_factors["difficulty_of_values"][0] += 3

                        # HCF of numerator and denominator of answer used to simplify fraction in the answer
                        final_numerator = sum(new_numerators)
                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "-":
                        # Generates a subtraction question for fractions
                        difficulty_factors["maths_topic"][0] += 1
                        if denominators[0] != denominators[1]:
                            difficulty_factors["number_of_steps"][0] += 2
                            difficulty_factors["difficulty_of_values"][0] += 1
                        final_denominator = lcm(denominators[0], denominators[1])
                        for x in range(2):
                            new_numerators.append(int(numerators[x] * (final_denominator / denominators[x])))
                            new_denominators.append(int(final_denominator))

                        # Questions becomes more difficult if the fractions' numerators and denominators are larger
                        if final_denominator > 50:
                            difficulty_factors["difficulty_of_values"][0] += 0.5
                        elif final_denominator > 100:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif final_denominator > 200:
                            difficulty_factors["difficulty_of_values"][0] += 1.5
                        if new_numerators[0] <= 10 or new_denominators[1] <= 10:
                            pass
                        elif 10 < new_numerators[0] <= 50 or 10 < new_numerators[1] <= 50:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 50 < new_numerators[0] <= 100 or 50 < new_numerators[1] <= 100:
                            difficulty_factors["difficulty_of_values"][0] += 2
                        elif 100 < new_numerators[0] <= 200 or 100 < new_numerators[1] <= 200:
                            difficulty_factors["difficulty_of_values"][0] += 3
                        else:
                            difficulty_factors["difficulty_of_values"][0] += 4

                        # HCF of numerator and denominator of answer used to simplify fraction in the answer
                        final_numerator = new_numerators[0] - new_numerators[1]
                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "*":
                        # Generates a multiplication question for fractions
                        final_numerator = int(numerators[0] * numerators[1])
                        final_denominator = int(denominators[0] * denominators[1])

                        # Questions becomes more difficult if the fractions' numerators and denominators are larger
                        if numerators[0] == 1 or numerators[1] == 1:
                            pass
                        elif numerators[0] == 2 or numerators[0] == 10 or numerators[1] == 2 or numerators[1] == 10:
                            difficulty_factors["difficulty_of_values"][0] += 0.5
                        elif 2 < numerators[0] <= 10 or 2 < numerators[1] <= 10:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 10 < numerators[0] <= 20 or 10 < numerators[1] <= 20:
                            difficulty_factors["difficulty_of_values"][0] += 1.5

                        if denominators[0] == 1 or denominators[1] == 1:
                            pass
                        elif denominators[0] == 2 or denominators[0] == 10 or denominators[1] == 2 or denominators[1] == 10:
                            difficulty_factors["difficulty_of_values"][0] += 0.5
                        elif 2 < denominators[0] <= 10 or 2 < denominators[1] <= 10:
                            difficulty_factors["difficulty_of_values"][0] += 1
                        elif 10 < denominators[0] <= 20 or 10 < denominators[1] <= 20:
                            difficulty_factors["difficulty_of_values"][0] += 1.5

                        # HCF of numerator and denominator of answer used to simplify fraction in the answer
                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "/":
                        # Generates a division question for fractions
                        difficulty_factors["maths_topic"][0] += 2
                        difficulty_factors["depth_of_knowledge"][0] += 2
                        difficulty_factors["number_of_steps"][0] += 2

                        final_numerator = numerators[0] / numerators[1]
                        final_denominator = denominators[0] / denominators[1]
                        if final_numerator.is_integer() and final_denominator.is_integer():
                            # Questions becomes more difficult if the fractions' numerators and denominators are larger
                            if numerators[0] == 1 or numerators[1] == 1:
                                pass
                            elif numerators[0] == 2 or numerators[0] == 10 or numerators[1] == 2 or numerators[1] == 10:
                                difficulty_factors["difficulty_of_values"][0] += 0.5
                            elif 2 < numerators[0] <= 10 or 2 < numerators[1] <= 10:
                                difficulty_factors["difficulty_of_values"][0] += 1
                            elif 10 < numerators[0] <= 20 or 10 < numerators[1] <= 20:
                                difficulty_factors["difficulty_of_values"][0] += 1.5

                            if denominators[0] == 1 or denominators[1] == 1:
                                pass
                            elif denominators[0] == 2 or numerators[0] == 10 or denominators[1] == 2 or denominators[1] == 10:
                                difficulty_factors["difficulty_of_values"][0] += 0.5
                            elif 2 < denominators[0] <= 10 or 2 < denominators[1] <= 10:
                                difficulty_factors["difficulty_of_values"][0] += 1
                            elif 10 < denominators[0] <= 20 or 10 < denominators[1] <= 20:
                                difficulty_factors["difficulty_of_values"][0] += 1.5

                            # HCF of numerator and denominator of answer used to simplify fraction in the answer
                            hcf = gcd(int(final_numerator), int(final_denominator))
                            final_numerator = int(final_numerator / hcf)
                            final_denominator = int(final_denominator / hcf)
                            answer = f"{final_numerator}/{final_denominator}"
                        else:
                            is_valid = False

                # If numerator and denominators are equal for any fraction in operation, question is invalid
                if numerators[0] == denominators[0] or numerators[1] == denominators[1]: is_valid = False

                if is_valid: # Only can break out of loop if question is valid
                    # Generates choices for answers for the question if the question type is multiple-choice or true/false
                    answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen, difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question

                    if final_difficulty == entered_difficulty: # Breaks out of while loop if difficulty level matches entered difficulty
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break

            case "algebra":
                # Generates an algebraic fractions question
                time_needed = 120 # Needs more time to answer this question than other subtopics
                question_type_chosen = "free_text"
                question, answer, question_type_chosen = algebraic_fractions(difficulty_factors) # Calls function to make algebraic fraction expression
                # Generates choices for answers for the question if the question type is multiple-choice or true/false
                answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen,
                                                                          difficulty_factors)
                difficulty_factors["question_type"][0] = 6
                difficulty_factors["answers_similarity"][0] = 6
                difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors) # Generates difficulty level of question
                answer = str(answer)

                # Breaks out of while loop if difficulty level matches entered difficulty
                if question is not None and answer is not None and final_difficulty == entered_difficulty:
                    print(difficulty_factors)
                    print(difficulty_weighting)
                    break
            case _:
                pass

    match question_type_chosen:
        case "free_text":
            question = question
        # Question changed to display all four potential answers in multiple-choice question
        case "multiple-choice":
            question = f"{question}\nIs it {answers[0]}, {answers[1]}, {answers[2]} or {answers[3]}?"
        case "true/false":
            # Question changed to display all one potential answer in true/false question
            question = f"{question}\nIs the answer {answers[0]}, answer with True or False."
            # Answer changed from number value to True or False in true/false question
            if answers[0] == answer:
                answer = "True"
            else:
                answer = "False"
        case _:
            pass

    new_question = ""
    for x in range(len(question)): # Replaces 1x or 1y in question with x or y
        if question[x] == "1" and x + 1 < len(question) and (question[x + 1] == "x" or question[x + 1] == "y"):
            pass
        else:
            new_question += question[x]

    return new_question, answer, difficulty_weighting, time_needed
