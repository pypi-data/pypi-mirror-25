from fabric.api import task
from fabric.contrib.console import confirm
from fabric.operations import local, run, prompt, sudo
from fabric.utils import abort

from eryx_deploy import backups
from eryx_deploy.utils import assert_configuration_variable_exists, get_configuration_variable, inside_virtualenv, \
    inside_project_path, configuration_variable_exists


@task
def make_release_and_deploy():
    make_release()
    deploy()


@task
def deploy():
    check_configuration()

    remote_pull()
    remote_install_dependencies()
    remote_migrate()
    remote_collect_static()

    restart_webserver()


@task
def make_release():
    ready_for_release = confirm("Are you currently in 'dev' branch with everything merged and pulled (clean tree!), "
                                "ready to make a release?",
                                default=False)

    if not ready_for_release:
        abort("Prepare everything and try again!")

    run_tests()

    local('git fetch --tags')

    print("Latest git tag: ")
    # FIXME: This fails if no previous tag is found
    local('git describe --abbrev=0')

    version = prompt('Version: ', validate='^\d{1,3}[.]\d{1,2}[.]\d{1,2}')

    local('git checkout master')
    pull()

    local('git merge dev')
    local('git tag -a \'%s\' -m \'Release version %s\'' % (version, version))

    push(include_tags=True)

    # Back to dev
    local('git checkout dev')


def check_configuration():
    backups.check_configuration()

    assert_configuration_variable_exists('PROJECT_REMOTE_PATH')
    assert_configuration_variable_exists('VIRTUAL_ENV_PATH')
    assert_configuration_variable_exists('REQUIREMENTS_FILE_PATH')

    assert_configuration_variable_exists('DB_BACKEND')
    assert_configuration_variable_exists('REMOTE_DB_NAME')
    assert_configuration_variable_exists('REMOTE_DB_USER')

    if get_configuration_variable('DB_BACKEND') == 'mysql':
        assert_configuration_variable_exists('REMOTE_DB_PASSWORD')


def run_tests():
    if get_configuration_variable('RUN_TESTS_BEFORE_RELEASE', True):
        if configuration_variable_exists('TEST_SETTINGS'):
            local('python manage.py test --settings="%s"' % get_configuration_variable('TEST_SETTINGS'))
        else:
            local('python manage.py test')


def pull():
    local('git pull')


def push(include_tags=False):
    local('git push')

    if include_tags:
        local('git push --tags')


@inside_project_path
def remote_pull():
    run('git pull')


@inside_project_path
@inside_virtualenv
def remote_install_dependencies():
    should_run_migrations = confirm('Upgrade dependencies?', default=False)

    if should_run_migrations:
        requirements_file_path = get_configuration_variable('REQUIREMENTS_FILE_PATH')
        run('pip install -Ur %s' % requirements_file_path)


@inside_project_path
@inside_virtualenv
def remote_migrate():
    should_run_migrations = confirm('Run migrations?', default=False)
    if should_run_migrations:
        backups.create_db_backup_in_server()
        run('python manage.py migrate')


@inside_project_path
@inside_virtualenv
def remote_collect_static():
    should_collect_static = confirm('Collect static?', default=False)
    if should_collect_static:
        run('python manage.py collectstatic')


def restart_webserver():
    should_restart_apache = confirm('Restart apache?', default=False)

    if should_restart_apache:
        sudo('apache2ctl -k graceful')
