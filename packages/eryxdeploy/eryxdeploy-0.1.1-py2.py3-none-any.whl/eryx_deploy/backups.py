# coding=utf-8
from datetime import datetime

from fabric.context_managers import settings
from fabric.contrib.console import confirm
from fabric.decorators import task
from fabric.operations import get
from fabric.operations import local, run, os
from fabric.utils import abort

from eryx_deploy.databases import get_remote_database, get_local_database
from eryx_deploy.utils import assert_configuration_variable_exists, get_configuration_variable

DATE_FORMAT = "%d-%m-%Y"
DATE_TIME_FORMAT = DATE_FORMAT + "-%H:%M:%S"


def list_dir(dir_path):
    if dir_path[-1] != '/':
        dir_path += '/'

    file_names = run("ls -m %s" % dir_path)
    file_names = map(lambda s: s.strip(), file_names.split(","))
    return file_names


def check_configuration():
    assert_configuration_variable_exists('REMOTE_DB_NAME')
    assert_configuration_variable_exists('LOCAL_DB_NAME')

    assert_configuration_variable_exists('REMOTE_DB_USER')
    assert_configuration_variable_exists('LOCAL_DB_USER')

    assert_configuration_variable_exists('REMOTE_DB_PASSWORD')
    assert_configuration_variable_exists('LOCAL_DB_PASSWORD')

    assert_configuration_variable_exists('DB_BACKEND')


def today_date():
    return datetime.today().strftime(DATE_FORMAT)


def today_datetime():
    return datetime.today().strftime(DATE_TIME_FORMAT)


def get_last_backup_date_time():
    date_times = []

    for file_name in list_dir("./"):
        try:
            db_name = file_name.split('+')[0]
            date_time = file_name.split('+')[-1].split('.gz')[0]
            date_time = datetime.strptime(date_time, DATE_TIME_FORMAT)

            if db_name == get_configuration_variable('REMOTE_DB_NAME'):
                date_times.append(date_time)

        except ValueError:
            pass

    if len(date_times):
        return max(date_times)


def exists_today_remote_db_backup():
    last_backup_date_time = get_last_backup_date_time()
    if last_backup_date_time:
        return last_backup_date_time.date() == datetime.today().date()
    return False


def create_db_backup_in_server():
    backup_file_name = '%s+%s.gz' % (get_configuration_variable('REMOTE_DB_NAME'), today_datetime())
    backup_file_path = os.path.join('./', backup_file_name)

    print("Haciendo un backup de la base de datos remota...")
    database = get_remote_database()
    command = database.backup_command(backup_file_path=backup_file_path)
    run(command)

    return backup_file_path


def get_last_backup_file_name():
    last_date_time = get_last_backup_date_time()
    return '%s+%s.gz' % (get_configuration_variable('REMOTE_DB_NAME'), last_date_time.strftime(DATE_TIME_FORMAT))


def download_remote_db_from_last_backup():
    backup_file_name = get_last_backup_file_name()
    backup_file_path = os.path.join('./', backup_file_name)

    possible_local_back_up_file = os.path.join('./', backup_file_name)
    if os.path.exists(possible_local_back_up_file):
        print("Ya existe un archivo con el mismo nombre, asumiendo que es el backup deseado...")
        return possible_local_back_up_file

    print("Descargando base de datos remota...")
    files_downloaded = get(backup_file_path, local_path='./')

    if backup_file_path in files_downloaded.failed:
        abort("Problema al descargar el archivo %s!" % backup_file_path)

    return files_downloaded[0]


def reload_local_db_from_last_backup():
    file_name = download_remote_db_from_last_backup()
    database = get_local_database()

    if os.path.exists(file_name):
        if confirm("La base de datos local será borrada. Desea continuar?", default=False):

            with settings(warn_only=True):
                command = database.drop_command()
                result = local(command)
                print result.return_code

            command = database.create_command()
            local(command)

            command = database.rebuild_from_backup_command(backup_file_path=file_name)
            local(command)
        else:
            abort("Abortando")
    else:
        abort("No se encontro el archivo %s!" % file_name)


def reload_remote_db_from_last_backup():
    backup_file_name = get_last_backup_file_name()
    backup_file_path = os.path.join('./', backup_file_name)

    database = get_remote_database()
    run(database.drop_command())
    run(database.create_command())
    run(database.rebuild_from_backup_command(backup_file_path))


@task
def reload_local_db_from_today_backup():
    check_configuration()

    if exists_today_remote_db_backup():
        question = "Ya existe un backup de la base de datos remota con fecha de hoy ¿Quieres crear uno de todas formas?"
        answer = confirm(question, default=True)

        if answer:
            create_db_backup_in_server()

    else:
        create_db_backup_in_server()

    reload_local_db_from_last_backup()


@task
def rollback_remote_db_to_last_backup():
    check_configuration()

    question = "SI CONTINUA CON ESTA OPERACIÓN SE ELIMINARÁ LA BASE DE DATOS REMOTA. ¿Desea continuar?"
    answer_1 = confirm(question, default=False)

    question = "!!!!!SI CONTINUA CON ESTA OPERACIÓN SE ELIMINARÁ LA BASE DE DATOS REMOTA. ¿Esta muy seguro de que " \
               "desea continuar? "
    answer_2 = confirm(question, default=False)

    if answer_1 and answer_2:
        reload_remote_db_from_last_backup()
    else:
        abort("Abortando")
