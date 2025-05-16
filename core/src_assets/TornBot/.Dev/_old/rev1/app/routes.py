Version = [0,0,3]
State = "FSK"

from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route("/favicon.ico")
def favicon () :
    return send_from_directory('static/img', 'favicon.ico', mimetype='image/vnd.microsoft.icon'), 666

@main_bp.route("/")
def home () :
    return render_template("home.html")

@main_bp.route("/dashboard")
@login_required
def dashboard () :
    return render_template("dashboard.html", user=current_user)