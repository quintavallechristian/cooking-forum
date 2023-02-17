from website.models import User
from  werkzeug.security import generate_password_hash
from faker import Faker
fake = Faker()


def test_new_user():
    email = fake.email()
    name = fake.name()
    user = User(email = email, password = generate_password_hash('testPassword'), name = name)
    assert user.email == email
    assert user.password != 'testPassword'
    assert user.name == name