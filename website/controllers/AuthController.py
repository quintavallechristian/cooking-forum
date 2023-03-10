from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from website import mail, db
from flask_mail import Message
from random import randint
from flask import current_app
from .UserController import getUser
from .EmailController import sendMail


def login(email, password, otp=None):
    user = getUser(email)
    if not user:
        return ({"error": "Could not verify user"}, 404)

    if check_password_hash(user.password, password):
        token = generateToken(user)

        if user.has2fa:
            if user.currentOtp and otp == user.currentOtp:
                associateOtp(user, None)
                return ({"token": token}, 200)
            if otp:
                return ({"error": "Could not verify otp"}, 401)

            newOtp = generateOTP()
            associateOtp(user, newOtp)
            if sendMail(user, newOtp):
                return ({"message": "Check your email"}, 201)
            return ({"error": "Error sending the validation email. Probably due to a misconfiguration in the email client. Use the otp state here to authenticate", "otp": newOtp}, 500)
        else:
            return ({"token": token}, 200)
    return ({"error": "Wrong email or password"}, 401)


def signup(params):
    name, email, password, has2fa = params
    user = getUser(email)

    if user:
        return ({"message": "User already exists. Please Log in."}, 200)

    user = User(
        name=name, email=email, password=generate_password_hash(password), has2fa=has2fa
    )
    db.session.add(user)
    db.session.commit()
    return ({"message": "Successfully registered."}, 201)


###### UTILS ####
def generateOTP(n=6):
    n = 1 if n < 1 else n
    return randint(int("1" * n), int("9" * n))


def generateToken(user):
    return jwt.encode(
        {"id": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)},
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )


def associateOtp(user, otp):
    user.currentOtp = otp
    db.session.add(user)
    db.session.commit()
