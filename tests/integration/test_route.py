from website import db, mail
from website.models import User
from website import db, mail
from werkzeug.security import generate_password_hash
from website.api import api
from website.config import TestingConfig
import unittest
from flask import Flask
from faker import Faker

fake = Faker()

class TestClass(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(TestingConfig())
        self.app.register_blueprint(api, url_prefix='/api')
        self.client = self.app.test_client()
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
            user = User(email = theMail, password = generate_password_hash('testPassword'), name = fake.name())
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/login', json={
                'email': theMail, 'password': 'testPassword'
            })

            assert 'token' in response.get_json()
            assert response.status_code == 201
    
    def test_correct_login_with_otp_sent(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(email = theMail, password = generate_password_hash('testPassword'), name = fake.name(), has2fa = True)
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/login', json={
                'email': theMail, 'password': 'testPassword'
            })

            assert 'message' in response.get_json()
            assert response.get_json()['message'] == 'check your email'
            assert response.status_code == 200

    def test_verify_otp(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(email = theMail, password = generate_password_hash('testPassword'), name = fake.name(), has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/verify', json={
                'email': theMail, 'password': 'testPassword', 'otp': '123456'
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
            theMail = fake.email()
            user = User(email = theMail, password = generate_password_hash('testPassword'), name = fake.name(), has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/login', json={
                'email': theMail, 'password': 'wrong_psw'
            })

            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Wrong email or password'
            assert response.status_code == 401

    def test_wrong_verify_otp(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(email = theMail, password = generate_password_hash('testPassword'), name = fake.name(), has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/verify', json={
                'email': theMail, 'password': 'testPassword', 'otp': '000000'
            })

            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Could not verify otp'
            assert response.status_code == 401

    def test_successful_signup(self):
        with self.app.app_context():
            theMail = fake.email()
            theName = fake.name()
            response = self.client.post('/api/signup', json={
                'name': theName, 
                'email': theMail, 
                'password': 'testPassword', 
                'has2fa': False
            })

            user = User.query\
                .filter_by(email = theMail)\
                .first()
            assert user.password != 'testPassword'
            assert user.name == theName
            assert not user.has2fa
            assert 'message' in response.get_json()
            assert response.get_json()['message'] == 'Successfully registered.'
            assert response.status_code == 201

    def test_already_present_user_signup(self):
        with self.app.app_context():
            theMail = fake.email()
            user = User(email = theMail, password = generate_password_hash('testPassword'), name = fake.name(), has2fa = True, currentOtp = '123456')
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/api/signup', json={
                'name': fake.name(), 
                'email': theMail, 
                'password': 'testPassword', 
                'has2fa': False
            })
            assert 'message' in response.get_json()
            assert response.get_json()['message'] == 'User already exists. Please Log in.'
            assert response.status_code == 201

    def test_wrong_email_format_signup(self):
        with self.app.app_context():
            response = self.client.post('/api/signup', json={
                'name': fake.name(), 
                'email': 'christiil.com', 
                'password': 'testPassword', 
                'has2fa': False
            })

            user = User.query\
                .filter_by(email = fake.email())\
                .first()
            assert user == None
            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Invalid email.'
            assert response.status_code == 403

    def test_wrong_name_format_signup(self):
        with self.app.app_context():
            response = self.client.post('/api/signup', json={
                'name': '', 
                'email': fake.email(), 
                'password': 'testPassword', 
                'has2fa': False
            })

            user = User.query\
                .filter_by(email = fake.email())\
                .first()
            assert user == None
            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Invalid name.'
            assert response.status_code == 403

    def test_wrong_email_format_signup(self):
        with self.app.app_context():
            response = self.client.post('/api/signup', json={
                'name': fake.name(), 
                'email': fake.email(), 
                'password': 'test', 
                'has2fa': False
            })

            user = User.query\
                .filter_by(email = fake.email())\
                .first()
            assert user == None
            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Invalid password.'
            assert response.status_code == 403
    
    def test_wrong_email_format_signup(self):
        with self.app.app_context():
            response = self.client.post('/api/signup', json={
                'name': fake.name(), 
                'email': fake.email(), 
                'password': 'testPassword', 
            })

            user = User.query\
                .filter_by(email = fake.email())\
                .first()
            assert user == None
            assert 'error' in response.get_json()
            assert response.get_json()['error'] == 'Invalid 2fa option.'
            assert response.status_code == 403

    def test_logged_in_route(self):
        with self.app.app_context():
            myMail = fake.email()
            user1 = User(email = myMail, password = generate_password_hash('testPassword'), name = fake.name())
            db.session.add(user1)
            user2 = User(email = fake.email(), password = generate_password_hash('testPassword'), name = fake.email())
            db.session.add(user2)
            db.session.commit()

            response = self.client.post('/api/login', json={
                'email': myMail, 'password': 'testPassword'
            })

            token = response.get_json().get('token')

            response = self.client.get('/api/users', headers={'Authorization': 'Bearer ' + token})
            self.assertIn( 'users', response.get_json())
            self.assertEqual(len(response.get_json()['users']), 2)
            self.assertEqual(response.status_code, 200)