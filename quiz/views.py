import matplotlib
import numpy as np
from matplotlib import patches
matplotlib.use("Agg")  # Use a backend that doesn't require the main thread
import matplotlib.pyplot as plt
from flask import render_template, redirect, url_for, request, flash, session, send_file
from sympy import sympify, factor, expand, simplify
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt
from io import BytesIO
from math import sin, cos

from quiz import app, db
from .QuizCode.min_and_max_difficulties import *
from quiz.forms import (RegisterForm, LoginForm, AnswerForm, TopicsForm, RestartForm, AnswerQuadraticEquationForm,
                        AnswerSimultaneousEquationForm, AnswerQuadraticSimultaneousEquationForm, ResultsForm,
                        MaxResultsForm)
from .QuizCode.topic_manager import question_topic_selection
from quiz.models import User, QuestionTopics, QuestionDifficulties
from quiz.update_results import update_topic_information, update_difficulty_information, get_user_results, \
    get_difficulty_results, get_topic_results


@app.route("/", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_anonymous:
        form = RegisterForm()
        if form.validate_on_submit():
            preexisting_username = User.query.filter_by(username=form.username.data).first()
            preexisting_email = User.query.filter_by(email=form.email.data).first()
            if not preexisting_username and not preexisting_email:
                created_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
                db.session.add(created_user)
                db.session.commit()
                question_topics = QuestionTopics(user_id=created_user.id)
                question_difficulties = QuestionDifficulties(user_id=created_user.id)
                db.session.add(question_topics)
                db.session.add(question_difficulties)
                db.session.commit()
                login_user(created_user)
                flash("Account creation successful!", category="success")
                return redirect(url_for("quiz_selection"))
            else:
                flash("Account already exists with that username or email.", category="danger")

        return render_template("register.html", form=form)
    else:
        flash("This page cannot be accessed if you are logged in.", category="warning")
        return redirect(url_for("quiz_selection"))

@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You are now logged out.", category="info")
    return redirect(url_for("register_page"))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            user_logging_in = User.query.filter_by(username=form.username.data).first()
            if user_logging_in and bcrypt.checkpw(form.password.data.encode("utf-8"), user_logging_in.password):
                login_user(user_logging_in)
                flash("Login successful!", category="success")
                return redirect(url_for("quiz_selection"))
            else:
                flash("Your login details are invalid.", category="danger")
                return redirect(url_for("login_page"))
        return render_template("login.html", form=form)
    else:
        flash("This page cannot be accessed if you are logged in.", category="warning")
        return redirect(url_for("quiz_selection"))

@app.route("/remove")
def remove_page():
    session.pop("final_question", None)
    session.pop("final_answer", None)
    session.pop("final_difficulty_weighting", None)
    session.pop("multiple_answers", None)
    session.pop("current_topic", None)
    session.pop("current_difficulty", None)
    session.pop("difficulty_range", None)
    session.pop("score", None)
    return redirect(url_for("quiz_selection"))

@app.route("/end-quiz", methods=["GET", "POST"])
@login_required
def end_quiz():
    form = RestartForm()
    if request.method == "POST":
        return redirect(url_for("quiz_selection"))
    number_of_questions = session.get("number_of_questions")
    score = session.get("score")
    return render_template("end_quiz.html", form=form, number_of_questions=number_of_questions, score=score)


@app.route("/quiz-selection", methods=["GET", "POST"])
@login_required
def quiz_selection():
    form = TopicsForm()

    session.pop("topic_selection", None)
    session.pop("number_of_questions", None)
    session.pop("question_number", None)
    session.pop("final_question", None)
    session.pop("final_answer", None)
    session.pop("final_difficulty_weighting", None)
    session.pop("multiple_answers", None)
    session.pop("calculator_needed", None)
    session.pop("time_needed", None)
    session.pop("current_topic", None)
    session.pop("current_difficulty", None)
    session.pop("difficulty_range", None)
    session.pop("max_difficulty", None)
    session.pop("min_difficulty", None)
    session.pop("score", None)
    session.pop("difficulty_counter", None)
    session.pop("topic_counter", None)
    session.pop("image_values", None)
    session.pop("image_added", None)
    session.pop("graph_values", None)
    session.pop("graph_added", None)
    session.pop("circle_image_values", None)
    session.pop("circle_image_added", None)
    session.pop("circle_image_added", None)
    session["max_difficulty"] = 0
    session["min_difficulty"] = 10

    if request.method == "POST":
        topics_chosen = []
        if request.form.get("operations") is not None:
            topics_chosen.append("operations")
            if session["max_difficulty"] < operations[1]:
                session["max_difficulty"] = operations[1]
            if session["min_difficulty"] > operations[0]:
                session["min_difficulty"] = operations[0]
        if request.form.get("fractions") is not None:
            topics_chosen.append("fractions")
            if session["max_difficulty"] < fractions[1]:
                session["max_difficulty"] = fractions[1]
            if session["min_difficulty"] > fractions[0]:
                session["min_difficulty"] = fractions[0]
        if request.form.get("calculus") is not None:
            topics_chosen.append("calculus")
            if session["max_difficulty"] < calculus[1]:
                session["max_difficulty"] = calculus[1]
            if session["min_difficulty"] > calculus[0]:
                session["min_difficulty"] = calculus[0]
        if request.form.get("equations") is not None:
            topics_chosen.append("equations")
            if session["max_difficulty"] < equations[1]:
                session["max_difficulty"] = equations[1]
            if session["min_difficulty"] > equations[0]:
                session["min_difficulty"] = equations[0]
        if request.form.get("expressions") is not None:
            topics_chosen.append("expressions")
            if session["max_difficulty"] < expressions[1]:
                session["max_difficulty"] = expressions[1]
            if session["min_difficulty"] > expressions[0]:
                session["min_difficulty"] = expressions[0]
        if request.form.get("sequences") is not None:
            topics_chosen.append("sequences")
            if session["max_difficulty"] < sequences[1]:
                session["max_difficulty"] = sequences[1]
            if session["min_difficulty"] > sequences[0]:
                session["min_difficulty"] = sequences[0]
        if request.form.get("hcf_lcm") is not None:
            topics_chosen.append("hcf_lcm")
            if session["max_difficulty"] < hcf_lcm[1]:
                session["max_difficulty"] = hcf_lcm[1]
            if session["min_difficulty"] > hcf_lcm[0]:
                session["min_difficulty"] = hcf_lcm[0]
        if request.form.get("percentages") is not None:
            topics_chosen.append("percentages")
            if session["max_difficulty"] < percentages[1]:
                session["max_difficulty"] = percentages[1]
            if session["min_difficulty"] > percentages[0]:
                session["min_difficulty"] = percentages[0]
        if request.form.get("triangles") is not None:
            topics_chosen.append("triangles")
            if session["max_difficulty"] < triangles[1]:
                session["max_difficulty"] = triangles[1]
            if session["min_difficulty"] > triangles[0]:
                session["min_difficulty"] = triangles[0]
        if request.form.get("circles") is not None:
            topics_chosen.append("circles")
            if session["max_difficulty"] < circles[1]:
                session["max_difficulty"] = circles[1]
            if session["min_difficulty"] > circles[0]:
                session["min_difficulty"] = circles[0]
        if request.form.get("graphs") is not None:
            topics_chosen.append("graphs")
            if session["max_difficulty"] < graphs[1]:
                session["max_difficulty"] = graphs[1]
            if session["min_difficulty"] > graphs[0]:
                session["min_difficulty"] = graphs[0]

        if len(topics_chosen) == 0:
            flash("Please select a topic.", category="danger")
            # return redirect(url_for("quiz_selection"))
        elif int(request.form.get("difficulty")) > session["max_difficulty"]:
            flash("The difficulty selected is too high for the chosen topics.", category="danger")
        elif int(request.form.get("difficulty")) < session["min_difficulty"]:
            flash("The difficulty selected is too low for the chosen topics.", category="danger")
        else:
            session["difficulty_counter"] = {
                f"level_{x}": [0, 0] for x in range(1, 11)
            }
            session["topic_counter"] = {
                "operations": [0, 0],
                "expressions": [0, 0],
                "equations": [0, 0],
                "fractions": [0, 0],
                "sequences": [0, 0],
                "hcf_lcm": [0, 0],
                "percentages": [0, 0],
                "calculus": [0, 0],
                "triangles": [0, 0],
                "circles": [0, 0],
                "graphs": [0, 0]
            }

            session["topic_selection"] = topics_chosen
            session["current_difficulty"] = int(request.form.get("difficulty"))
            session["number_of_questions"] = int(request.form.get("questions"))
            session["question_number"] = 1
            session["difficulty_range"] = 0
            session["score"] = 0
            print(session.get("topic_selection"))
            return redirect(url_for("quiz_page"))

    return render_template("quiz_selection.html", form=form)

@app.route("/image")
def get_image():
    point_a = session["image_values"].get("point_a")
    point_b = session["image_values"].get("point_b")
    point_c = session["image_values"].get("point_c")
    length_a = session["image_values"].get("length_a")
    length_b = session["image_values"].get("length_b")
    length_c = session["image_values"].get("length_c")
    angle_a = session["image_values"].get("angle_a")
    angle_b = session["image_values"].get("angle_b")
    angle_c = session["image_values"].get("angle_c")
    question_topic = session["image_values"].get("question_topic")
    question_subtopic = session["image_values"].get("question_subtopic")

    print(f"{question_topic} {question_subtopic}")

    x_coordinates = [point_a[0], point_b[0], point_c[0], point_a[0]]
    y_coordinates = [point_a[1], point_b[1], point_c[1], point_a[1]]

    plt.figure(figsize=(30, 20))

    if question_topic == "pythagoras":
        if question_subtopic == "missing_side":
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, "x", fontsize="20")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")
        else:
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, f"Side a = {length_a:.2f}cm", fontsize="20")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, "x", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")
    elif question_topic == "trigonometry":
        if question_subtopic == "missing_side":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, "x", fontsize="20")
        else:
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")
    elif question_topic == "sine_cosine_area":
        if question_subtopic == "sine_side":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, "x", fontsize="20")
        elif question_subtopic == "sine_angle":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")
        elif question_subtopic == "cosine_side":
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, "x", fontsize="20")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")
        elif question_subtopic == "cosine_angle":
            plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, f"Side a = {length_a:.2f}cm", fontsize="20")
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")
        elif question_subtopic == "area":
            plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
            plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")

    else:
        plt.text((point_b[0] + point_c[0]) / 2, (point_b[1] + point_c[1]) / 2, f"Side a = {length_a:.2f}cm", fontsize="20")
        plt.text((point_a[0] + point_c[0]) / 2, (point_a[1] + point_c[1]) / 2, f"Side b = {length_b:.2f}cm", fontsize="20")
        plt.text((point_b[0] + point_a[0]) / 2, (point_b[1] + point_a[1]) / 2, f"Side c = {length_c:.2f}cm", fontsize="20")

    if question_topic == "simple_angles":
        plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°", fontsize="20")
        plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°", fontsize="20")
        plt.text(point_c[0], point_c[1], "x", fontsize="20")
    elif question_topic == "trigonometry":
        if question_subtopic == "missing_side":
            plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°", fontsize="20")
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°", fontsize="20")
        else:
            plt.text(point_a[0], point_a[1], "x", fontsize="20")
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°", fontsize="20")
    elif question_topic == "sine_cosine_area":
        if question_subtopic == "sine_side":
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°", fontsize="20")
            plt.text(point_c[0], point_c[1], f"Angle C = {angle_c:.2f}°", fontsize="20")
        elif question_subtopic == "sine_angle":
            plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°", fontsize="20")
            plt.text(point_c[0], point_c[1], "x", fontsize="20")
        elif question_subtopic == "cosine_side":
            plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°", fontsize="20")
        elif question_subtopic == "cosine_angle":
            plt.text(point_a[0], point_a[1], "x", fontsize="20")
        elif question_subtopic == "area":
            plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°", fontsize="20")
    else:
        plt.text(point_a[0], point_a[1], f"Angle A = {angle_a:.2f}°", fontsize="20")
        plt.text(point_b[0], point_b[1], f"Angle B = {angle_b:.2f}°", fontsize="20")
        plt.text(point_c[0], point_c[1], f"Angle C = {angle_c:.2f}°", fontsize="20")

    plt.gca().set_aspect("equal", adjustable="box")
    plt.axis("off")
    plt.plot(x_coordinates, y_coordinates, color="blue", linestyle="-", marker=".")
    # Adapted from https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    triangle_img = BytesIO()
    plt.savefig(triangle_img, format="png")
    triangle_img.seek(0)
    plt.close()
    return send_file(triangle_img, mimetype="image/png")

