# Djotali

[![Build status](https://travis-ci.org/Botilab/djotali.svg?branch=master)](https://travis-ci.org/Botilab/djotali)
[![PyPI version](https://badge.fury.io/py/djotali.svg)](https://badge.fury.io/py/djotali)

Our SAAS solution to easily send messages to your clients

## Requirements
Python >= 3.6
`python3 -m venv venv the first time`
`source venv/bin/activate`
`pip install -r requirements.txt`

## Installation
* Setup your database. You can set a DB URL in the .env file with the same pattern than the one visible in the settings.
For sqlite : `sqlite:///dev.sqlite3`

* ``` python manage.py migrate```

* ``` python manage.py seed```

* ```python manage.py runserver```

## Run the lint and tests
`flake8 && python manage.py test`

## Make migrations
`python manage.py makemigrations contacts && python manage.py makemigrations campaigns`

## Create a version
`fab tag_version` to bump the version, tag the bumped version and push it to origin  
`fab -d tag_version` for more info  
The tag creation trigger pypi artifact and docker containers creations

## Deploy a version
`fab deploy VERSION -H host_ip -u app_user -i path_to_private_key` to deploy an existing version

## Use .env file for configuration
Example of content  
```
DATABASE_URL=sqlite:///dev.sqlite3
CELERY_BROKER_URL=memory://localhost:8000//
```
