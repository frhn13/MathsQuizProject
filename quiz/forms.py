from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, FloatField, PasswordField
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
    operations = BooleanField(label="Operations")
    fractions = BooleanField(label="Fractions")
    calculus = BooleanField(label="Calculus")
    equations = BooleanField(label="Equations")
    expressions = BooleanField(label="Expressions")
    sequences = BooleanField(label="Sequences")
    hcf_lcm = BooleanField(label="HCF, LCM and Prime Factors")
    percentages = BooleanField(label="Percentages")
    triangles = BooleanField(label="Pythagoras and other Triangle Questions")
    questions = IntegerField(label="Enter the number of questions to answers", validators=[DataRequired(), NumberRange(10, 50)])
    difficulty = IntegerField(label="Enter the starting difficulty of the questions", validators=[DataRequired(), NumberRange(1, 10)])
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
