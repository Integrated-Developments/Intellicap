from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
# <!-- Initiate Flask and Config ----->
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '直腸暴行海賊'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///intellicap.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = False  # True in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SQLALCHEMY_ECHO'] = False  # Set to True for debugging SQL queries
    app.config['DEBUG'] = True  # Set to False in production
    app.config['TESTING'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # seconds
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year for static files

# <!-- Register & Config bp's ----->
    from core.bp.auth_bp import auth_bp
    from core.bp.user_bp import user_bp
    from core.bp.code_bp import code_bp
    from core.bp.main_bp import main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(code_bp, url_prefix='/code')
    app.register_blueprint(main_bp, url_prefix='/')

    socketio.init_app(app, cors_allowed_origins="*")
    return app, socketio