@app.route("/circle-image")
def get_circle_image():
    radius = session["circle_image_values"].get("radius")
    angle = session["circle_image_values"].get("angle")
    question_topic = session["circle_image_values"].get("question_topic")
    use_diameter = session["circle_image_values"].get("use_diameter")

    # Adapted from https://www.youtube.com/watch?v=i7ATPhd0nwc
    fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
    ax.set_aspect("equal")
    ax.set_xlim(-radius - 1, radius + 1)
    ax.set_ylim(-radius - 1, radius + 1)

    sector = patches.Wedge((0, 0), radius, 0, angle, color="lightblue", edgecolor="black")

    angle1_rad = np.radians(0)
    angle2_rad = np.radians(angle)
    sector_1 = (radius * cos(angle1_rad), radius * sin(angle1_rad))
    sector_2 = (radius * cos(angle2_rad), radius * sin(angle2_rad))

    circle = plt.Circle((0, 0), radius=radius, color="blue", fill=False)
    if not use_diameter:
        ax.plot([0, radius], [0, 0], linestyle="--", color="blue")
        ax.text(radius / 1.5, 0.5, f"r = {radius}",
                fontsize=10)
    else:
        ax.plot([-radius, radius], [0, 0], linestyle="--", color="blue")
        ax.text(radius / 1.5, 0.5, f"d = {radius * 2}",
                fontsize=10)

    if question_topic in ("sector", "arc", "area_of_shaded_area"):
        ax.text(0, 0.5, f"{angle}°", fontsize=10)
        ax.add_patch(sector)

    if question_topic == "area_of_shaded_area":
        ax.plot([sector_1[0], sector_2[0]], [sector_1[1], sector_2[1]], linestyle="-", color="black")

    ax.add_patch(circle)
    ax.axis("off")

    # Adapted from https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    circle_image = BytesIO()
    plt.savefig(circle_image, format="png", bbox_inches="tight")
    circle_image.seek(0)
    plt.close()
    return send_file(circle_image, mimetype="image/png")

