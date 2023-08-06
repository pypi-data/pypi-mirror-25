from datetime import date
from functools import wraps

from fabric.context_managers import prefix, cd
from fabric.state import env


def today():
    return str(date.today())


def assert_configuration_variable_exists(var_name):
    if var_name not in env.conf:
        raise Exception('%s environment variable is not defined.' % var_name)


def configuration_variable_exists(var_name):
    return var_name in env.conf


def get_configuration_variable(var_name, default=None):
    return env.conf.get(var_name, default)


def virtualenv():
    virtual_env_path = get_configuration_variable('VIRTUAL_ENV_PATH')
    return prefix('source %s/bin/activate' % virtual_env_path)


def project_path():
    the_project_path = get_configuration_variable('PROJECT_REMOTE_PATH')
    return cd(the_project_path)


def inside_virtualenv(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with virtualenv():
            return func(*args, **kwargs)

    return inner


def inside_project_path(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with project_path():
            return func(*args, **kwargs)

    return inner
