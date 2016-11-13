from flask import Flask

from app.models import db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)

    return app
