from flask_login import UserMixin
import bcrypt

from quiz import db, login_manager

@login_manager.user_loader
def load_user(user_id): # Needed for logging in users
    return User.query.get(int(user_id))

# Model for the User table, contains all the attributes needed for a user account
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email = db.Column(db.String(length=40), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    # Has one-to-one relations with the tables storing the number of question the user got right or wrong for each
    # difficulty level and maths topic
    question_topics = db.relationship("QuestionTopics")
    question_difficulties = db.relationship("QuestionDifficulties")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        # Password is hashed and salted before it is stored in the DB
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# Model for the table that stores the number of questions a user got right or wrong for each maths topic
class QuestionTopics(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    operations_right = db.Column(db.Integer(), default=0)
    operations_wrong = db.Column(db.Integer(), default=0)

    expressions_right = db.Column(db.Integer(), default=0)
    expressions_wrong = db.Column(db.Integer(), default=0)

    fractions_right = db.Column(db.Integer(), default=0)
    fractions_wrong = db.Column(db.Integer(), default=0)

    equations_right = db.Column(db.Integer(), default=0)
    equations_wrong = db.Column(db.Integer(), default=0)

    sequences_right = db.Column(db.Integer(), default=0)
    sequences_wrong = db.Column(db.Integer(), default=0)

    hcf_lcm_right = db.Column(db.Integer(), default=0)
    hcf_lcm_wrong = db.Column(db.Integer(), default=0)

    percentages_right = db.Column(db.Integer(), default=0)
    percentages_wrong = db.Column(db.Integer(), default=0)

    calculus_right = db.Column(db.Integer(), default=0)
    calculus_wrong = db.Column(db.Integer(), default=0)

    triangles_right = db.Column(db.Integer(), default=0)
    triangles_wrong = db.Column(db.Integer(), default=0)

    circles_right = db.Column(db.Integer(), default=0)
    circles_wrong = db.Column(db.Integer(), default=0)

    graphs_right = db.Column(db.Integer(), default=0)
    graphs_wrong = db.Column(db.Integer(), default=0)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)

# Model for the table that stores the number of questions a user got right or wrong for each difficulty level
class QuestionDifficulties(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    level_one_right = db.Column(db.Integer(), default=0)
    level_one_wrong = db.Column(db.Integer(), default=0)

    level_two_right = db.Column(db.Integer(), default=0)
    level_two_wrong = db.Column(db.Integer(), default=0)

    level_three_right = db.Column(db.Integer(), default=0)
    level_three_wrong = db.Column(db.Integer(), default=0)

    level_four_right = db.Column(db.Integer(), default=0)
    level_four_wrong = db.Column(db.Integer(), default=0)

    level_five_right = db.Column(db.Integer(), default=0)
    level_five_wrong = db.Column(db.Integer(), default=0)

    level_six_right = db.Column(db.Integer(), default=0)
    level_six_wrong = db.Column(db.Integer(), default=0)

    level_seven_right = db.Column(db.Integer(), default=0)
    level_seven_wrong = db.Column(db.Integer(), default=0)

    level_eight_right = db.Column(db.Integer(), default=0)
    level_eight_wrong = db.Column(db.Integer(), default=0)

    level_nine_right = db.Column(db.Integer(), default=0)
    level_nine_wrong = db.Column(db.Integer(), default=0)

    level_ten_right = db.Column(db.Integer(), default=0)
    level_ten_wrong = db.Column(db.Integer(), default=0)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
