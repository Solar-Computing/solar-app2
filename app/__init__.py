from flask import Flask

from app.models import db
from app.controllers.api import api

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)

    app.register_blueprint(api, url_prefix='/api')

    return app
