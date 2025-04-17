from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo
import re

class AnswerForm(FlaskForm):
    answer = StringField(label="Answer: ", validators=[DataRequired()])
    submit = SubmitField(label="Submit Answer")


class AnswerQuadraticEquationForm(FlaskForm):
    answer_x_1 = StringField(label="X1: ", validators=[DataRequired()])
    answer_x_2 = StringField(label="X2: ", validators=[DataRequired()])
    submit = SubmitField(label="Submit Answer")


class AnswerSimultaneousEquationForm(FlaskForm):
    answer_x = StringField(label="X: ", validators=[DataRequired()])
    answer_y = StringField(label="Y: ", validators=[DataRequired()])
    submit = SubmitField(label="Submit Answer")


class AnswerQuadraticSimultaneousEquationForm(FlaskForm):
    answer_x_1 = StringField(label="X1: ", validators=[DataRequired()])
    answer_x_2 = StringField(label="X2: ", validators=[DataRequired()])
    answer_y_1 = StringField(label="Y1: ", validators=[DataRequired()])
    answer_y_2 = StringField(label="Y2: ", validators=[DataRequired()])
    submit = SubmitField(label="Submit Answer")


class TopicsForm(FlaskForm):
    operations = BooleanField(label="Operations, Difficulty: 1-5")
    fractions = BooleanField(label="Fractions, Difficulty: 2-6")
    calculus = BooleanField(label="Calculus, Difficulty: 7-10")
    equations = BooleanField(label="Equations, Difficulty: 4-8")
    expressions = BooleanField(label="Expressions, Difficulty: 3-6")
    sequences = BooleanField(label="Sequences, Difficulty: 2-8")
    hcf_lcm = BooleanField(label="HCF, LCM and Prime Factors, Difficulty: 2-5")
    percentages = BooleanField(label="Percentages, Difficulty: 2-6")
    triangles = BooleanField(label="Triangles, Difficulty: 2-7")
    circles = BooleanField(label="Circles, Difficulty: 3-7")
    graphs = BooleanField(label="Graphs, Difficulty: 2-8")
    questions = IntegerField(label="Enter the number of questions to answers",
                             validators=[DataRequired(), NumberRange(10, 50)])
    difficulty = IntegerField(label="Enter the starting difficulty of the questions",
                              validators=[DataRequired(), NumberRange(1, 10)])
    submit = SubmitField(label="Submit Selection")


class RestartForm(FlaskForm):
    submit = SubmitField(label="Start New Quiz")


class RegisterForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired(), Length(4, 20)])
    email = StringField(label="Email Address:", validators=[DataRequired(), Length(4, 40), Email()])
    password = PasswordField(label="Password:", validators=[DataRequired(), Length(4, 20)])
    confirm_password = PasswordField(label="Confirm Password:", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Sign Up")


class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired(), Length(4, 20)])
    password = PasswordField(label="Password:", validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField(label="Login")


class ResultsForm(FlaskForm):
    results_returned = RadioField("Choose results to return:",
                                  choices=[("all", "All Results"),
                                           ("difficulty", "All results for a specific Difficulty"),
                                           ("topic", "All results for a specific Topic")], default="all")
    topic_chosen = SelectField(label="Select Topic: ",
                               choices=[("operations", "Operations"), ("fractions", "Fractions"),
                                        ("expressions", "Expressions"),
                                        ("equations", "Equations"), ("percentages", "Percentages"),
                                        ("sequences", "Sequences"),
                                        ("triangles", "Triangles"), ("calculus", "Calculus"),
                                        ("hcf_lcm", "HCF, LCM and Prime Factors"),
                                        ("circles", "Circles"), ("graphs", "Graphs")], default="operations")
    difficulty_chosen = IntegerField(label="Select Difficulty: ", validators=[NumberRange(1, 10)], default=5)
    user_chosen = SelectField(label="Select User: ")

    compare_results = BooleanField(label="Compare Results with Another Person?")
    second_user_chosen = SelectField(label="Select Second User: ")

    submit = SubmitField(label="Submit")

    def __init__(self, user_list):
        super().__init__()
        self.user_chosen.choices = user_list
        self.second_user_chosen.choices = user_list

class MaxResultsForm(FlaskForm):
    number_or_percentage_returned = RadioField(
                               choices=[("number", "Highest Number"),
                                        ("percentage", "Highest Percentage")], default="number")
    results_returned = RadioField("Choose results to return:",
                                  choices=[("all", "All Results"),
                                           ("difficulty", "All results for a specific Difficulty"),
                                           ("topic", "All results for a specific Topic")], default="all")
    topic_chosen = SelectField(label="Select Topic:",
                               choices=[("operations", "Operations"), ("fractions", "Fractions"),
                                        ("expressions", "Expressions"),
                                        ("equations", "Equations"), ("percentages", "Percentages"),
                                        ("sequences", "Sequences"),
                                        ("triangles", "Triangles"), ("calculus", "Calculus"),
                                        ("hcf_lcm", "HCF, LCM and Prime Factors"),
                                        ("circles", "Circles"), ("graphs", "Graphs")], default="operations")
    difficulty_chosen = IntegerField(label="Select Difficulty: ", validators=[NumberRange(1, 10)], default=5)

    submit = SubmitField(label="Submit")

    def __init__(self, new_label):
        super().__init__()
        self.number_or_percentage_returned.label.text = new_label
