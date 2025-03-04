from quiz import app
from flask import render_template, redirect, url_for, request, flash, session
from quiz.forms import AnswerForm, TopicsForm
from quiz.QuizCode.quizCode import operations_question_generation

@app.route("/remove")
def remove_page():
    session.pop("final_question", None)
    session.pop("final_answer", None)
    session.pop("final_difficulty_weighting", None)
    session.pop("current_difficulty", None)
    session.pop("difficulty_range", None)
    session.pop("score", None)
    return redirect(url_for("base_page"))

@app.route("/quiz_selection", methods=["GET", "POST"])
def quiz_selection():
    form = TopicsForm()

    if request.method == "POST":
        pass

    return render_template("quiz_selection.html", form=form)

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def base_page():
    form = AnswerForm()
    difficulty_boundary = 20

    if "current_difficulty" not in session:
        session["current_difficulty"] = 2
        session["difficulty_range"] = 50
        session["score"] = 0

    if "final_answer" not in session:
        first_num, second_num, question, answer, difficulty_weighting = operations_question_generation(
            2, ["free_text", "multiple-choice", "true/false"])
        session["final_answer"] = answer
        session["final_question"] = question
        session["final_difficulty_weighting"] = difficulty_weighting

    final_answer = session.get("final_answer")
    final_question = session.get("final_question")

    if request.method == "POST":
        answer = request.form.get("answer")
        try:
            if type(answer) != type(final_answer):
                answer = int(answer)
            else:
                if answer == "True" or answer == "False":
                    pass
                else:
                    flash("You must enter True or False. Try again", category="danger")
                    return redirect(url_for("base_page"))
        except Exception:
            flash("You must enter a number. Try again.", category="danger")
            return redirect(url_for("base_page"))

        if answer == final_answer:
            session["score"]  += 1
            print("Correct")
            if session["current_difficulty"] > 1:
                session["difficulty_range"] += ((session["final_difficulty_weighting"] - (session["current_difficulty"] * 20)) * 2)
                if session["difficulty_range"] >= 100:
                    session["current_difficulty"]  += 1
                    session["difficulty_range"] = 50
            flash(f"Well done! You got it right!", category="success")
        else:
            if session["current_difficulty"] < 5:
                session["difficulty_range"] -= (
                        (difficulty_boundary - (
                                    session["final_difficulty_weighting"] - (session["current_difficulty"] * 20))) * 2)
                if session["difficulty_range"] <= 0 and session["current_difficulty"]:
                    session["current_difficulty"] -= 1
                    session["difficulty_range"] = 50
            flash(f"You got it wrong! The correct answer is {final_answer}", category="danger")

        session.pop("final_question", None)
        session.pop("final_answer", None)
        session.pop("final_difficulty_weighting", None)
        print(session.get("current_difficulty"))
        print(session.get("difficulty_range"))
        return redirect(url_for("base_page"))
    current_difficulty = session.get("current_difficulty")
    score = session.get("score")
    return render_template("quiz.html", form=form, final_question=final_question, current_difficulty=current_difficulty, score=score)
