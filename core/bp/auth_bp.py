from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# <!-- Functions ----->
def func () :
    pass

# <!-- Route Logic ----->
@auth_bp.route('/login')
def login () :
    pass
