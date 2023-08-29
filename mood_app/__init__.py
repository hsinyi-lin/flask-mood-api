from flask import Flask
from flask_cors import CORS

from .extensions import mongo
from .routes.user import user
from .routes.mood import mood


def create_app(config_object='mood_app.settings'):
    app = Flask(__name__)

    app.config.from_object(config_object)
    # CORS(app, origins='')

    mongo.init_app(app)

    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(mood, url_prefix='/mood')

    return app