from flask import Blueprint, redirect, url_for
from utils import Coder

api = Blueprint('api', __name__)

users = [{"angry": "tfukgobx"} , {"cree": "pyslut"}]

@api.route('/')
def api_dashboard():
    return "API Dashboard - Under Construction"

@api.route('/code/user=<user>&key=<key>', methods=['GET'])
def api_code(user, key):
    if user in [u for d in users for u in d.keys()]:
        if key == [d[user] for d in users if user in d][0]:
            coder = Coder()
            result = coder.Start_Session(user)
            if isinstance(result, str) and result.startswith('https://'):
                return redirect(result)
            elif isinstance(result, str) and result.startswith('error:'):
                return f"Failed to start code-server session: {result}", 500
            else:
                return "Unknown error occurred while starting session.", 500
        else:
            return "Invalid Key", 403
    return "User not found", 404
