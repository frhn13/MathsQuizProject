from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange

class AnswerForm(FlaskForm):
    answer = StringField(label="Answer: ", validators=[DataRequired()])
    submit = SubmitField(label="Submit Answer")

class TopicsForm(FlaskForm):
    operations = BooleanField(label="Operations")
    decimals = BooleanField(label="Fraction and Decimals")
    calculus = BooleanField(label="Calculus")
    equations = BooleanField(label="Equations")
    expressions = BooleanField(label="Expressions")
    sequences = BooleanField(label="Sequences")
    graphs = BooleanField(label="Graphs")
    basic_shapes = BooleanField(label="Basic Shapes")
    three_d_shapes = BooleanField(label="3D Shapes")
    trigonometry = BooleanField(label="Trigonometry and Pythagoreas")
    questions = IntegerField(label="Enter the number of questions to answers", validators=[DataRequired(), NumberRange(10, 50)])
    difficulty = IntegerField(label="Enter the starting difficulty of the questions", validators=[DataRequired(), NumberRange(1, 5)])
    submit = SubmitField(label="Submit Selection")
