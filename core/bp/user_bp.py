from flask import Blueprint

user_bp = Blueprint('/user', __name__)

@user_bp.route('/profile')
def user_profile():
    return "User Profile Page Under Construction"
