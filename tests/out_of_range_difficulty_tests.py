import pytest

from quiz.QuizCode.operations_generation import operations_question_generation

def test_generate_operations_question_on_above_max_difficulty(difficulty_factors, question_types):
    question, answer, difficulty_weighting, time_needed = operations_question_generation(entered_difficulty=6, question_types=question_types, difficulty_factors=difficulty_factors)
    assert type(answer) == int or answer in ("True", "False")

    if type(answer) == int and abs(answer) > 1000:
        assert time_needed == 120
    else:
        assert time_needed == 60