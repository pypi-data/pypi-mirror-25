# Eryx Deploy

This tool automates deployment for apps developed on Eryx using Fabric. 
For now, it's focused on apps with a Django-based backend.

*ALPHA status*

## Features

- Support for upgrade deployments. No initial deployment support for now (in progress).
- Support for MySQL and PostgreSQL DBs.
- Does DB backups before migrations.
- Can fetch a remote DB copy and install it locally.
- Ask for confirmation on every step.

**Tests are missing for now, so use this with caution!**

## Usage

### Setup

1. Add ``eryxdeploy`` to your dev requirements and update them.
2. Create a fabfile.py with project configuration on your project's root dir.

Sample file:

````
from eryx_deploy import *

env.user = 'root'
env.hosts = ['staging.project-name.com']  # remote host where deployment should take place

env.conf = {
    'DB_BACKEND': 'postgres',  # or 'mysql'
    
    'PROJECT_REMOTE_PATH': '/var/www/master/project_name',
    'VIRTUAL_ENV_PATH': '/var/www/master/project_name/bootstrap',
    'REQUIREMENTS_FILE_PATH': '/var/www/master/project_name/requirements/master.txt',
    
    'RUN_TESTS_BEFORE_RELEASE': True,
    'TEST_SETTINGS': "django_package_name.test_settings",
    
    'REMOTE_DB_NAME': 'db_name',
    'REMOTE_DB_USER': 'postgres',
    'REMOTE_DB_PASSWORD': None,
    
    'LOCAL_DB_NAME': 'db_name_dev',
    'LOCAL_DB_USER': 'postgres',
    'LOCAL_DB_PASSWORD': None,
}
````

### Release and deploy

1. Make a new release with (should be inside your virtualenv!):

````
$ fab make_release
````

2. ...and deploy:

````
$ fab deploy
````

Optionally, you can do the release and deploy altogether with:

````
$ fab make_release_and_deploy
````

### Other useful commands

- ``fab reload_local_db_from_today_backup``: Creates a remote DB backup, downloads it and reloads DB from local 
environment.
- ``fab rollback_remote_db_to_last_backup``: Re-creates remote DB from last remote backup.