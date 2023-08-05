# flask-settings
Flask settings extension is similar to Django settings.

[![Build Status](https://travis-ci.org/left-join/flask-settings.svg?branch=master)](https://travis-ci.org/left-join/flask-settings)
[![Coverage Status](https://coveralls.io/repos/github/left-join/flask-settings/badge.svg?branch=master)](https://coveralls.io/github/left-join/flask-settings?branch=master)
[![Code Health](https://landscape.io/github/left-join/flask-settings/master/landscape.svg?style=flat)](https://landscape.io/github/left-join/flask-settings/master)

# Installation
```bash
pip install flask-settings
```

# How to use

File app/settings/default.py
```python
from flask_settings import BasicConfig


class DefaultConfig(BasicConfig):
    SQLALCHEMY_DATABASE_PROTOCOL = 'postgresql'
    SQLALCHEMY_DATABASE_HOST = 'localhost'
    SQLALCHEMY_DATABASE_PORT = 5432
    SQLALCHEMY_DATABASE_USERNAME = 'postgres'
    SQLALCHEMY_DATABASE_PASSWORD = 'postgres'
    SQLALCHEMY_DATABASE_NAME = 'default'

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # calculated constant
        return '{protocol}://{username}:{password}@{host}:{port}/{db}'.format(
            protocol=self.SQLALCHEMY_DATABASE_PROTOCOL,
            username=self.SQLALCHEMY_DATABASE_USERNAME,
            password=self.SQLALCHEMY_DATABASE_PASSWORD,
            host=self.SQLALCHEMY_DATABASE_HOST,
            port=self.SQLALCHEMY_DATABASE_PORT,
            db=self.SQLALCHEMY_DATABASE_NAME)

```

File app/settings/development.py
```python
from app.settings.default import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_NAME = 'development'

```

File app/settings/testing.py
```python
from app.settings.default import DefaultConfig


class TestingConfig(DefaultConfig):
    TESTING = True

    SQLALCHEMY_DATABASE_NAME = 'testing'

```

File app/settings/production.py
```python
from app.settings.default import DefaultConfig


class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_HOST = '10.0.0.1'
    SQLALCHEMY_DATABASE_USERNAME = 'user'
    SQLALCHEMY_DATABASE_PASSWORD = 'password'
    SQLALCHEMY_DATABASE_NAME = 'production'

```

File app/application.py
```python
from flask import Flask
from flask_settings import Settings
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

settings = Settings(app)

db = SQLAlchemy(app)
db.create_all(app=app)


@app.route('/')
def index_page():
    return 'database name: ' + settings.SQLALCHEMY_DATABASE_NAME


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

```

The global settings variable can be used in any module with application context:
```
from flask import Blueprint
from flask_settings.globals import settings


bp = Blueprint(__name__, __name__)


@bp.route('/')
def index_page():
    return 'database name: ' + settings.SQLALCHEMY_DATABASE_NAME

```

Run application in development mode:
```bash
FLASK_SETTINGS="development" python app/application.py
```

Run application tests in testing mode:
```bash
FLASK_SETTINGS="testing" nosetests
```

Run application in production mode:
```bash
FLASK_SETTINGS="production" uwsgi --wsgi-file=app/application.py --callable=app --http=0.0.0.0:5000
```
