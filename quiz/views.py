from quiz import app
from flask import render_template, redirect, url_for, request, flash, session
from quiz.forms import AnswerForm, TopicsForm, RestartForm, AnswerQuadraticEquationForm, AnswerSimultaneousEquationForm, AnswerQuadraticSimultaneousEquationForm
from .QuizCode.topic_manager import question_topic_selection
from sympy import sympify, factor, expand, simplify
from .QuizCode.min_and_max_difficulties import operations, equations, expressions, fractions


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
def end_quiz():
    form = RestartForm()
    if request.method == "POST":
        return redirect(url_for("quiz_selection"))
    number_of_questions = session.get("number_of_questions")
    score = session.get("score")
    return render_template("end_quiz.html", form=form, number_of_questions=number_of_questions, score=score)

@app.route("/", methods=["GET", "POST"])
@app.route("/quiz-selection", methods=["GET", "POST"])
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
    session.pop("score", None)

    if request.method == "POST":
        topics_chosen = []
        if request.form.get("operations") is not None:
            topics_chosen.append("operations")
        if request.form.get("fractions") is not None:
            topics_chosen.append("fractions")
        if request.form.get("calculus") is not None:
            topics_chosen.append("calculus")
        if request.form.get("equations") is not None:
            topics_chosen.append("equations")
        if request.form.get("expressions") is not None:
            topics_chosen.append("expressions")
        if request.form.get("sequences") is not None:
            topics_chosen.append("sequences")
        if request.form.get("hcf_lcm") is not None:
            topics_chosen.append("hcf_lcm")
        if request.form.get("percentages") is not None:
            topics_chosen.append("percentages")
        if request.form.get("triangles") is not None:
            topics_chosen.append("triangles")
        if len(topics_chosen) == 0:
            flash("Please select a topic.", category="danger")
            # return redirect(url_for("quiz_selection"))
        else:
            session["topic_selection"] = topics_chosen
            session["current_difficulty"] = int(request.form.get("difficulty"))
            session["number_of_questions"] = int(request.form.get("questions"))
            session["question_number"] = 1
            session["difficulty_range"] = 50
            session["score"] = 0
            print(session.get("topic_selection"))
            return redirect(url_for("quiz_page"))

    return render_template("quiz_selection.html", form=form)


@app.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    if "topic_selection" not in session:
        flash("You must make a quiz before starting one.", category="danger")
        return redirect(url_for("quiz_selection"))
    else:
        form = AnswerForm()
        difficulty_boundary = 30
        if "final_answer" not in session:
            topic, question, answer, difficulty_weighting, multiple_answers = question_topic_selection(
                session.get("topic_selection"), int(session.get("current_difficulty")),
    ["free_text", "multiple-choice", "true/false"])
            session["current_topic"] = topic
            session["final_answer"] = answer
            session["final_question"] = question
            session["final_difficulty_weighting"] = difficulty_weighting
            session["multiple_answers"] = multiple_answers

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
        print(type(final_answer))

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
                            final_answer = simplify(sympify(final_answer))
                            answer = simplify(sympify(answer))
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
                            final_answer = simplify(sympify(final_answer))
                            answer = simplify(sympify(answer))
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

            if (answer == final_answer or (type(final_answer == list) and (len(final_answer) == 1 and answer == final_answer[0])) or
                    (type(answer) == list and type(final_answer) == list and ((len(answer) == 2 and answer[0] == final_answer[0] and answer[1] == final_answer[1])
            or (len(answer) == 4 and (answer[0] == final_answer[0] and answer[1] == final_answer[0] or (answer[0] == final_answer[1] and answer[1] == final_answer[0]))
                and (answer[2] == final_answer[2] and answer[3] == final_answer[3] or (answer[2] == final_answer[3] and answer[3] == final_answer[2])))))):
                session["score"] += 1
                print("Correct")
                if session["current_difficulty"] < 10:
                    session["difficulty_range"] += ((session["final_difficulty_weighting"] - (session["current_difficulty"])) * 30)
                    if session["difficulty_range"] >= 100:
                        session["current_difficulty"]  += 1
                        session["difficulty_range"] = 50
                else:
                    session["difficulty_range"] = 50
                flash(f"Well done! You got it right!", category="success")
            else:
                print("Incorrect")
                if session["current_difficulty"] > 1:
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
                return redirect(url_for("end_quiz"))

            return redirect(url_for("quiz_page"))

        current_difficulty = session.get("current_difficulty")
        score = session.get("score")
        question_number = session.get("question_number")
        multiple_answers = session.get("multiple_answers")
        return render_template("quiz.html", form=form, final_question=final_question,
                               current_difficulty=current_difficulty, score=score, question_number=question_number,
                               multiple_answers=multiple_answers)
