from flask_login import current_user

from quiz import db
from quiz.models import QuestionTopics, QuestionDifficulties

def update_topic_information(topic_counter : dict):
    question_topics = QuestionTopics.query.filter_by(user_id=current_user.id).first()
    if question_topics:
        question_topics.operations_right += topic_counter["operations"][0]
        question_topics.operations_wrong += topic_counter["operations"][1]

        question_topics.fractions_right += topic_counter["fractions"][0]
        question_topics.fractions_wrong += topic_counter["fractions"][1]

        question_topics.calculus_right += topic_counter["calculus"][0]
        question_topics.calculus_wrong += topic_counter["calculus"][1]

        question_topics.equations_right += topic_counter["equations"][0]
        question_topics.equations_wrong += topic_counter["equations"][1]

        question_topics.expressions_right += topic_counter["expressions"][0]
        question_topics.expressions_wrong += topic_counter["expressions"][1]

        question_topics.sequences_right += topic_counter["sequences"][0]
        question_topics.sequences_wrong += topic_counter["sequences"][1]

        question_topics.percentages_right += topic_counter["percentages"][0]
        question_topics.percentages_wrong += topic_counter["percentages"][1]

        question_topics.triangles_right += topic_counter["triangles"][0]
        question_topics.triangles_wrong += topic_counter["triangles"][1]

        question_topics.hcf_lcm_right += topic_counter["hcf_lcm"][0]
        question_topics.hcf_lcm_wrong += topic_counter["hcf_lcm"][1]

        question_topics.circles_right += topic_counter["circles"][0]
        question_topics.circles_wrong += topic_counter["circles"][1]

        question_topics.graphs_right += topic_counter["graphs"][0]
        question_topics.graphs_wrong += topic_counter["graphs"][1]

        db.session.commit()

        question_topics.operations_percentage = question_topics.operations_right / (question_topics.operations_right + question_topics.operations_wrong) if (question_topics.operations_right + question_topics.operations_wrong) != 0 else 0
        question_topics.fractions_percentage = question_topics.fractions_right / (question_topics.fractions_right + question_topics.fractions_wrong) if (question_topics.fractions_right + question_topics.fractions_wrong) != 0 else 0
        question_topics.calculus_percentage = question_topics.calculus_right / (question_topics.calculus_right + question_topics.calculus_wrong) if (question_topics.calculus_right + question_topics.calculus_wrong) != 0 else 0
        question_topics.equations_percentage = question_topics.equations_right / (question_topics.equations_right + question_topics.equations_wrong) if (question_topics.equations_right + question_topics.equations_wrong) != 0 else 0
        question_topics.expressions_percentage = question_topics.expressions_right / (question_topics.expressions_right + question_topics.expressions_wrong) if (question_topics.expressions_right + question_topics.expressions_wrong) != 0 else 0
        question_topics.sequences_percentage = question_topics.sequences_right / (question_topics.sequences_right + question_topics.sequences_wrong) if (question_topics.sequences_right + question_topics.sequences_wrong) != 0 else 0
        question_topics.percentages_percentage = question_topics.percentages_right / (question_topics.percentages_right + question_topics.percentages_wrong) if (question_topics.percentages_right + question_topics.percentages_wrong) != 0 else 0
        question_topics.triangles_percentage = question_topics.triangles_right / (question_topics.triangles_right + question_topics.triangles_wrong) if (question_topics.triangles_right + question_topics.triangles_wrong) != 0 else 0
        question_topics.hcf_lcm_percentage = question_topics.hcf_lcm_right / (question_topics.hcf_lcm_right + question_topics.hcf_lcm_wrong) if (question_topics.hcf_lcm_right + question_topics.hcf_lcm_wrong) != 0 else 0
        question_topics.circles_percentage = question_topics.circles_right / (question_topics.circles_right + question_topics.circles_wrong) if (question_topics.circles_right + question_topics.circles_wrong) != 0 else 0
        question_topics.graphs_percentage = question_topics.graphs_right / (question_topics.graphs_right + question_topics.graphs_wrong) if (question_topics.graphs_right + question_topics.graphs_wrong) != 0 else 0

        db.session.commit()


