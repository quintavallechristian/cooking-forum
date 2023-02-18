from website.controllers.AuthController import login, signup
from werkzeug.security import generate_password_hash
from website.models import User
from website import db, mail
from website.config import TestingConfig
import unittest
from flask import Flask
from website.controllers import UserController
from faker import Faker

fake = Faker()


class TestClass(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(TestingConfig())
        db.init_app(self.app)
        mail.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        self.app = Flask(__name__)
        self.app.config.from_object(TestingConfig())
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()

    def test_get_user(self):
        with self.app.app_context():
            email = fake.email()
            name = fake.name()
            user = User(
                email=email, password=generate_password_hash("testPassword"), name=name
            )
            db.session.add(user)
            db.session.commit()
            self.assertEqual(UserController.getUser(email).email, user.email)

    def test_get_users(self):
        with self.app.app_context():
            user1 = User(
                email=fake.email(),
                password=generate_password_hash("testPassword"),
                name=fake.name(),
            )
            db.session.add(user1)
            user2 = User(
                email=fake.email(),
                password=generate_password_hash("testPassword"),
                name=fake.name(),
            )
            db.session.add(user2)
            db.session.commit()

            self.assertEqual(len(UserController.getUsers()), 2)