@app.route("/graph")
def get_graph():
    time_values = session["graph_values"].get("time_values")
    distance_values = session["graph_values"].get("distance_values")
    speed_values = session["graph_values"].get("speed_values")
    pie_chart_values = session["graph_values"].get("pie_chart_values")
    pie_chart_labels = session["graph_values"].get("pie_chart_labels")
    graph_values = {
        "time_values": session["graph_values"].get("time_values"),
        "distance_values": session["graph_values"].get("distance_values"),
        "speed_values": session["graph_values"].get("speed_values"),
        "pie_chart_values": session["graph_values"].get("pie_chart_values"),
        "pie_chart_labels": session["graph_values"].get("pie_chart_labels")
    }

    # plt.figure(figsize=(20, 20))

    if distance_values != []:
        plt.gca().set_aspect("equal", adjustable="box")
        plt.plot(time_values, distance_values, linestyle="-", marker=".", color="blue")
        plt.xlabel("Time in Minutes")
        plt.ylabel("Distance")
        plt.grid()
        # Adapted from https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        graph_image = BytesIO()
        plt.savefig(graph_image, format="png")
        graph_image.seek(0)
        plt.close()
    elif speed_values != []:
        plt.gca().set_aspect("equal", adjustable="box")
        plt.plot(time_values, speed_values, linestyle="-", marker=".", color="blue")
        plt.xlabel("Time in Seconds")
        plt.ylabel("Speed")
        plt.grid()
        # Adapted from https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        graph_image = BytesIO()
        plt.savefig(graph_image, format="png")
        graph_image.seek(0)
        plt.close()
    elif pie_chart_values != []:
        def angle_generation(percentage):
            angle = (percentage / 100) * 360
            return f"{angle:.0f}°"

        plt.gca().set_aspect("equal", adjustable="box")
        plt.pie(pie_chart_values, labels=pie_chart_labels, startangle=90,
                wedgeprops={"edgecolor": "black"}, autopct=angle_generation)
        # Adapted from https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        graph_image = BytesIO()
        plt.savefig(graph_image, format="png", bbox_inches="tight")
        graph_image.seek(0)
        plt.close()

    return send_file(graph_image, mimetype="image/png")


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz_page():
    if "topic_selection" not in session:
        flash("You must make a quiz before starting one.", category="danger")
        return redirect(url_for("quiz_selection"))
    else:
        form = AnswerForm()
        difficulty_boundary = 30
        if "final_answer" not in session:
            topic, question, answer, difficulty_weighting, multiple_answers, image_values, graph_values, circle_image_values, \
                calculator_needed, time_needed = question_topic_selection(session.get("topic_selection"), int(session.get("current_difficulty")),
    ["free_text", "multiple-choice", "true/false"])
            session["current_topic"] = topic
            session["final_answer"] = answer
            session["final_question"] = question
            session["final_difficulty_weighting"] = difficulty_weighting
            session["multiple_answers"] = multiple_answers
            session["calculator_needed"] = calculator_needed
            session["time_needed"] = time_needed
            if image_values is not None:
                session["image_values"] = image_values
                session["image_added"] = True
            else:
                session.pop("image_values", None)
                session.pop("image_added", None)
            if graph_values is not None:
                session["graph_values"] = graph_values
                session["graph_added"] = True
            else:
                session.pop("graph_values", None)
                session.pop("graph_added", None)
            if circle_image_values is not None:
                session["circle_image_values"] = circle_image_values
                session["circle_image_added"] = True
            else:
                session.pop("circle_image_values", None)
                session.pop("circle_image_added", None)

        if session["multiple_answers"] == "No":
            form = AnswerForm()
        if session["multiple_answers"] == "TwoSame":
            form = AnswerQuadraticEquationForm()
        if session["multiple_answers"] == "TwoDifferent":
            form = AnswerSimultaneousEquationForm()
        if session["multiple_answers"] == "FourDifferent":
            form = AnswerQuadraticSimultaneousEquationForm()

        final_answer = session.get("final_answer")
        final_question = session.get("final_question")
        print(final_answer)

        answer_timeout = False
        if request.method == "POST":
            answer = 0
            match session["multiple_answers"]:
                case "No":
                    answer = request.form.get("answer")
                    if answer == "timeout":
                        answer_timeout = True
                case "TwoSame":
                    answer_x_1 = request.form.get("answer_x_1")
                    if answer_x_1 == "timeout":
                        answer_timeout = True
                case "TwoDifferent":
                    answer_x = request.form.get("answer_x")
                    if answer_x == "timeout":
                        answer_timeout = True
                case "FourDifferent":
                    answer_x_1 = request.form.get("answer_x_1")
                    if answer_x_1 == "timeout":
                        answer_timeout = True

            if not answer_timeout:
                match session["current_topic"]:
                    case "equations":
                        match session["multiple_answers"]:
                            case "No":
                                answer = request.form.get("answer")
                                if not answer.replace(".", "").replace("-", "").isnumeric():
                                    flash("You must enter a number. Try again.", category="danger")
                                    return redirect(url_for("quiz_page"))
                                answer = float(answer)

                            case "TwoSame":
                                answer_x_1 = request.form.get("answer_x_1")
                                answer_x_2 = request.form.get("answer_x_2")

                                if (not answer_x_1.replace(".", "").replace("-","").isnumeric() or
                                        not answer_x_2.replace(".", "").replace("-","").isnumeric()):
                                    flash("You must enter a number. Try again.", category="danger")
                                    return redirect(url_for("quiz_page"))
                                answer = [float(answer_x_1), float(answer_x_2)]

                            case "TwoDifferent":
                                answer_x = request.form.get("answer_x")
                                answer_y = request.form.get("answer_y")

                                if (not answer_x.replace(".", "").replace("-","").isnumeric() or
                                        not answer_y.replace(".", "").replace("-","").isnumeric()):
                                    flash("You must enter a number. Try again.", category="danger")
                                    return redirect(url_for("quiz_page"))
                                answer = [float(answer_x), float(answer_y)]
                            case "FourDifferent":
                                answer_x_1 = request.form.get("answer_x_1")
                                answer_x_2 = request.form.get("answer_x_2")
                                answer_y_1 = request.form.get("answer_y_1")
                                answer_y_2 = request.form.get("answer_y_2")

                                if (not answer_x_1.replace(".", "").replace("-","").isnumeric() or
                                        not answer_x_2.replace(".", "").replace("-","").isnumeric()
                                        or not answer_y_1.replace(".", "").replace("-","").isnumeric()
                                        or not answer_y_2.replace(".", "").replace("-","").isnumeric()):
                                    flash("You must enter a number. Try again.", category="danger")
                                    return redirect(url_for("quiz_page"))
                                answer = [float(answer_x_1), float(answer_x_2), float(answer_y_1), float(answer_y_2)]
                            case _:
                                pass

                    case "fractions":
                        answer = request.form.get("answer")
                        if final_answer in ("True", "False") and answer not in ("True", "False"):
                            flash("You must enter True or False. Try again", category="danger")
                            return redirect(url_for("quiz_page"))
                        elif type(final_answer) == str and not "/" in answer and final_answer not in ("True", "False"):
                            flash("You must write your answer as a fraction. Try again.", category="danger")
                            return redirect(url_for("quiz_page"))
                        elif final_answer == str and "x" in final_answer:
                            if "/" in answer:
                                final_answer = str(simplify(sympify(final_answer)))
                                # answer = simplify(sympify(answer))
                            else:
                                flash("You must write your answer as a fraction. Try again.", category="danger")
                                return redirect(url_for("quiz_page"))
                        else:
                            final_answer = str(final_answer)

                    case "expressions":
                        answer = request.form.get("answer")
                        if final_answer in ("True", "False") and answer not in ("True", "False"):
                            flash("You must enter True or False. Try again", category="danger")
                            return redirect(url_for("quiz_page"))
                        else:
                            if not answer.isnumeric() and "x" not in answer:
                                flash("Expression must include an x. Try again.", category="danger")
                                return redirect(url_for("quiz_page"))
                            elif ("(" in answer or ")" in answer) and "(" not in final_answer:
                                flash("Expression must be expanded, so no brackets. Try again.", category="danger")
                                return redirect(url_for("quiz_page"))
                            elif "(" in final_answer and "(" not in answer and ")" not in answer:
                                flash("Expression must be factorised. Try again.", category="danger")
                                return redirect(url_for("quiz_page"))
                            else:
                                for x in range(len(answer)):
                                    if x < len(answer) - 1 and answer[x].isnumeric() and (answer[x+1] == "x" or answer[x+1] == "("):
                                        answer = f"{answer[0:x+1]}*{answer[x+1:]}"
                                    elif x < len(answer) - 1 and answer[x] == "x" and answer[x+1] == "(":
                                        answer = f"{answer[0:x + 1]}*{answer[x + 1:]}"
                                    elif x < len(answer) - 1 and answer[x] == "x" and answer[x+1].isnumeric():
                                        answer = f"{answer[0:x+1]}**{answer[x+1:]}"
                                    elif x < len(answer) - 1 and answer[x] == "x" and answer[x+1] == "^":
                                        answer = f"{answer[0:x+1]}**{answer[x+2:]}"
                                print(answer)
                                print(final_answer)
                            try:
                                answer = sympify(answer)
                                final_answer = sympify(final_answer)
                            except Exception:
                                pass

                    case "calculus":
                        answer = request.form.get("answer")
                        if not final_answer.isnumeric() and "y" not in final_answer:
                            for x in range(len(answer)):
                                if x < len(answer) - 1 and answer[x].isnumeric() and (
                                        answer[x + 1] == "x" or answer[x + 1] == "("):
                                    answer = f"{answer[0:x + 1]}*{answer[x + 1:]}"
                                elif x < len(answer) - 1 and answer[x] == "x" and answer[x + 1] == "(":
                                    answer = f"{answer[0:x + 1]}*{answer[x + 1:]}"
                                elif x < len(answer) - 1 and answer[x] == "x" and answer[x + 1].isnumeric():
                                    answer = f"{answer[0:x + 1]}**{answer[x + 1:]}"
                                elif x < len(answer) - 1 and answer[x] == "x" and answer[x + 1] == "^":
                                    answer = f"{answer[0:x + 1]}**{answer[x + 2:]}"
                            print(answer)
                            print(final_answer)
                            try:
                                answer = sympify(answer)
                                final_answer = sympify(final_answer)
                            except Exception:
                                pass
                        else:
                            final_answer = final_answer.replace(" ", "")
                            answer = answer.replace(" ", "")

                    case "graphs":
                        answer = request.form.get("answer")
                        try:
                            answer = request.form.get("answer")
                            if type(final_answer) == int:
                                answer = int(answer)
                            elif type(final_answer) == float:
                                answer = float(answer)
                            else:
                                if "y=" in final_answer or "y =" in final_answer:
                                    final_answer = final_answer.replace(" ", "")
                                    answer = answer.replace(" ", "")
                        except Exception:
                            flash("You must enter a number. Try again.", category="danger")
                            return redirect(url_for("quiz_page"))

                    case "hcf_lcm":
                        answer = request.form.get("answer")
                        total_number = ""
                        final_answer_str = ""
                        try:
                            if type(final_answer) == int:
                                answer = int(answer)
                            elif type(final_answer) == dict:
                                answer = answer.replace(" ", "")
                                numbers_dict = {}
                                for x, character in enumerate(answer):
                                    if not character.isnumeric() and character.lower() not in ("x", "*"):
                                        flash("You must list the multiplication of prime factors like a x b x c. Try again.", category="danger")
                                        return redirect(url_for("quiz_page"))
                                    elif character.isnumeric():
                                        total_number += character
                                        if x+1 == len(answer) or (x+1 < len(answer) and answer[x+1].lower() in ("x", "*")):
                                            if total_number not in numbers_dict:
                                                numbers_dict[total_number] = 1
                                            else:
                                                numbers_dict[total_number] += 1
                                            total_number = ""
                                for number in numbers_dict:
                                    if number not in final_answer:
                                        answer = ""
                                        break
                                    elif numbers_dict[number] != final_answer[number]:
                                        answer = ""
                                        break

                                for number in final_answer:
                                    for x in range(final_answer[number]):
                                        final_answer_str += f"{number}x"
                                final_answer_str = final_answer_str[0:-1]
                                final_answer = final_answer_str

                                if answer != "":
                                    answer = final_answer
                            else:
                                if final_answer in ("True", "False") and answer not in ("True", "False"):
                                    flash("You must enter True or False. Try again", category="danger")
                                    return redirect(url_for("quiz_page"))
                        except Exception:
                            flash("You must enter a number. Try again.", category="danger")
                            return redirect(url_for("quiz_page"))

                    case _:
                        try:
                            answer = request.form.get("answer")
                            if type(final_answer) == int:
                                answer = int(answer)
                            elif type(final_answer) == float:
                                answer = float(answer)
                            else:
                                if final_answer in ("True", "False") and answer not in ("True", "False"):
                                    flash("You must enter True or False. Try again", category="danger")
                                    return redirect(url_for("quiz_page"))
                                else:
                                    pass
                        except Exception:
                            flash("You must enter a number. Try again.", category="danger")
                            return redirect(url_for("quiz_page"))


            if answer_timeout:
                session["topic_counter"][session["current_topic"]][1] += 1
                difficulty_counter = session["difficulty_counter"]
                difficulty_counter[f"level_{session['current_difficulty']}"][1] += 1
                session["difficulty_counter"] = difficulty_counter

                print("Timeout")
                if session["current_difficulty"] > session["min_difficulty"]:
                    session["difficulty_range"] -= 1
                    if session["difficulty_range"] <= -5:
                        session["current_difficulty"] -= 1
                        session["difficulty_range"] = 0
                else:
                    session["difficulty_range"] = 0
                flash(f"You took too long to answer the question! The correct answer was {final_answer}.", category="danger")

            elif (answer == final_answer or (type(final_answer) == list and (len(final_answer) == 1 and answer == final_answer[0])) or
                     (type(answer) == list and type(final_answer) == list and
                     ((len(answer) == 2 and answer[0] == final_answer[0] and answer[1] == final_answer[1])
                or (len(answer) == 2 and answer[0] == final_answer[1] and answer[1] == final_answer[0] and session["multiple_answers"] == "TwoSame")
                or (len(answer) == 4 and (answer[0] == final_answer[0] and answer[1] == final_answer[0] or (answer[0] == final_answer[1] and answer[1] == final_answer[0]))
                and (answer[2] == final_answer[2] and answer[3] == final_answer[3] or (answer[2] == final_answer[3] and answer[3] == final_answer[2])))))):
                session["score"] += 1
                session["topic_counter"][session["current_topic"]][0] += 1
                difficulty_counter = session["difficulty_counter"]
                difficulty_counter[f"level_{session['current_difficulty']}"][0] += 1
                session["difficulty_counter"] = difficulty_counter

                print("Correct")
                if session["current_difficulty"] < session["max_difficulty"]:
                    session["difficulty_range"] += 1
                    if session["difficulty_range"] >= 5:
                        session["current_difficulty"] += 1
                        session["difficulty_range"] = 0
                else:
                    session["difficulty_range"] = 0
                flash(f"Well done! You got it right!", category="success")

            else:
                session["topic_counter"][session["current_topic"]][1] += 1
                difficulty_counter = session["difficulty_counter"]
                difficulty_counter[f"level_{session['current_difficulty']}"][1] += 1
                session["difficulty_counter"] = difficulty_counter

                print("Incorrect")
                if session["current_difficulty"] > session["min_difficulty"]:
                    session["difficulty_range"] -= 1
                    if session["difficulty_range"] <= -5:
                        session["current_difficulty"] -= 1
                        session["difficulty_range"] = 0
                else:
                    session["difficulty_range"] = 0
                flash(f"You got it wrong! The correct answer is {final_answer}.", category="danger")

            print(f"Weighting: {session.get('final_difficulty_weighting')}")
            print(f"Current difficulty: {session.get('current_difficulty')}")
            print(f"Difficulty range: {session.get('difficulty_range')}")

            session["question_number"] += 1
            session.pop("final_question", None)
            session.pop("final_answer", None)
            session.pop("final_difficulty_weighting", None)
            session.pop("multiple_answers", None)
            session.pop("current_topic", None)

            if session["question_number"] > session["number_of_questions"]:
                print(session["topic_counter"])
                print(session["difficulty_counter"])
                update_topic_information(session["topic_counter"])
                update_difficulty_information(session["difficulty_counter"])
                # question_topics = QuestionTopics.query.filter_by(user_id=current_user.id).first()

                return redirect(url_for("end_quiz"))

            return redirect(url_for("quiz_page"))

        current_difficulty = session.get("current_difficulty")
        score = session.get("score")
        question_number = session.get("question_number")
        multiple_answers = session.get("multiple_answers")
        image_added = session.get("image_added")
        graph_added = session.get("graph_added")
        circle_image_added = session.get("circle_image_added")
        calculator_needed = session.get("calculator_needed")
        max_difficulty = session.get("max_difficulty")
        min_difficulty = session.get("min_difficulty")
        time_needed = session.get("time_needed")
        return render_template("quiz.html", form=form, final_question=final_question,
                               current_difficulty=current_difficulty, score=score, question_number=question_number,
                               multiple_answers=multiple_answers, image_added=image_added, graph_added=graph_added,
                               circle_image_added=circle_image_added, calculator_needed=calculator_needed,
                               max_difficulty=max_difficulty, min_difficulty=min_difficulty, time_needed=time_needed)

