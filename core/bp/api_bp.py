from flask import Blueprint

api_bp = Blueprint('/api', __name__)

@api_bp.route('/')
def api_dashboard():
    return "API Dashboard - Under Construction"
