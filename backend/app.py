from flask import Flask, render_template, request, redirect, url_for
import json
import os.path

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# function ran after user clicks submit button on form
@app.route('/shorten', methods=['GET', 'POST'])
def shorten():
    new_shortcut_input = request.form['new_shortcut_name_input']
    original_url_input = request.form['original_url_input']

    response = {}
    shortcuts = {} # data of all shortcuts will be saved into file

    # save to existing file that already has previously made shortcuts
    if os.path.exists('shortcuts.json'):
        with open('shortcuts.json') as shortcuts_file:
            shortcuts = json.load(shortcuts_file)

    # don't proceed to saving data if user tries to use the same shortcut name
    if new_shortcut_input in shortcuts.keys():
        response['error'] = 'Shortcut name already in use. It redirects to ' + shortcuts[new_shortcut_input]['url'];
        return json.dumps(response)

    response['url'] = original_url_input

    # save new shortcut to json file
    shortcuts[new_shortcut_input] = response
    with open('shortcuts.json', 'w') as shortcuts_file:
        json.dump(shortcuts, shortcuts_file)

    return json.dumps(response)

# link that doesn't exist
@app.route('/<nonexistent_path>')
def redirect_back_home(nonexistent_path=None):
    return redirect(url_for('home'))
