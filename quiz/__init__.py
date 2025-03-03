from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "VerySecretKey" # Needed to display the form

from quiz import views