def update_difficulty_information(difficulty_counter : dict):
    question_difficulties = QuestionDifficulties.query.filter_by(user_id=current_user.id).first()
    if question_difficulties:
        question_difficulties.level_one_right = difficulty_counter["level_1"][0]
        question_difficulties.level_one_wrong = difficulty_counter["level_1"][1]

        question_difficulties.level_two_right = difficulty_counter["level_2"][0]
        question_difficulties.level_two_wrong = difficulty_counter["level_2"][1]

        question_difficulties.level_three_right = difficulty_counter["level_3"][0]
        question_difficulties.level_three_wrong = difficulty_counter["level_3"][1]

        question_difficulties.level_four_right = difficulty_counter["level_4"][0]
        question_difficulties.level_four_wrong = difficulty_counter["level_4"][1]

        question_difficulties.level_five_right = difficulty_counter["level_5"][0]
        question_difficulties.level_five_wrong = difficulty_counter["level_5"][1]

        question_difficulties.level_six_right = difficulty_counter["level_6"][0]
        question_difficulties.level_six_wrong = difficulty_counter["level_6"][1]

        question_difficulties.level_seven_right = difficulty_counter["level_7"][0]
        question_difficulties.level_seven_wrong = difficulty_counter["level_7"][1]

        question_difficulties.level_eight_right = difficulty_counter["level_8"][0]
        question_difficulties.level_eight_wrong = difficulty_counter["level_8"][1]

        question_difficulties.level_nine_right = difficulty_counter["level_9"][0]
        question_difficulties.level_nine_wrong = difficulty_counter["level_9"][1]

        question_difficulties.level_ten_right = difficulty_counter["level_10"][0]
        question_difficulties.level_ten_wrong = difficulty_counter["level_10"][1]

        db.session.commit()

        question_difficulties.level_one_percentage = (question_difficulties.level_one_right /
                                                      (question_difficulties.level_one_right + question_difficulties.level_one_wrong)) \
            if (question_difficulties.level_one_right + question_difficulties.level_one_wrong) != 0 else 0
        question_difficulties.level_two_percentage = (question_difficulties.level_two_right /
                                                      (question_difficulties.level_two_right + question_difficulties.level_two_wrong)) \
            if (question_difficulties.level_two_right + question_difficulties.level_two_wrong) != 0 else 0
        question_difficulties.level_three_percentage = (question_difficulties.level_three_right /
                                                        (question_difficulties.level_three_right + question_difficulties.level_three_wrong)) \
            if (question_difficulties.level_three_right + question_difficulties.level_three_wrong) != 0 else 0
        question_difficulties.level_four_percentage = (question_difficulties.level_four_right /
                                                       (question_difficulties.level_four_right + question_difficulties.level_four_wrong)) \
            if (question_difficulties.level_four_right + question_difficulties.level_four_wrong) != 0 else 0
        question_difficulties.level_five_percentage = (question_difficulties.level_five_right /
                                                       (question_difficulties.level_five_right + question_difficulties.level_five_wrong)) \
            if (question_difficulties.level_five_right + question_difficulties.level_five_wrong) != 0 else 0
        question_difficulties.level_six_percentage = (question_difficulties.level_six_right /
                                                      (question_difficulties.level_six_right + question_difficulties.level_six_wrong)) \
            if (question_difficulties.level_six_right + question_difficulties.level_six_wrong) != 0 else 0
        question_difficulties.level_seven_percentage = (question_difficulties.level_seven_right /
                                                        (question_difficulties.level_seven_right + question_difficulties.level_seven_wrong)) \
            if (question_difficulties.level_seven_right + question_difficulties.level_seven_wrong) != 0 else 0
        question_difficulties.level_eight_percentage = (question_difficulties.level_eight_right /
                                                        (question_difficulties.level_eight_right + question_difficulties.level_eight_wrong)) \
            if (question_difficulties.level_eight_right + question_difficulties.level_eight_wrong) != 0 else 0
        question_difficulties.level_nine_percentage = (question_difficulties.level_nine_right /
                                                       (question_difficulties.level_nine_right + question_difficulties.level_nine_wrong)) \
            if (question_difficulties.level_nine_right + question_difficulties.level_nine_wrong) != 0 else 0
        question_difficulties.level_ten_percentage = (question_difficulties.level_ten_right /
                                                      (question_difficulties.level_ten_right + question_difficulties.level_ten_wrong)) \
            if (question_difficulties.level_ten_right + question_difficulties.level_ten_wrong) != 0 else 0

        db.session.commit()

def get_user_results(chosen_user):
    question_difficulties = QuestionDifficulties.query.filter_by(user_id=chosen_user.id).first()
    answers_correct = (question_difficulties.level_one_right + question_difficulties.level_two_right +
                       question_difficulties.level_three_right + question_difficulties.level_four_right +
                       question_difficulties.level_five_right + question_difficulties.level_six_right +
                       question_difficulties.level_seven_right + question_difficulties.level_eight_right +
                       question_difficulties.level_nine_right + question_difficulties.level_ten_right)

    answers_incorrect = (question_difficulties.level_one_wrong + question_difficulties.level_two_wrong +
                       question_difficulties.level_three_wrong + question_difficulties.level_four_wrong +
                       question_difficulties.level_five_wrong + question_difficulties.level_six_wrong +
                       question_difficulties.level_seven_wrong + question_difficulties.level_eight_wrong +
                       question_difficulties.level_nine_wrong + question_difficulties.level_ten_wrong)

    answers_percentage = (question_difficulties.level_one_percentage + question_difficulties.level_two_percentage +
                       question_difficulties.level_three_percentage + question_difficulties.level_four_percentage +
                       question_difficulties.level_five_percentage + question_difficulties.level_six_percentage +
                       question_difficulties.level_seven_percentage + question_difficulties.level_eight_percentage +
                       question_difficulties.level_nine_percentage + question_difficulties.level_ten_percentage) / 10

    return answers_correct, answers_incorrect, answers_percentage


def get_difficulty_results(chosen_user, chosen_difficulty):
    pass

def get_topic_results(chosen_user, chosen_topic):
    pass
