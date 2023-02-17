from website.controllers.AuthController import login, signup
from werkzeug.security import generate_password_hash
from website.models import User
from website import db, mail
import unittest
from flask import Flask

class TestClass(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbtest.sqlite'
        self.app.config['SECRET_KEY'] = 'test_token'
        self.app.config['TESTING'] = True
        self.app.config['MAIL_FROM_NAME'] = 'test@test.com'
        db.init_app(self.app)
        mail.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbtest.sqlite'
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()

    def test_correct_login(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian')
            db.session.add(user)
            db.session.commit()
            response, code = login('christian@gmail.com', 'testPassword')
            assert 'token' in response
            assert code == 201
    
    def test_correct_login_with_otp_sent(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True)
            db.session.add(user)
            db.session.commit()
            response, code = login('christian@gmail.com', 'testPassword')
            assert 'message' in response
            assert response['message'] == 'check your email'
            assert code == 200

    def test_verifiy_otp(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()
            response, code = login('christian@gmail.com', 'testPassword', '123456')
            assert 'token' in response
            assert code == 201

    def test_missing_user_login(self):
        with self.app.app_context():
            response, code = login('wrong_email', 'wrong_psw')
            assert 'error' in response
            assert response['error'] == 'Could not verify user'
            assert code == 401

    def test_wrong_credentials_login(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()
            response, code = login('christian@gmail.com', 'wrong_psw')
            assert 'error' in response
            assert response['error'] == 'Wrong email or password'
            assert code == 401

    def test_wrong_verifiy_otp(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()
            response, code = login('christian@gmail.com', 'testPassword', '000000')
            assert 'error' in response
            assert response['error'] == 'Could not verify otp'
            assert code == 401

    def test_successful_signup(self):
        with self.app.app_context():
            response, code = signup(('Christian', 'christian@gmail.com', 'testPassword', False))
            user = User.query\
                .filter_by(email = 'christian@gmail.com')\
                .first()
            assert user.password != 'testPassword'
            assert user.name == 'Christian'
            assert not user.has2fa
            assert 'message' in response
            assert response['message'] == 'Successfully registered.'
            assert code == 201

    def test_already_present_user_signup(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()
            response, code = signup(('Christian', 'christian@gmail.com', 'testPassword', False))
            assert 'message' in response
            assert response['message'] == 'User already exists. Please Log in.'
            assert code == 201