import os
import pathlib as pt
import secrets
import string

from datetime import timedelta

basedir = str(pt.Path.cwd())


class Config:
    ALLOWED_UPLOAD_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    DEFAULT_AVATAR_PATH = basedir + "/web_app/static/profile_photos/without_avatar.jpg"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = "app.docflow@gmail.com"
    MAIL_PASSWORD = "crdkazldbdiafeox"
    PROFILE_PHOTO_FOLDER_PATH = f"{basedir}/web_app/static/profile_photos/"
    PWD_LENGTH = 12
    PWD_GENERATE_ALPHABET = string.ascii_letters + string.digits + string.punctuation
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SECURITY_PASSWORD_SALT = secrets.token_urlsafe(64)
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
