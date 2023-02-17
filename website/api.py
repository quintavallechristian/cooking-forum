from flask import request, jsonify, make_response
from  werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
import jwt
from datetime import datetime, timedelta
from functools import wraps
from .models import User
from . import db
from .controllers import AuthController
from .controllers.UserController import getUser

from flask import current_app


api = Blueprint('api', __name__)

# function to check jwt
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'error' : 'missing auth token'}), 401
  
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            current_user = User.query\
                .filter_by(id = data['id'])\
                .first()
        except:
            return jsonify({
                'error' : 'invalid token'
            }), 401
        return  f(current_user, *args, **kwargs)
  
    return decorated
  
@api.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'id': user.id,
            'name' : user.name,
            'email' : user.email
        })
  
    return jsonify({'users': output})
  
@api.route('/login', methods =['POST'])
def login():
    auth = request.json
  
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            jsonify({'error': 'Could not verify'}),
            403,
        )
    response, code = AuthController.login(auth.get('email'), auth.get('password'))
    return make_response(jsonify(response), code)

@api.route('/verify', methods =['POST'])
def verify():
    auth = request.json
  
    if not auth or not auth.get('email') or not auth.get('password')  or not auth.get('otp'):
        return make_response(
            jsonify({'error': 'Could not verify'}),
            403,
        )
    response, code = AuthController.login(auth.get('email'), auth.get('password'), auth.get('otp'))
    return make_response(jsonify(response), code)
  
# signup route
@api.route('/signup', methods =['POST'])
def signup():
    data = request.json
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
    has2fa = data.get('has2fa')
    
    response, code = AuthController.signup((name, email, password, has2fa))

    return make_response(jsonify(response),code)
