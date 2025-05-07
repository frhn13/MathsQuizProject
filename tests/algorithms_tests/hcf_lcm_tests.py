from quiz.QuizCode.hcf_lcm_generation import hcf_lcm_question_generation

def test_generate_hcf_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = hcf_lcm_question_generation(entered_difficulty=3,
                                                                             difficulty_factors=difficulty_factors,
                                                                             question_types=question_types)
        if "What is the highest common factor" in question and (type(answer) == int or answer in ("True", "False")): break

    assert "What is the highest common factor" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_lcm_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = hcf_lcm_question_generation(entered_difficulty=2,
                                                                             difficulty_factors=difficulty_factors,
                                                                             question_types=question_types)
        if "What is the lowest common multiple" in question and (type(answer) == int or answer in ("True", "False")): break

    assert "What is the lowest common multiple" in question and (type(answer) == int or answer in ("True", "False"))

def test_generate_prime_factors_questions(difficulty_factors, question_types):
    question = ""
    answer = 0
    for x in range(100):
        question, answer, difficulty_weighting, time_needed = hcf_lcm_question_generation(entered_difficulty=5,
                                                                             difficulty_factors=difficulty_factors,
                                                                             question_types=question_types)
        if "be written as a product of its prime factors?" in question and (type(answer) == dict): break

    assert "be written as a product of its prime factors?" in question and (type(answer) == dict)