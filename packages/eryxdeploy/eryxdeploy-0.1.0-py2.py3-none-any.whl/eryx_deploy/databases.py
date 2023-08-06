from eryx_deploy.utils import get_configuration_variable


class Database(object):
    def __init__(self, name, user, password=None):
        self.name = name
        self.user = user
        self.password = password

    def drop_command(self):
        raise NotImplementedError('subclass responsibility')

    def create_command(self):
        raise NotImplementedError('subclass responsibility')

    def backup_command(self, backup_file_path):
        raise NotImplementedError('subclass responsibility')

    def rebuild_from_backup_command(self, backup_file_path):
        raise NotImplementedError('Not implemented yet')

    @classmethod
    def to_handle(cls, db_backend):
        for database_subclass in cls.__subclasses__():
            if database_subclass.can_handle(db_backend):
                return database_subclass

        raise Exception('No database found for %s' % db_backend)


class MySqlDatabase(Database):
    @classmethod
    def can_handle(cls, db_backend):
        return db_backend == 'mysql'

    def drop_command(self):
        return "sudo mysqladmin -p drop %s" % self.name

    def create_command(self):
        return "sudo mysqladmin -p create %s" % self.name

    def backup_command(self, backup_file_path):
        return 'mysqldump -u %s -p%s %s | gzip > %s' % (self.user, self.password, self.name, backup_file_path)

    def rebuild_from_backup_command(self, backup_file_path):
        return "gunzip -c %(backup_file_path)s | sudo mysql -p %(db)s" % {'backup_file_path': backup_file_path,
                                                                          'db': self.name}


class PostgresDatabase(Database):
    def drop_command(self):
        return "sudo -u %s dropdb %s" % (self.user, self.name)

    def create_command(self):
        return "sudo -u %s createdb %s" % (self.user, self.name)

    def backup_command(self, backup_file_path):
        return 'sudo -u %s pg_dump %s | gzip > %s' % (self.user, self.name, backup_file_path)

    def rebuild_from_backup_command(self, backup_file_path):
        return "gunzip -c %s | sudo -u %s psql %s" % (backup_file_path, self.user, self.name)

    @classmethod
    def can_handle(cls, db_backend):
        return db_backend == 'postgres'


def get_local_database():
    db_backend = get_configuration_variable('DB_BACKEND')
    db_name = get_configuration_variable('LOCAL_DB_NAME')
    db_user = get_configuration_variable('LOCAL_DB_USER')
    db_password = get_configuration_variable('LOCAL_DB_PASSWORD', None)

    database_class = Database.to_handle(db_backend)

    return database_class(name=db_name, user=db_user, password=db_password)


def get_remote_database():
    db_backend = get_configuration_variable('DB_BACKEND')
    db_name = get_configuration_variable('REMOTE_DB_NAME')
    db_user = get_configuration_variable('REMOTE_DB_USER')
    db_password = get_configuration_variable('REMOTE_DB_PASSWORD', None)

    database_class = Database.to_handle(db_backend)

    return database_class(name=db_name, user=db_user, password=db_password)
