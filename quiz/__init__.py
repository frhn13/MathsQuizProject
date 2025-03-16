from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .QuizCode.topic_manager import question_topic_selection

app = Flask(__name__)

app.config["SECRET_KEY"] = "VerySecretKey" # Needed to display the form
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maths_quiz.db"
db = SQLAlchemy(app) # Creates database
login_manager = LoginManager(app)

from quiz import views