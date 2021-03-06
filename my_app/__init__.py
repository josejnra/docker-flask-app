from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from my_app.config import get_config


application = Flask(__name__)
application.config.from_object(get_config())

db = SQLAlchemy(application)
db.init_app(application)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

application.register_blueprint(api_bp, url_prefix='/api')


@application.route('/')
def hello_world():
    return 'Hello World!'


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@application.errorhandler(Exception)
def handle_exception(error):
    """
        Function to handle exceptions when it is raised in the app.

        Parameters
        ----------
        error: AbstractException
            Exception to be handle.
    """
    return jsonify({'exception': str(error)})


application.register_error_handler(Exception, handle_exception)

from my_app.resources import TeamsResource, PlayersResource

# Resources
api.add_resource(TeamsResource, '/teams', '/teams/<int:id_>', strict_slashes=False)
api.add_resource(PlayersResource, '/players', '/teams/<int:id_>', strict_slashes=False)

from my_app.models import TeamsModel, PlayersModel
