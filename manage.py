#!/usr/bin/env python

import os

from flask_script import Manager, Server

from app import create_app
from app.models import db

env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('app.settings.%sConfig' % env.capitalize())

manager = Manager(app)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db)

@manager.command
def createdb():
    db.create_all()

if __name__ == "__main__":
    manager.run()