@app.route("/get-results-graph")
@login_required
def get_results_graph():
    user = User.query.filter_by(username=session["username"]).first()
    second_user = User.query.filter_by(username=session["second_username"]).first()
    match session["graph_type"]:
        case "all":
            answer_correct, answer_incorrect, answer_percentage = get_user_results(user)
            if session["compare_results"]:
                answer_correct_2, answer_incorrect_2, answer_percentage_2 = get_user_results(second_user)
                y_axis_2 = [answer_correct_2, answer_incorrect_2]
                plt.title(f"Number of questions {session['username']} and {session['second_username']} got right and wrong")
            else:
                plt.title(f"Number of questions {session['username']} got right and wrong")

            x_axis = ["Correct Answers", "Incorrect Answers"]
            y_axis = [answer_correct, answer_incorrect]
            plt.xlabel("Right or Wrong")
            plt.ylabel("Number of Questions")

        case "difficulty":
            answer_correct, answer_incorrect, answer_percentage = get_difficulty_results(user, session["difficulty"])
            if session["compare_results"]:
                answer_correct_2, answer_incorrect_2, answer_percentage_2 = get_difficulty_results(second_user, session["difficulty"])
                y_axis_2 = [answer_correct_2, answer_incorrect_2]
                plt.title(f"Number of questions {session['username']} and {session['second_username']} got right and wrong on Difficulty {session['difficulty']}")
            else:
                plt.title(f"Number of questions {session['username']} got right and wrong on Difficulty {session['difficulty']}")

            x_axis = ["Correct Answers", "Incorrect Answers"]
            y_axis = [answer_correct, answer_incorrect]
            plt.xlabel("Right or Wrong")
            plt.ylabel("Number of Questions")

        case "topic":
            answer_correct, answer_incorrect, answer_percentage = get_topic_results(user, session["topic"])
            if session["compare_results"]:
                answer_correct_2, answer_incorrect_2, answer_percentage_2 = get_topic_results(second_user, session["topic"])
                y_axis_2 = [answer_correct_2, answer_incorrect_2]
                if session["topic"] == "hcf_lcm":
                    plt.title(
                        f"Number of HCF, LCM and prime factors questions {session['username']} and {session['second_username']} got right and wrong")
                else:
                    plt.title(f"Number of {session['topic']} questions {session['username']} and {session['second_username']} got right and wrong")
            else:
                if session["topic"] == "hcf_lcm":
                    plt.title(
                        f"Number of HCF, LCM and prime factors questions {session['username']} got right and wrong")
                else:
                    plt.title(
                        f"Number of {session['topic']} questions {session['username']} got right and wrong")

            x_axis = ["Correct Answers", "Incorrect Answers"]
            y_axis = [answer_correct, answer_incorrect]
            plt.xlabel("Right or Wrong")
            plt.ylabel("Number of Questions")
            if session["topic"] == "hcf_lcm":
                plt.title(f"Number of HCF, LCM and prime factors questions {session['username']} got right and wrong")
            else:
                plt.title(f"Number of {session['topic']} questions {session['username']} got right and wrong")

        case _:
            answer_correct, answer_incorrect, answer_percentage = get_user_results(current_user)
            if session["compare_results"]:
                pass
            x_axis = ["Correct Answers", "Incorrect Answers"]
            y_axis = [answer_correct, answer_incorrect]
            plt.xlabel("Right or Wrong")
            plt.ylabel("Number of Questions")
            plt.title(f"Number of questions you got right and wrong")

    if session["compare_results"]:
        # Adapted from https://www.youtube.com/watch?v=ZjQCPMO7LBE
        bar_1 = np.arange(len(x_axis))
        bar_2 = [x+0.5 for x in bar_1]
        bars_1 = plt.bar(bar_1, y_axis, 0.5, label=session["username"], align='center')
        bars_2 = plt.bar(bar_2, y_axis_2, 0.5, label=session["second_username"], align='center')
        plt.bar_label(bars_1, fmt="%d", padding=10, label_type="center")
        plt.bar_label(bars_2, fmt="%d", padding=10, label_type="center")
        plt.xticks(bar_1, x_axis)
        plt.legend()
    else:
        bars = plt.bar(x_axis, y_axis)
        plt.bar_label(bars, fmt="%d", padding=10, label_type="center")
    # Adapted from https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    graph_image = BytesIO()
    plt.savefig(graph_image, format="png")
    graph_image.seek(0)
    plt.close()

    return send_file(graph_image, mimetype="image/png")

