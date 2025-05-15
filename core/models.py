from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

class FileMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(64), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    owner = db.Column(db.String(64), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    # Optionally: file size, file type, etc.
