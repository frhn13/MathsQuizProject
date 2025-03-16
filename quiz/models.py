from flask_login import UserMixin
import bcrypt

from quiz import db, login_manager

@login_manager.user_loader
def load_user(user_id): # Needed for logging in users
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email = db.Column(db.String(length=40), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    question_topics = db.relationship("QuestionTopics")
    question_difficulties = db.relationship("QuestionDifficulties")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

class QuestionTopics(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    operations_right = db.Column(db.Integer(), default=0)
    operations_wrong = db.Column(db.Integer(), default=0)
    operations_percentage = db.Column(db.Float(), default=0.0)

    expressions_right = db.Column(db.Integer(), default=0)
    expressions_wrong = db.Column(db.Integer(), default=0)
    expressions_percentage = db.Column(db.Float(), default=0.0)

    fractions_right = db.Column(db.Integer(), default=0)
    fractions_wrong = db.Column(db.Integer(), default=0)
    fractions_percentage = db.Column(db.Float(), default=0.0)

    equations_right = db.Column(db.Integer(), default=0)
    equations_wrong = db.Column(db.Integer(), default=0)
    equations_percentage = db.Column(db.Float(), default=0.0)

    sequences_right = db.Column(db.Integer(), default=0)
    sequences_wrong = db.Column(db.Integer(), default=0)
    sequences_percentage = db.Column(db.Float(), default=0.0)

    hcf_lcm_right = db.Column(db.Integer(), default=0)
    hcf_lcm_wrong = db.Column(db.Integer(), default=0)
    hcf_lcm_percentage = db.Column(db.Float(), default=0.0)

    percentages_right = db.Column(db.Integer(), default=0)
    percentages_wrong = db.Column(db.Integer(), default=0)
    percentages_percentage = db.Column(db.Float(), default=0.0)

    calculus_right = db.Column(db.Integer(), default=0)
    calculus_wrong = db.Column(db.Integer(), default=0)
    calculus_percentage = db.Column(db.Float(), default=0.0)

    triangles_right = db.Column(db.Integer(), default=0)
    triangles_wrong = db.Column(db.Integer(), default=0)
    triangles_percentage = db.Column(db.Float(), default=0.0)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)

class QuestionDifficulties(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    level_one_right = db.Column(db.Integer(), default=0)
    level_one_wrong = db.Column(db.Integer(), default=0)
    level_one_percentage = db.Column(db.Float(), default=0.0)

    level_two_right = db.Column(db.Integer(), default=0)
    level_two_wrong = db.Column(db.Integer(), default=0)
    level_two_percentage = db.Column(db.Float(), default=0.0)

    level_three_right = db.Column(db.Integer(), default=0)
    level_three_wrong = db.Column(db.Integer(), default=0)
    level_three_percentage = db.Column(db.Float(), default=0.0)

    level_four_right = db.Column(db.Integer(), default=0)
    level_four_wrong = db.Column(db.Integer(), default=0)
    level_four_percentage = db.Column(db.Float(), default=0.0)

    level_five_right = db.Column(db.Integer(), default=0)
    level_five_wrong = db.Column(db.Integer(), default=0)
    level_five_percentage = db.Column(db.Float(), default=0.0)

    level_six_right = db.Column(db.Integer(), default=0)
    level_six_wrong = db.Column(db.Integer(), default=0)
    level_six_percentage = db.Column(db.Float(), default=0.0)

    level_seven_right = db.Column(db.Integer(), default=0)
    level_seven_wrong = db.Column(db.Integer(), default=0)
    level_seven_percentage = db.Column(db.Float(), default=0.0)

    level_eight_right = db.Column(db.Integer(), default=0)
    level_eight_wrong = db.Column(db.Integer(), default=0)
    level_eight_percentage = db.Column(db.Float(), default=0.0)

    level_nine_right = db.Column(db.Integer(), default=0)
    level_nine_wrong = db.Column(db.Integer(), default=0)
    level_nine_percentage = db.Column(db.Float(), default=0.0)

    level_ten_right = db.Column(db.Integer(), default=0)
    level_ten_wrong = db.Column(db.Integer(), default=0)
    level_ten_percentage = db.Column(db.Float(), default=0.0)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
