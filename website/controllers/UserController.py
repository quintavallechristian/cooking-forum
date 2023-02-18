from ..models import User


def getUsers():
    users = User.query.all()

    return list(
        map(
            lambda x: {
                "id": x.id,
                "name": x.name,
                "email": x.email,
            },
            users,
        )
    )


def getUser(email):
    return User.query.filter_by(email=email).first()
