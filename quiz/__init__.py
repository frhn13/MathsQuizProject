from flask import Flask
from .QuizCode.topic_manager import question_topic_selection

app = Flask(__name__)

app.config["SECRET_KEY"] = "VerySecretKey" # Needed to display the form

from quiz import views