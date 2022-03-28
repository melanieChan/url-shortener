from flask import Flask, render_template, request, redirect, url_for
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# function ran after user clicks submit button on form
@app.route('/shorten', methods=['GET', 'POST'])
def shorten():
    new_shortcut_input = request.form['new_shortcut_name_input']

    response = {}
    shortcuts = {} # data of all shortcuts will be saved into file

    # save to existing file that already has previously made shortcuts
    if os.path.exists('shortcuts.json'):
        with open('shortcuts.json') as shortcuts_file:
            shortcuts = json.load(shortcuts_file)

    # don't proceed to saving data if user tries to use the same shortcut name
    if new_shortcut_input in shortcuts.keys():
        # get existing url or file associated with shortcut
        current_link = shortcuts[new_shortcut_input]['url'] if 'url' in shortcuts[new_shortcut_input] else shortcuts[new_shortcut_input]['file']
        response['error'] = 'Shortcut name already in use. It redirects to <a href="' + current_link + '" target="_blank" rel="noopener noreferrer">' + current_link + '</a>';
        return json.dumps(response)

    # save new shortcut and its (url or file)
    if 'original_url_input' in request.form.keys():
        response['url'] = request.form['original_url_input']
    else:
        file = request.files['file'] # get user's input file

        # save with shortcut name (since shortcut should be unique) in case multiple independent files uploaded have same name
        custom_file_path = request.form['new_shortcut_name_input'] + secure_filename(file.filename)
        current_dir = os.path.dirname(os.path.realpath(__file__)) + '/static/user_files/'
        file.save(current_dir + custom_file_path)

        response['file'] = custom_file_path

    # save new shortcut to json file
    shortcuts[new_shortcut_input] = response
    with open('shortcuts.json', 'w') as shortcuts_file:
        json.dump(shortcuts, shortcuts_file)

    return json.dumps(response)

# link that doesn't exist
@app.route('/<shortcut_path>')
def redirect_to_url(shortcut_path):
    if os.path.exists('shortcuts.json'): # find file
        with open('shortcuts.json') as shortcuts_file:
            shortcuts = json.load(shortcuts_file) # get data from file
            if shortcut_path in shortcuts.keys(): # search for specific shortcut
                # go to url or file using shortcut
                if 'url' in shortcuts[shortcut_path].keys():
                    return redirect(shortcuts[shortcut_path]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + shortcuts[shortcut_path]['file']))
