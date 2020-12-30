from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def survey_start():
    """Homepage of app where user begins survey."""

    return render_template('index.html', survey=satisfaction_survey)

@app.route("/session", methods=["POST"])
def session_reset():

    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<int:qnum>")
def get_question(qnum):
    """Displays a question based on where user is in survey."""

    responses = session.get("responses")

    if (responses is None):
        return redirect('/questions/0')
    
    if (len(responses) != qnum):
        flash("Invalid question: please complete all questions in order!")
        return redirect(f"/questions/{len(responses)}")

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/thankyou")

    question = satisfaction_survey.questions[qnum]
    return render_template('question.html', question=question, num=qnum)

@app.route("/answer", methods=["POST"])
def send_answer():
    """Saves answer to responses session. If user has finished all questions, redirects to thank you page."""

    responses = session["responses"]
    answer = request.form['answer']
    responses.append(answer)
    session["responses"] = responses
    return redirect(f"/questions/{len(responses)}")

@app.route("/thankyou")
def thank_you():
    """Thanks user for completing survey with button to return to homepage."""

    return render_template('thankyou.html')