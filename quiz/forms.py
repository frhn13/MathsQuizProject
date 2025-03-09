from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange

class AnswerForm(FlaskForm):
    answer = StringField(label="Answer: ", validators=[DataRequired()])
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
    difficulty = IntegerField(label="Enter the starting difficulty of the questions", validators=[DataRequired(), NumberRange(1, 5)])
    submit = SubmitField(label="Submit Selection")

class RestartForm(FlaskForm):
    submit = SubmitField(label="Start New Quiz")
