from flask_login import current_user, login_user, logout_user

from quiz import db
from quiz.models import QuestionTopics, QuestionDifficulties, User

def create_new_user(created_user: User):
    # Function adds records for new user to User table
    db.session.add(created_user)
    db.session.commit()
    # Also adds records for that user in the table that record their number of correct and incorrect answers for each topic and difficulty
    question_topics = QuestionTopics(user_id=created_user.id)
    question_difficulties = QuestionDifficulties(user_id=created_user.id)
    db.session.add(question_topics)
    db.session.add(question_difficulties)
    db.session.commit()
    login_user(created_user) # Then logs in the user

def delete_user(user_to_delete: User):
    # Function deletes the record for the specified user and their corresponding Question Topic and Question Difficulty records
    logout_user() # Logs out the current user before deleting their details
    question_difficulties_to_delete = QuestionDifficulties.query.filter_by(user_id=user_to_delete.id).first()
    question_topics_to_delete = QuestionTopics.query.filter_by(user_id=user_to_delete.id).first()
    db.session.delete(question_difficulties_to_delete)
    db.session.delete(question_topics_to_delete)
    db.session.delete(user_to_delete)
    db.session.commit()

def update_topic_information(topic_counter : dict):
    # Function updates the number of questions the current user got right or wrong for each topic with the results from the quiz they just did
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

def update_difficulty_information(difficulty_counter : dict):
    # Function updates the number of questions the current user got right or wrong for each difficulty level with the results from the quiz they just did
    question_difficulties = QuestionDifficulties.query.filter_by(user_id=current_user.id).first()
    if question_difficulties:
        question_difficulties.level_one_right += difficulty_counter["level_1"][0]
        question_difficulties.level_one_wrong += difficulty_counter["level_1"][1]

        question_difficulties.level_two_right += difficulty_counter["level_2"][0]
        question_difficulties.level_two_wrong += difficulty_counter["level_2"][1]

        question_difficulties.level_three_right += difficulty_counter["level_3"][0]
        question_difficulties.level_three_wrong += difficulty_counter["level_3"][1]

        question_difficulties.level_four_right += difficulty_counter["level_4"][0]
        question_difficulties.level_four_wrong += difficulty_counter["level_4"][1]

        question_difficulties.level_five_right += difficulty_counter["level_5"][0]
        question_difficulties.level_five_wrong += difficulty_counter["level_5"][1]

        question_difficulties.level_six_right += difficulty_counter["level_6"][0]
        question_difficulties.level_six_wrong += difficulty_counter["level_6"][1]

        question_difficulties.level_seven_right += difficulty_counter["level_7"][0]
        question_difficulties.level_seven_wrong += difficulty_counter["level_7"][1]

        question_difficulties.level_eight_right += difficulty_counter["level_8"][0]
        question_difficulties.level_eight_wrong += difficulty_counter["level_8"][1]

        question_difficulties.level_nine_right += difficulty_counter["level_9"][0]
        question_difficulties.level_nine_wrong += difficulty_counter["level_9"][1]

        question_difficulties.level_ten_right += difficulty_counter["level_10"][0]
        question_difficulties.level_ten_wrong += difficulty_counter["level_10"][1]

        db.session.commit()

def get_user_results(chosen_user):
    # Finds all total number of questions the passed in user got correct and incorrect and returns that
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

    try: # Also calculates the percentage of the questions the user got correct and returns that
        answers_percentage = round(answers_correct / (answers_correct + answers_incorrect), 2) * 100
    except ZeroDivisionError:
        answers_percentage = 0

    return answers_correct, answers_incorrect, answers_percentage


