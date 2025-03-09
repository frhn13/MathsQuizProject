from quiz import app
from flask import render_template, redirect, url_for, request, flash, session
from quiz.forms import AnswerForm, TopicsForm, RestartForm
from quiz.QuizCode.quizCode import question_topic_selection

@app.route("/remove")
def remove_page():
    session.pop("final_question", None)
    session.pop("final_answer", None)
    session.pop("final_difficulty_weighting", None)
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
            topic, question, answer, difficulty_weighting = question_topic_selection(session.get("topic_selection"),
                int(session.get("current_difficulty")), ["free_text", "multiple-choice", "true/false"])
            session["current_topic"] = topic
            session["final_answer"] = answer
            session["final_question"] = question
            session["final_difficulty_weighting"] = difficulty_weighting

        final_answer = session.get("final_answer")
        final_question = session.get("final_question")
        print(final_answer)

        if request.method == "POST":
            answer = request.form.get("answer")
            if session["current_topic"] == "fractions":
                if (answer != "True" and answer != "False") and (final_answer == "True" or final_answer == "False"):
                    flash("You must enter True or False. Try again", category="danger")
                    return redirect(url_for("quiz_page"))
                elif type(final_answer) == str and not "/" in answer and (final_answer != "True" and final_answer != "False"):
                    flash("You must write your answer as a fraction. Try again.", category="danger")
                    return redirect(url_for("quiz_page"))
                else:
                    final_answer = str(final_answer)
            else:
                try:
                    if type(answer) != type(final_answer):
                        answer = int(answer)
                    else:
                        if answer == "True" or answer == "False":
                            pass
                        else:
                            flash("You must enter True or False. Try again", category="danger")
                            return redirect(url_for("quiz_page"))
                except Exception:
                    flash("You must enter a number. Try again.", category="danger")
                    return redirect(url_for("quiz_page"))

            if answer == final_answer:
                session["score"] += 1
                print("Correct")
                if session["current_difficulty"] < 5:
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
            session.pop("current_topic", None)

            if session["question_number"] > session["number_of_questions"]:
                return redirect(url_for("end_quiz"))

            return redirect(url_for("quiz_page"))

        current_difficulty = session.get("current_difficulty")
        score = session.get("score")
        question_number = session.get("question_number")
        return render_template("quiz.html", form=form, final_question=final_question, current_difficulty=current_difficulty, score=score, question_number=question_number)
