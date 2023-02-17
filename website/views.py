from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route('/users')
def users():
    return render_template('users.html')