# solar-app2
New solar-app repo using Python3/Flask

## Installation and Setup

### Installing `virtualenv`
`virtualenv` is a tool to create isolated Python environments. For development in this project, the use of a new `virtualenv` is highly recommended.
```bash
$ sudo pip install virtualenv
```

### Installing `pip-tools`
`pip-tools` is a set of Python command line tools that manages `pip`-based packages. **Note:** `pip-tools` requires `pip` version 6.1 or higher.
```bash
$ sudo pip install pip-tools
```

### Creating and Using `virtualenv`
The following instructions are targetted for Unix's `bash` shell. Be sure to create the virtual environment *outside* the repository.
```bash
$ virtualenv -p python3 venv  # create a python virtual environment named 'venv' using python3
$ source venv/bin/activate    # activate (or enter) the virtual environment
$ deactivate                  # deactivate (or leave) the virtual environment
```

### Installing Dependencies
Install dependencies inside the `virtualenv`.
```bash
(venv)$ pip-compile requirements.in
```

### Setting Up Databases
Create a database (with the name `solar`) on a local postgres database.

Configure your settings with secret and database credentials.
```bash
(venv)$ cp app/settings.py.example app/settings.py
(venv)$ vim app/settings.py
```

Set up tables (with SQLAlchemy) and import data (TODO)
```bash
(venv)$ python manage.py createdb
```

## Running the app

```bash
(venv)$ python manage.py runserver
```

