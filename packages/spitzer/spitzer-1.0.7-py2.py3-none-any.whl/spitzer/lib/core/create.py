import hashlib
import os
from datetime import datetime

from spitzer.lib.core.connection import Connection
from spitzer.lib.models.spitzer_migrations import SpitzerMigrationsModel


class Create(Connection):

    __path = str
    __targets = list

    def __init__(self, targets: list, path):
        super(Create, self).__init__(targets)
        self.__path = os.path.realpath(path)
        self.__targets = targets

    def run(self):

        file_name = "{0}.sql".format(datetime.now().strftime("%Y%m%d%H%M%S"))
        self.save_migration_file(file_name)

        model = SpitzerMigrationsModel()

        model.id = os.urandom(15).hex()
        model.migration = file_name
        model.checksum = hashlib.sha256(open("{0}/{1}".format(self.__path, file_name), 'rb').read()).hexdigest()

        self.start_transaction()

        for target in self.__targets:
            try:
                model.save(using=target)
                self.commit()
            except BaseException as e:
                self.rollback()
                print("Spitzer could not create the migration file: {0}".format(str(e)))

        print("Migration file created on {0}/{1}.".format(self.__path, file_name))
        return True

    def save_migration_file(self, file_name: str):
        file = open("{0}/{1}".format(self.__path, file_name), "w+")
        file.write(self.file_temlate())
        file.close()
        return True

    @staticmethod
    def file_temlate():
        return """-- Migration file created on {0}\n""".format(datetime.now().strftime("%Y-%m-%d% %H:%M:%S"))
