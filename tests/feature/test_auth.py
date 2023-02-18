from website.controllers.AuthController import login, signup
from werkzeug.security import generate_password_hash
from website.models import User
from website import db, mail
from website.config import TestingConfig
import unittest
from flask import Flask
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

    def test_correct_login(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(
                email=theMail,
                password=generate_password_hash("testPassword"),
                name=fake.name(),
            )
            db.session.add(user)
            db.session.commit()
            response, code = login(theMail, "testPassword")
            assert "token" in response
            assert code == 200

    def test_correct_login_with_otp_sent(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(
                email=theMail,
                password=generate_password_hash("testPassword"),
                name=fake.name(),
                has2fa=True,
            )
            db.session.add(user)
            db.session.commit()
            response, code = login(theMail, "testPassword")
            assert "message" in response
            assert response["message"] == "Check your email"
            assert code == 201

    def test_correct_login_with_otp_not_sent(self):
        with self.app.app_context():
            self.app.config["MAIL_USERNAME"] = None
            theMail = fake.email()
            user = User(
                email=theMail,
                password=generate_password_hash("testPassword"),
                name=fake.name(),
                has2fa=True,
            )
            db.session.add(user)
            db.session.commit()
            response, code = login(theMail, "testPassword")
            assert "error" in response
            assert "otp" in response
            self.assertIn("Error sending the validation email", response["error"])
            assert code == 500

    def test_verify_otp(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(
                email=theMail,
                password=generate_password_hash("testPassword"),
                name=fake.name(),
                has2fa=True,
                currentOtp="123456",
            )
            db.session.add(user)
            db.session.commit()
            response, code = login(theMail, "testPassword", "123456")
            assert "token" in response
            assert code == 200

    def test_missing_user_login(self):
        with self.app.app_context():
            theMail = fake.email()
            response, code = login("wrong_email", "wrong_psw")
            assert "error" in response
            assert response["error"] == "Could not verify user"
            assert code == 404

    def test_wrong_credentials_login(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(
                email=theMail,
                password=generate_password_hash("testPassword"),
                name=fake.name(),
                has2fa=True,
                currentOtp="123456",
            )
            db.session.add(user)
            db.session.commit()
            response, code = login(theMail, "wrong_psw")
            assert "error" in response
            assert response["error"] == "Wrong email or password"
            assert code == 401

    def test_wrong_verifiy_otp(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(
                email=theMail,
                password=generate_password_hash("testPassword"),
                name=fake.name(),
                has2fa=True,
                currentOtp="123456",
            )
            db.session.add(user)
            db.session.commit()
            response, code = login(theMail, "testPassword", "000000")
            assert "error" in response
            assert response["error"] == "Could not verify otp"
            code == 401

    def test_successful_signup(self):
        with self.app.app_context():
            theMail = fake.email()
            theName = fake.name()
            response, code = signup((theName, theMail, "testPassword", False))
            user = User.query.filter_by(email=theMail).first()
            assert user.password != "testPassword"
            assert user.name == theName
            assert not user.has2fa
            assert "message" in response
            assert response["message"] == "Successfully registered."
            assert code == 201

    def test_already_present_user_signup(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(
                email=theMail,
                password=generate_password_hash("testPassword"),
                name=fake.name(),
                has2fa=True,
                currentOtp="123456",
            )
            db.session.add(user)
            db.session.commit()
            response, code = signup((fake.name(), theMail, "testPassword", False))
            assert "message" in response
            assert response["message"] == "User already exists. Please Log in."
            assert code == 200
