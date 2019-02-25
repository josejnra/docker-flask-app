from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import get_config
from models import TeamsModel, PlayersModel

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


application = Flask(__name__)
application.config.from_object(get_config())

db = SQLAlchemy(application)
db.init_app(application)


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    application.run()
