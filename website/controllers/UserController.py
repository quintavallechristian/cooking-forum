from ..models import User

def getUser(email):
    return User.query\
        .filter_by(email = email)\
        .first()