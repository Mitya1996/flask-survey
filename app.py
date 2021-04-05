from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    return render_template('home.html', survey=survey)

@app.route('/init', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/question/0')

@app.route('/question/<int:qidx>')
def question(qidx):
    #protect from user tinkering with URL
    correct_idx = len(session['responses'])
    if qidx != correct_idx:
        flash(f'Sir/madam, you are trying to access an invalid question and have been redirected to question {correct_idx + 1}.')
        return redirect(f'/question/{correct_idx}')

    curr_q = survey.questions[qidx]
    return render_template('question.html', curr_q=curr_q, qidx=qidx)

@app.route('/answer', methods=['POST'])
def answer():
    answ = request.form['choice']
    if len(session['responses']) < len(survey.questions): #only append if responses not yet full
        session['responses'] = [*session['responses'], answ] #append response

    qidx = len(session['responses'])
    if qidx > len(survey.questions) - 1:
        return redirect('/thankyou') 
    else:
        return redirect(f'/question/{qidx}')

@app.route('/thankyou')
def thankyou():
    print(session['responses']) 
    return render_template('thankyou.html')


    
@app.before_request
def test():
    print(session.get('responses', None))