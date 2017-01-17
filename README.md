# solar-app2
New solar-app repo using Python3/Flask

## (Install) Create and Activate Python Virtual Environment

(These directions are for bash, use `venv/bin/activate.fsh` etc for
other shells)

```bash
pip install virtualenv
virtualenv -p python3 venv # create a python virtual environment
source venv/bin/activate # activate the virtual environment
```

### Deactivating
```bash
deactivate
```

## Installation and Setup

Install dependencies.
```bash
pip install -r requirements.txt
```

Create a database (with name `solar`) on a local postgres database.

Configure your settings with secret and database credentials.
```bash
cp app/settings.py.example app/settings.py
vim app/settings.py
```

Set up tables (with SQLAlchemy) and import data (TODO)
```bash
python manage.py createdb
```

## Running the app

```bash
python manage.py runserver
```

