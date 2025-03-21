import matplotlib
matplotlib.use('Agg')  # Use a backend that doesn't require the main thread
import matplotlib.pyplot as plt
from flask import render_template, redirect, url_for, request, flash, session, send_file
from sympy import sympify, factor, expand, simplify
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt
from io import BytesIO

from quiz import app, db
from .QuizCode.min_and_max_difficulties import *
from quiz.forms import (RegisterForm, LoginForm, AnswerForm, TopicsForm, RestartForm, AnswerQuadraticEquationForm,
                        AnswerSimultaneousEquationForm, AnswerQuadraticSimultaneousEquationForm)
from .QuizCode.topic_manager import question_topic_selection
from quiz.models import User, QuestionTopics, QuestionDifficulties
from quiz.update_results import update_topic_information, update_difficulty_information

@app.route("/", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_anonymous:
        form = RegisterForm()
        if form.validate_on_submit():
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

        return render_template("register.html", form=form)
    else:
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
            }
            session["topic_selection"] = topics_chosen
            session["current_difficulty"] = int(request.form.get("difficulty"))
            session["number_of_questions"] = int(request.form.get("questions"))
            session["question_number"] = 1
            session["difficulty_range"] = 50
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
            topic, question, answer, difficulty_weighting, multiple_answers, image_values = question_topic_selection(
                session.get("topic_selection"), int(session.get("current_difficulty")),
    ["free_text", "multiple-choice", "true/false"])
            session["current_topic"] = topic
            session["final_answer"] = answer
            session["final_question"] = question
            session["final_difficulty_weighting"] = difficulty_weighting
            session["multiple_answers"] = multiple_answers
            if image_values is not None:
                session["image_values"] = image_values
                session["image_added"] = True
            else:
                session.pop("image_values", None)
                session.pop("image_added", None)

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

        if request.method == "POST":
            answer = 0
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
                        if "x" not in answer:
                            flash("Expression must be entered in correct format. Try again.", category="danger")
                            return redirect(url_for("quiz_page"))
                        else:
                            answer = answer.replace(" ", "")
                            final_answer = str(simplify(sympify(final_answer))).replace(" ", "")
                            # answer = simplify(sympify(answer))
                case "calculus":
                    answer = request.form.get("answer")
                    if not final_answer.isnumeric() and "y" not in final_answer:
                        final_answer = sympify(final_answer)
                        answer = sympify(answer)
                    else:
                        final_answer = final_answer.replace(" ", "")
                        answer = answer.replace(" ", "")
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

            if (answer == final_answer or (type(final_answer) == list and (len(final_answer) == 1 and answer == final_answer[0])) or
                    (type(answer) == list and type(final_answer) == list and ((len(answer) == 2 and answer[0] == final_answer[0] and answer[1] == final_answer[1])
            or (len(answer) == 4 and (answer[0] == final_answer[0] and answer[1] == final_answer[0] or (answer[0] == final_answer[1] and answer[1] == final_answer[0]))
                and (answer[2] == final_answer[2] and answer[3] == final_answer[3] or (answer[2] == final_answer[3] and answer[3] == final_answer[2])))))):
                session["score"] += 1
                session["topic_counter"][session["current_topic"]][0] += 1
                difficulty_counter = session["difficulty_counter"]
                difficulty_counter[f"level_{session['current_difficulty']}"][0] += 1
                session["difficulty_counter"] = difficulty_counter

                print("Correct")
                if session["current_difficulty"] < session["max_difficulty"]:
                    session["difficulty_range"] += ((session["final_difficulty_weighting"] - (session["current_difficulty"])) * 30)
                    if session["difficulty_range"] >= 100:
                        session["current_difficulty"] += 1
                        session["difficulty_range"] = 50
                else:
                    session["difficulty_range"] = 50
                flash(f"Well done! You got it right!", category="success")
            else:

                session["topic_counter"][session["current_topic"]][1] += 1
                difficulty_counter = session["difficulty_counter"]
                difficulty_counter[f"level_{session['current_difficulty']}"][1] += 1
                session["difficulty_counter"] = difficulty_counter

                print("Incorrect")
                if session["current_difficulty"] > session["min_difficulty"]:
                    session["difficulty_range"] -= (
                            (difficulty_boundary - (
                                        session["final_difficulty_weighting"] - (session["current_difficulty"]))) * 30)
                    if session["difficulty_range"] <= 0:
                        session["current_difficulty"] -= 1
                        session["difficulty_range"] = 50
                else:
                    session["difficulty_range"] = 50
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
        return render_template("quiz.html", form=form, final_question=final_question,
                               current_difficulty=current_difficulty, score=score, question_number=question_number,
                               multiple_answers=multiple_answers, image_added=image_added)
