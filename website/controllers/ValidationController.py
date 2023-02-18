import re


def validateAll(name, email, password, has2fa):
    if not validateEmail(email):
        return False, "Invalid email."
    if not validatePassword(password):
        return False, "Invalid password."
    if not validateName(name):
        return False, "Invalid name."
    if not validate2fa(has2fa):
        return False, "Invalid 2fa option."
    return True, "ok"


def validateEmail(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True


def validatePassword(password):
    if len(password) < 8:
        return False
    return True


def validateName(name):
    if not name or len(name) == 0:
        return False
    return True


def validate2fa(has2fa):
    if not isinstance(has2fa, bool):
        return False
    return True
