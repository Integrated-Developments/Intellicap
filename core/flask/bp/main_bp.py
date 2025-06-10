from flask import Blueprint, send_from_directory, current_app
from datetime import datetime
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'img'), 'favicon.ico')

@main_bp.route('/')
def landing ():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Welcome to the IntelliCap API! Current server time is {current_time}."
