import random
from math import gcd, lcm

from .helper_functions import answer_generation_decimals, answer_generation, answer_generation_fractions, calculate_difficulty, algebraic_fractions

# Fraction conversion, fraction operations, algebraic fractions, surds
def fractions_question_generation(entered_difficulty: int, question_types: list, difficulty_factors: dict):
    question_type_chosen = random.choice(question_types)
    # fractions_topic = random.choice(["conversion", "operations", "algebra", "surds"])
    is_division = random.random()
    fractions_topic = "algebra"
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    answer = ""
    question = ""
    answers = []
    difficulty_weighting = 0

    while True:
        fractions_topic = random.choice(["conversion", "operations", "algebra"])
        match fractions_topic:
            case "conversion":
                difficulty_factors["maths_topic"][0] = 1
                difficulty_factors["difficulty_of_values"][0] = 1
                difficulty_factors["depth_of_knowledge"][0] = 2
                difficulty_factors["multiple_topics"][0] = 1
                difficulty_factors["difficulty_of_answer"][0] = 1
                difficulty_factors["number_of_steps"][0] = 1

                num1 = random.randint(1, 100)
                num2 = random.randint(1, 100)
                fraction_value = f"{num1}/{num2}"
                decimal_value = num1 / num2
                percentage_value = (num1 / num2) * 100
                convert = random.choice(["/ to .", "/ to %", "% to /", ". to /"])

                if round(decimal_value, 1) != decimal_value:
                    difficulty_factors["difficulty_of_answer"][0] += 1
                if num1 > num2:
                    difficulty_factors["difficulty_of_answer"][0] += 1
                    difficulty_factors["difficulty_of_values"][0] += 2
                match convert:
                    case "/ to .":
                        answer = decimal_value
                        question = f"Convert {fraction_value} to a decimal."
                        answers, difficulty_factors = answer_generation_decimals(answer, question_type_chosen,
                                                                                  difficulty_factors)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                        decimal_str = str(decimal_value)
                        if percentage_value.is_integer()  and final_difficulty == entered_difficulty and num1 < num2:
                            break
                    case "/ to %":
                        difficulty_factors["number_of_steps"][0] += 2
                        question = f"Convert {fraction_value} to a percentage."
                        answer = percentage_value
                        answers, difficulty_factors = answer_generation(int(answer), question_type_chosen,
                                                                                 difficulty_factors)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                        if percentage_value.is_integer() and final_difficulty == entered_difficulty:
                            answer = int(percentage_value)
                            break
                    case ". to /":
                        hcf = gcd(num1, num2)
                        final_numerator = int(num1 / hcf)
                        final_denominator = int(num2 / hcf)
                        answer = f"{final_numerator}/{final_denominator}"
                        question = f"Convert {decimal_value} to a fraction."

                        answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen,
                                                                                 difficulty_factors)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                        if percentage_value.is_integer() and final_difficulty == entered_difficulty:
                            break
                    case "% to /":
                        difficulty_factors["number_of_steps"][0] += 2
                        hcf = gcd(num1, num2)
                        final_numerator = int(num1 / hcf)
                        final_denominator = int(num2 / hcf)
                        answer = f"{final_numerator}/{final_denominator}"
                        question = f"Convert {percentage_value}% to a fraction."
                        answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen,
                                                                                 difficulty_factors)
                        difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                        if percentage_value.is_integer() and final_difficulty == entered_difficulty:
                            break
                    case _:
                        pass
            case "operations":
                is_valid = True

                difficulty_factors["maths_topic"][0] = 3
                difficulty_factors["difficulty_of_values"][0] = 2
                difficulty_factors["depth_of_knowledge"][0] = 4
                difficulty_factors["multiple_topics"][0] = 5
                difficulty_factors["difficulty_of_answer"][0] = 3
                difficulty_factors["number_of_steps"][0] = 2

                numerators = [random.randint(1, 20) for x in range(2)]
                denominators = [random.randint(1, 20) for x in range(2)]
                if is_division > 0.75:
                    operation = "/"
                else:
                    operation = random.choice(["+", "-", "*"])

                new_numerators = []
                new_denominators = []

                question = f"What is {numerators[0]}/{denominators[0]} {operation} {numerators[1]}/{denominators[1]}?"

                match operation:
                    case "+":
                        difficulty_factors["maths_topic"][0] += 1
                        if denominators[0] != denominators[1]:
                            difficulty_factors["number_of_steps"][0] += 2
                            difficulty_factors["difficulty_of_values"][0] += 1
                        final_denominator = lcm(denominators[0], denominators[1])

                        for x in range(2):
                            new_numerators.append(int(numerators[x] * (final_denominator / denominators[x])))
                            new_denominators.append(int(final_denominator))
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

                        final_numerator = sum(new_numerators)
                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "-":
                        difficulty_factors["maths_topic"][0] += 1
                        if denominators[0] != denominators[1]:
                            difficulty_factors["number_of_steps"][0] += 2
                            difficulty_factors["difficulty_of_values"][0] += 1
                        final_denominator = lcm(denominators[0], denominators[1])
                        for x in range(2):
                            new_numerators.append(int(numerators[x] * (final_denominator / denominators[x])))
                            new_denominators.append(int(final_denominator))

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

                        final_numerator = new_numerators[0] - new_numerators[1]
                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "*":
                        final_numerator = int(numerators[0] * numerators[1])
                        final_denominator = int(denominators[0] * denominators[1])

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

                        hcf = gcd(final_numerator, final_denominator)
                        final_numerator = int(final_numerator / hcf)
                        final_denominator = int(final_denominator / hcf)
                        answer = f"{final_numerator}/{final_denominator}"

                    case "/":
                        difficulty_factors["maths_topic"][0] += 2
                        difficulty_factors["depth_of_knowledge"][0] += 2
                        difficulty_factors["number_of_steps"][0] += 2
                        final_numerator = numerators[0] / numerators[1]
                        final_denominator = denominators[0] / denominators[1]
                        if final_numerator.is_integer() and final_denominator.is_integer():

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

                            hcf = gcd(int(final_numerator), int(final_denominator))
                            final_numerator = int(final_numerator / hcf)
                            final_denominator = int(final_denominator / hcf)
                            answer = f"{final_numerator}/{final_denominator}"
                        else:
                            is_valid = False
                if is_valid:
                    answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen, difficulty_factors)
                    difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)

                    if final_difficulty == entered_difficulty:
                        print(difficulty_factors)
                        print(difficulty_weighting)
                        break

            case "algebra":
                question, answer, question_type_chosen = algebraic_fractions(difficulty_factors)
                answers, difficulty_factors = answer_generation_fractions(answer, question_type_chosen,
                                                                          difficulty_factors)
                difficulty_weighting, final_difficulty = calculate_difficulty(difficulty_factors)
                answer = str(answer)

                if question is not None and answer is not None and final_difficulty == entered_difficulty:
                    print(difficulty_factors)
                    print(difficulty_weighting)
                    break
            case "surds":
                pass
            case _:
                pass

    match question_type_chosen:
        case "free_text":
            question = question
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

    return question, answer, difficulty_weighting
