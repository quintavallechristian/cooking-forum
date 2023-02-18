from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000))
    has2fa = db.Column(db.Boolean, default=False)
    currentOtp = db.Column(db.String(6), nullable=True)
