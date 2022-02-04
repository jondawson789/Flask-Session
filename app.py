from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def start_survey():
    title = survey.title
    instructions = survey.instructions

    return render_template("start.html", title = title, instructions = instructions)

@app.route("/questions/<int:question_id>")
def show_questions(question_id):
    if len(responses) == 0 and question_id != 0:
        flash("please start survey")
        return redirect("/")
    elif len(responses) == len(survey.questions):
        return redirect("/complete")
    elif question_id != len(responses):
        flash("answer this question to continue")
        return redirect(f"/questions/{len(responses)}")
    else:
        questions = survey.questions
        question = questions[question_id].question
        choices = questions[question_id].choices

        return render_template("questions.html", question = question, choices = choices)

@app.route("/answer", methods = ["POST"])
def handle_question():
    answer = request.form["answer"]
    responses.append(answer)

    if len(responses) == len(survey.questions):
        return redirect("/complete")

    next_id = len(responses)
    return redirect(f"/questions/{next_id}")

@app.route("/complete")
def show_complete():
    return render_template("complete.html")

