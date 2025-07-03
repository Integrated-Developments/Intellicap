from flask import Blueprint, current_app, send_from_directory, current_app, render_template, redirect, url_for, request
from datetime import datetime
import os

main = Blueprint('main', __name__)

@main.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'img'), 'favicon.ico')

@main.route('/')
def index ():
    langs = current_app.config['SUPPORTED_LANGUAGES']
    lang = request.accept_languages.best_match(langs)
    return redirect(url_for('main.local_index', lang=lang or current_app.config['DEFAULT_LANGUAGE']))

@main.route('/<lang>/')
def local_index(lang):
    if lang not in current_app.config['SUPPORTED_LANGUAGES']:
        lang = current_app.config['DEFAULT_LANGUAGE']
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(f'{lang}/landing.html', current_time=current_time)
