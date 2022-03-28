from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# function ran after user clicks submit button on form
@app.route('/shorten', methods=['GET', 'POST'])
def shorten():
    new_shortcut_input = request.form['new_shortcut_name_input']
    original_url_input = request.form['original_url_input']

    return new_shortcut_input

# link that doesn't exist
@app.route('/<nonexistent_path>')
def redirect_back_home(nonexistent_path=None):
    return redirect(url_for('home'))
