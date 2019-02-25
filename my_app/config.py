import os
import importlib

USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']


class BaseConfig:
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = None
    HASH_SECRET_KEY = '^F3g-h2%voJlXvl2OxE78b&jL@pdkzIWVSb#^_B-FNZQsQle0MY!v0Ljy5bnhoEc'


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'mysql://' + USER + ':' + PASSWORD + '@db-test/flask-db'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://' + USER + ':' + PASSWORD + '@db-dev/flask-db'


def get_config():
    return getattr(importlib.import_module('my_app.config'),
                   os.environ['FLASK_ENV'].capitalize() + 'Config')
