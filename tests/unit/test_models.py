from website.models import User
from  werkzeug.security import generate_password_hash


def test_new_user():
    user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian')
    assert user.email == 'christian@gmail.com'
    assert user.password != 'testPassword'
    assert user.name == 'Christian'