import os
from app import create_app

env = os.environ.get('APPNAME_ENV', 'dev')
application = create_app('app.settings.%sConfig' % env.capitalize())

if __name__ == "__main__":
    application.run()