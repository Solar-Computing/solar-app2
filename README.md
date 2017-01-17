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

```bash
pip install -r requirements.txt
cp app/settings.py.example app/settings.py
vim app/settings.py # edit the database urls and secrets for your env
```

## Running the app

```bash
python manage.py runserver
```