@app.route("/get-max-results-graph")
@login_required
def get_max_results_graph():
    users = User.query.all()
    user_results = []

    plt.title("Top 5 Users with the Highest Number of Correct Answers")
    plt.figure(figsize=(10, 10))

    match session["graph_type"]:
        case "all":
            for user in users:
                answer_correct, answer_incorrect, answer_percentage = get_user_results(user)
                user_results.append([user.username, answer_correct, answer_incorrect, answer_percentage])
        case "difficulty":
            for user in users:
                answer_correct, answer_incorrect, answer_percentage = get_difficulty_results(user, session["difficulty"])
                user_results.append([user.username, answer_correct, answer_incorrect, answer_percentage])
        case "topic":
            for user in users:
                answer_correct, answer_incorrect, answer_percentage = get_topic_results(user, session["topic"])
                user_results.append([user.username, answer_correct, answer_incorrect, answer_percentage])

    if session["number_or_percentage"] == "number":
        user_results.sort(key=lambda x: x[1], reverse=True)
        plt.ylabel("Number of Correct Answers")
    else:
        user_results.sort(key=lambda x: x[3], reverse=True)
        plt.ylabel("Percentage of Correct Answers")

    user_results = user_results if len(user_results) <= 5 else user_results[0:5]
    x_axis = [x[0] for x in user_results]
    plt.xlabel("Users")
    if session["number_or_percentage"] == "number":
        y_axis = [x[1] for x in user_results]
        match session["graph_type"]:
            case "all":
                plt.title(f"Top {len(user_results)} Users with the Highest Number of Correct Answers") if len(user_results) > 1 \
                    else plt.title(f"User with the Highest Number of Correct Answers")
            case "difficulty":
                plt.title(f"Top {len(user_results)} Users with the Highest Number of Correct Answers for Difficulty {session['difficulty']}") if len(user_results) > 1 \
                    else plt.title(f"User with the Highest Number of Correct Answers for Difficulty {session['difficulty']}")
            case "topic":
                if session["topic"] == "hcf_lcm":
                    plt.title(f"Top {len(user_results)} Users with the Highest Number of Correct Answers for HCF, LCM and prime factors Questions") if len(user_results) > 1 \
                        else plt.title(f"User with the Highest Number of Correct Answers for HCF, LCM and prime factors Questions")
                else:
                    plt.title(f"Top {len(user_results)} Users with the Highest Number of Correct Answers for {session['topic']} Questions") if len(user_results) > 1 \
                        else plt.title(f"User with the Highest Number of Correct Answers for {session['topic']} Questions")
    else:
        y_axis = [x[3] for x in user_results]
        match session["graph_type"]:
            case "all":
                plt.title(f"Top {len(user_results)} Users with the Highest Percentage of Correct Answers") if len(user_results) > 1 \
                    else plt.title(f"User with the Highest Percentage of Correct Answers")
            case "difficulty":
                plt.title(
                    f"Top {len(user_results)} Users with the Highest Percentage of Correct Answers for Difficulty {session['difficulty']}") if len(user_results) > 1 \
                    else plt.title(f"User with the Highest Percentage of Correct Answers for Difficulty {session['difficulty']}")
            case "topic":
                if session["topic"] == "hcf_lcm":
                    plt.title(
                        f"Top {len(user_results)} Users with the Highest Percentage of Correct Answers for HCF, LCM and prime factors Questions") if len(user_results) > 1 \
                        else plt.title(f"User with the Highest Percentage of Correct Answers for HCF, LCM and prime factors Questions")
                else:
                    plt.title(
                        f"Top {len(user_results)} Users with the Highest Percentage of Correct Answers for {session['topic']} Questions") if len(user_results) > 1 \
                        else plt.title(f"User with the Highest Percentage of Correct Answers for {session['topic']} Questions")

    print(y_axis)
    bars = plt.bar(x_axis, y_axis)
    plt.bar_label(bars, fmt="%d", padding=10, label_type="center")

    # Adapted from https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    graph_image = BytesIO()
    if y_axis != []:
        plt.savefig(graph_image, format="png")
        graph_image.seek(0)
        plt.close()

    return send_file(graph_image, mimetype="image/png")

