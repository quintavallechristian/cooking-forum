from dotenv import load_dotenv

load_dotenv()
import os


class Config(object):
    TESTING = False


class ProductionConfig(Config):
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")


class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:////tmp/foo.db"


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
