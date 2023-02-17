from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from .config import ProductionConfig


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config.from_object(ProductionConfig())

    db.init_app(app)
    mail.init_app(app)

    from .api import api
    from .views import views
    from . import models
    
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(views)


    with app.app_context():
        db.create_all()

    return app