@app.route("/view-results", methods=["GET", "POST"])
@login_required
def view_results():
    form_is_submitted = False
    session.pop("graph_type", None)
    session.pop("topic", None)
    session.pop("difficulty", None)
    session.pop("username", None)
    session.pop("compare_results", None)
    session.pop("second_username", None)
    session["graph_type"] = "NotChosen"
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append((user.username, user.username))
    form = ResultsForm(users_list)

    if form.validate_on_submit():
        form_is_submitted = True
        session["graph_type"] = form.results_returned.data
        session["topic"] = form.topic_chosen.data
        session["difficulty"] = form.difficulty_chosen.data
        session["username"] = form.user_chosen.data
        session["compare_results"] = form.compare_results.data
        session["second_username"] = form.second_user_chosen.data
        print(session["compare_results"])

    return render_template("view_results.html", form=form, form_is_submitted=form_is_submitted)

@app.route("/view-max-results", methods=["GET", "POST"])
@login_required
def view_max_results():
    form_is_submitted = False
    session.pop("number_or_percentage", None)
    session.pop("graph_type", None)
    session.pop("topic", None)
    session.pop("difficulty", None)
    form = MaxResultsForm("Choose whether you want to see the players with the highest number or the "
                               "highest percentage of correct questions:")

    if form.validate_on_submit():
        form_is_submitted = True
        session["number_or_percentage"] = form.number_or_percentage_returned.data
        session["graph_type"] = form.results_returned.data
        session["topic"] = form.topic_chosen.data
        session["difficulty"] = form.difficulty_chosen.data

    return render_template("view_max_results.html", form=form, form_is_submitted=form_is_submitted)

