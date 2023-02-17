from website import db, mail
from website.models import User
from website import db, mail
from werkzeug.security import generate_password_hash
from website.api import api
import unittest
from flask import Flask

class TestClass(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbtest.sqlite'
        self.app.config['SECRET_KEY'] = 'test_token'
        self.app.config['TESTING'] = True
        self.app.config['MAIL_FROM_NAME'] = 'test@test.com'
        self.app.register_blueprint(api, url_prefix='/api')
        self.client = self.app.test_client()
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

            response = self.client.post('/api/login', json={
                'email': 'christian@gmail.com', 'password': 'testPassword'
            })

            assert 'token' in response.get_json()
            assert response.status_code == 201
    
    def test_correct_login_with_otp_sent(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True)
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/login', json={
                'email': 'christian@gmail.com', 'password': 'testPassword'
            })

            assert 'message' in response.get_json()
            assert response.get_json()['message'] == 'check your email'
            assert response.status_code == 200

    def test_verifiy_otp(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/verify', json={
                'email': 'christian@gmail.com', 'password': 'testPassword', 'otp': '123456'
            })

            assert 'token' in response.get_json()
            assert response.status_code == 201

    def test_missing_user_login(self):
        with self.app.app_context():

            response = self.client.post('/api/login', json={
                'email': 'wrong_email', 'password': 'wrong_psw'
            })

            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Could not verify user'
            assert response.status_code == 401

    def test_missing_params_login(self):
        with self.app.app_context():

            response = self.client.post('/api/login', json={
                'email': 'wrong_email'
            })

            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Could not verify'
            assert response.status_code == 403

    def test_missing_params_verify(self):
        with self.app.app_context():

            response = self.client.post('/api/login', json={
                'email': 'wrong_email', 'passowrd': 'testPassword'
            })

            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Could not verify'
            assert response.status_code == 403

    def test_wrong_credentials_login(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/login', json={
                'email': 'christian@gmail.com', 'password': 'wrong_psw'
            })

            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Wrong email or password'
            assert response.status_code == 401

    def test_wrong_verifiy_otp(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/verify', json={
                'email': 'christian@gmail.com', 'password': 'testPassword', 'otp': '000000'
            })

            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Could not verify otp'
            assert response.status_code == 401

    def test_successful_signup(self):
        with self.app.app_context():
            response = self.client.post('/api/signup', json={
                'name': 'Christian', 
                'email': 'christian@gmail.com', 
                'password': 'testPassword', 
                'has2fa': False
            })

            user = User.query\
                .filter_by(email = 'christian@gmail.com')\
                .first()
            assert user.password != 'testPassword'
            assert user.name == 'Christian'
            assert not user.has2fa
            assert 'message' in response.get_json()
            assert response.get_json()['message'] == 'Successfully registered.'
            assert response.status_code == 201

    def test_already_present_user_signup(self):
        with self.app.app_context():
            user = User(email = 'christian@gmail.com', password = generate_password_hash('testPassword'), name = 'Christian', has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/signup', json={
                'name': 'Christian', 
                'email': 'christian@gmail.com', 
                'password': 'testPassword', 
                'has2fa': False
            })
            assert 'message' in response.get_json()
            assert response.get_json()['message'] == 'User already exists. Please Log in.'
            assert response.status_code == 201