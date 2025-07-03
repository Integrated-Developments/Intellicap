#!/usr/bin/env python3

# <!-- [SS-1]: Imports ----->
import os
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

# <!-- [SS-2]: Global Variables ----->
socketio = SocketIO()
db = SQLAlchemy()
_dir = os.path.dirname(os.path.abspath(__file__))

# <!-- [SS-3]: Helper Functions ----->

# <!-- [SS-4]: Functions ----->
def create_app():
    '''Create and configure the Flask application instance.'''
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SUPPORTED_LANGUAGES'] = ['en', 'ja', 'sp', 'de']
    app.config['DEFAULT_LANGUAGE'] = 'en'
    app.config['SECRET_KEY'] = '直腸暴行海賊'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:tfukgobx@localhost:6666/intellicap'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = False  # True in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SQLALCHEMY_ECHO'] = False  # Set to True for debugging SQL queries
    app.config['DEBUG'] = True  # Set to False in production
    app.config['TESTING'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # seconds
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    app.config['JSON_SORT_KEYS'] = True
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    db.init_app(app)

# <!-- Register & Config bp's ----->
    from bp.admin_bp import admin_bp
    from bp.auth_bp import auth_bp
    from bp.user_bp import user_bp
    from bp.main_bp import main
    from bp.api_bp import api_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')

    socketio.init_app(app, cors_allowed_origins="*")
    return app, socketio