def get_difficulty_results(chosen_user : User, chosen_difficulty : int):
    question_difficulties = QuestionDifficulties.query.filter_by(user_id=chosen_user.id).first()
    answer_correct = 0
    answer_incorrect = 0
    answer_percentage = 0
    # Finds all total number of questions the passed in user got correct and incorrect for a particular difficulty level
    # and returns that along with the percentage of question they got right for that difficulty
    try:
        match chosen_difficulty:
            case 1:
                answer_correct = question_difficulties.level_one_right
                answer_incorrect = question_difficulties.level_one_wrong
                answer_percentage = round(question_difficulties.level_one_right / (question_difficulties.level_one_right + question_difficulties.level_one_wrong), 2) * 100
            case 2:
                answer_correct = question_difficulties.level_two_right
                answer_incorrect = question_difficulties.level_two_wrong
                answer_percentage = round(question_difficulties.level_two_right / (question_difficulties.level_two_right + question_difficulties.level_two_wrong), 2) * 100
            case 3:
                answer_correct = question_difficulties.level_three_right
                answer_incorrect = question_difficulties.level_three_wrong
                answer_percentage = (round(question_difficulties.level_three_right / (question_difficulties.level_three_right + question_difficulties.level_three_wrong), 2)) * 100
            case 4:
                answer_correct = question_difficulties.level_four_right
                answer_incorrect = question_difficulties.level_four_wrong
                answer_percentage = round(question_difficulties.level_four_right / (question_difficulties.level_four_right + question_difficulties.level_four_wrong), 2) * 100
            case 5:
                answer_correct = question_difficulties.level_five_right
                answer_incorrect = question_difficulties.level_five_wrong
                answer_percentage = round(question_difficulties.level_five_right / (question_difficulties.level_five_right + question_difficulties.level_five_wrong), 2) * 100
            case 6:
                answer_correct = question_difficulties.level_six_right
                answer_incorrect = question_difficulties.level_six_wrong
                answer_percentage = round(question_difficulties.level_six_right / (question_difficulties.level_six_right + question_difficulties.level_six_wrong), 2) * 100
            case 7:
                answer_correct = question_difficulties.level_seven_right
                answer_incorrect = question_difficulties.level_seven_wrong
                answer_percentage = round(question_difficulties.level_seven_right / (question_difficulties.level_seven_right + question_difficulties.level_seven_wrong), 2) * 100
            case 8:
                answer_correct = question_difficulties.level_eight_right
                answer_incorrect = question_difficulties.level_eight_wrong
                answer_percentage = round(question_difficulties.level_eight_right / (question_difficulties.level_eight_right + question_difficulties.level_eight_wrong), 2) * 100
            case 9:
                answer_correct = question_difficulties.level_nine_right
                answer_incorrect = question_difficulties.level_nine_wrong
                answer_percentage = round(question_difficulties.level_nine_right / (question_difficulties.level_nine_right + question_difficulties.level_nine_wrong), 2) * 100
            case 10:
                answer_correct = question_difficulties.level_ten_right
                answer_incorrect = question_difficulties.level_ten_wrong
                answer_percentage = round(question_difficulties.level_ten_right / (question_difficulties.level_ten_right + question_difficulties.level_ten_wrong), 2) * 100
    except ZeroDivisionError:
        answer_percentage = 0

    return answer_correct, answer_incorrect, answer_percentage

def get_topic_results(chosen_user : User, chosen_topic : str):
    question_topics = QuestionTopics.query.filter_by(user_id=chosen_user.id).first()
    answer_correct = 0
    answer_incorrect = 0
    answer_percentage = 0
    # Finds all total number of questions the passed in user got correct and incorrect for a particular maths topic
    # and returns that along with the percentage of question they got right for that topic
    try:
        match chosen_topic:
            case "operations":
                answer_correct = question_topics.operations_right
                answer_incorrect = question_topics.operations_wrong
                answer_percentage = round(question_topics.operations_right / (question_topics.operations_right + question_topics.operations_wrong), 2) * 100
            case "fractions":
                answer_correct = question_topics.fractions_right
                answer_incorrect = question_topics.fractions_wrong
                answer_percentage = round(question_topics.fractions_right / (question_topics.fractions_right + question_topics.fractions_wrong), 2) * 100
            case "expressions":
                answer_correct = question_topics.expressions_right
                answer_incorrect = question_topics.expressions_wrong
                answer_percentage = round(question_topics.expressions_right / (question_topics.expressions_right + question_topics.expressions_wrong), 2) * 100
            case "equations":
                answer_correct = question_topics.equations_right
                answer_incorrect = question_topics.equations_wrong
                answer_percentage = round(question_topics.equations_right / (question_topics.equations_right + question_topics.equations_wrong), 2) * 100
            case "percentages":
                answer_correct = question_topics.percentages_right
                answer_incorrect = question_topics.percentages_wrong
                answer_percentage = round(question_topics.percentages_right / (question_topics.percentages_right + question_topics.percentages_wrong), 2) * 100
            case "sequences":
                answer_correct = question_topics.sequences_right
                answer_incorrect = question_topics.sequences_wrong
                answer_percentage = round(question_topics.sequences_right / (question_topics.sequences_right + question_topics.sequences_wrong), 2) * 100
            case "triangles":
                answer_correct = question_topics.triangles_right
                answer_incorrect = question_topics.triangles_wrong
                answer_percentage = round(question_topics.triangles_right / (question_topics.triangles_right + question_topics.triangles_wrong), 2) * 100
            case "calculus":
                answer_correct = question_topics.calculus_right
                answer_incorrect = question_topics.calculus_wrong
                answer_percentage = round(question_topics.calculus_right / (question_topics.calculus_right + question_topics.calculus_wrong), 2) * 100
            case "hcf_lcm":
                answer_correct = question_topics.hcf_lcm_right
                answer_incorrect = question_topics.hcf_lcm_wrong
                answer_percentage = round(question_topics.hcf_lcm_right / (question_topics.hcf_lcm_right + question_topics.hcf_lcm_wrong), 2) * 100
            case "circles":
                answer_correct = question_topics.circles_right
                answer_incorrect = question_topics.circles_wrong
                answer_percentage = round(question_topics.circles_right / (question_topics.circles_right + question_topics.circles_wrong), 2) * 100
            case "graphs":
                answer_correct = question_topics.graphs_right
                answer_incorrect = question_topics.graphs_wrong
                answer_percentage = round(question_topics.graphs_right / (question_topics.graphs_right + question_topics.graphs_wrong), 2) * 100
            case _:
                answer_correct = question_topics.operations_right
                answer_incorrect = question_topics.operations_wrong
                answer_percentage = round(question_topics.operations_right / (question_topics.operations_right + question_topics.operations_wrong), 2) * 100
    except ZeroDivisionError:
        answer_percentage = 0

    return answer_correct, answer_incorrect, answer_percentage
