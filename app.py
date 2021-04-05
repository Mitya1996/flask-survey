from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

responses = []  #empty list initiated for user to fill

@app.route('/')
def home():
    responses = [] #reset responses    
    return render_template('home.html', survey=survey)

@app.route('/question/<int:qidx>')
def question(qidx):
    #protect from user tinkering with URL
    correct_idx = len(responses)
    if qidx != correct_idx:
        flash(f'Sir/madam, you are trying to access an invalid question and have been redirected to question {correct_idx + 1}.')
        return redirect(f'/question/{correct_idx}')

    curr_q = survey.questions[qidx]
    return render_template('question.html', curr_q=curr_q, qidx=qidx)

@app.route('/answer', methods=['POST'])
def answer():
    answ = request.form['choice']
    if len(responses) < len(survey.questions): #only append if responses not yet full
        responses.append(answ)

    qidx = len(responses)
    if qidx > len(survey.questions) - 1:
        return redirect('/thankyou') 
    else:
        return redirect(f'/question/{qidx}')

@app.route('/thankyou')
def thankyou():
    print(responses) 
    return render_template('thankyou.html')


    
