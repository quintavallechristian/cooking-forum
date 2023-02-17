from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '4a27ffca0a21da'
    app.config['MAIL_PASSWORD'] = 'b2975e6fc78e72'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_FROM_NAME'] = 'cooking@forum.com'

    db.init_app(app)
    mail.init_app(app)

    from .auth import auth
    from .api import api
    from .views import views
    from . import models
    
    app.register_blueprint(auth)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(views)


    with app.app_context():
        db.create_all()

    return app