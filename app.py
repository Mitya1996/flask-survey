from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)

responses = []  #empty list initiated for user to fill

@app.route('/')
def home():    
    return render_template('home.html', surveys=surveys)