@app.route("/leaderboard", methods=["GET", "POST"])
@login_required
def leaderboard_page():
    form_is_submitted = False
    users = User.query.all()
    user_results = []

    form = MaxResultsForm("Choose whether you want the leaderboard to display the players by their number of correct answers or by their percentage of correct answers.")
    if form.validate_on_submit():
        print(f"Results Returned: {form.results_returned}")
        form_is_submitted = True
        match form.results_returned.data:
            case "difficulty":
                for user in users:
                    answer_correct, answer_incorrect, answer_percentage = get_difficulty_results(user, form.difficulty_chosen.data)
                    user_results.append([user.username, answer_correct, answer_incorrect, answer_percentage])
            case "topic":
                for user in users:
                    answer_correct, answer_incorrect, answer_percentage = get_topic_results(user, form.topic_chosen.data)
                    user_results.append([user.username, answer_correct, answer_incorrect, answer_percentage])
            case _:
                for user in users:
                    answer_correct, answer_incorrect, answer_percentage = get_user_results(user)
                    user_results.append([user.username, answer_correct, answer_incorrect, answer_percentage])

        if form.number_or_percentage_returned.data == "number":
            user_results.sort(key=lambda x: x[1], reverse=True)
        else:
            user_results.sort(key=lambda x: x[3], reverse=True)

    return render_template("leaderboard.html", user_results=user_results, form=form, form_is_submitted=form_is_submitted)

@app.route("/tutorial", methods=["GET", "POST"])
@login_required
def tutorial_page():
    return render_template("tutorial.html")

@app.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_to_delete = User.query.filter_by(username=form.username.data).first()
        if user_to_delete and user_to_delete.username == current_user.username and bcrypt.checkpw(form.password.data.encode("utf-8"), user_to_delete.password):
            logout_user()
            question_difficulties_to_delete = QuestionDifficulties.query.filter_by(user_id=user_to_delete.id).first()
            question_topics_to_delete = QuestionTopics.query.filter_by(user_id=user_to_delete.id).first()
            db.session.delete(question_difficulties_to_delete)
            db.session.delete(question_topics_to_delete)
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("Account deletion successful.", category="success")
            return redirect(url_for("register_page"))
        else:
            flash("The username or password entered does not match the details of the currently logged-in user.", category="danger")
    return render_template("delete_account.html", form=form)
