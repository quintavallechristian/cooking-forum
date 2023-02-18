from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from website import mail, db
from flask_mail import Message
from random import randint
from flask import current_app


def validMailParams():
    print(current_app.config["MAIL_USE_TLS"] )
    return (current_app.config["MAIL_FROM_NAME"] and
    current_app.config["MAIL_SERVER"] and
    current_app.config["MAIL_PORT"] and
    current_app.config["MAIL_USERNAME"] and
    current_app.config["MAIL_PASSWORD"] and
    isinstance(current_app.config["MAIL_USE_TLS"], bool))

def sendMail(user, otp):
    if not validMailParams():
        print(f"Error sending email. Invalid config. The otp is {otp}")
        return False
    
    # this can be improved by using a queue
    try:
        msg = Message(
            "Complete your registration",
            sender=current_app.config["MAIL_FROM_NAME"],
            recipients=[user.email],
        )
        msg.body = f"""
        Hi {user.name}!
        In order to complete the login you must insert this code in your application! 
        {otp}
        If you did not try to login to the application simply ignore this email.
        Regards, cooking forum team"""
        mail.send(msg)
        return True
    except:
        
        print(f"Error sending email. The otp is {otp}")
        return False