# solar-app2
New solar-app repo using Python3/Flask

## Prerequisite Tools
### `virtualenv`
`virtualenv` is a tool to create isolated Python environments. For development in this project, the use of a new `virtualenv` is highly recommended.

#### Installing `virtualenv`
```bash
$ sudo pip install virtualenv
```

#### Creating and Using `virtualenv`
The following instructions are targetted for Unix's `bash` shell. Be sure to create the virtual environment *outside* the repository.
```bash
$ virtualenv -p python3 venv    # create a python virtual environment named 'venv' using python3
$ source venv/bin/activate      # activate (or enter) the virtual environment
$ deactivate                    # deactivate (or leave) the virtual environment
```


### `pip-tools`
`pip-tools` is a set of command line tools built around `pip` that install, manage, update, and synchronize Python packages.

#### Installing `pip-tools`
Run the following inside the correct Python environment (typically a virtual environment).
```bash
$ pip install --upgrade pip     # ensure pip>=6.1
$ pip install pip-tools
```

#### Compiling Dependencies
Dependencies are specified inside [requirements.in](requirements.in). To build or update the [requirements.txt](requirements.txt) list, run the following command inside the desired Python environment.
```bash
$ pip-compile requirements.in
```

#### Installing Dependencies
Given that the dependencies listed in [requirements.txt](requirements.txt) are up-to-date, run the following command to synchronize the current environment's packages with the requirements.
```bash
$ pip-sync
```



## Setting Up Databases
Create a database (with the name `solar`) on a local postgres database.

Configure your settings with secret and database credentials.
```bash
$ cp app/settings.py.example app/settings.py
$ vim app/settings.py
```

Set up tables (with SQLAlchemy) and import data (TODO)
```bash
$ python manage.py createdb
```

## Running the Server

```bash
$ python manage.py runserver
```

