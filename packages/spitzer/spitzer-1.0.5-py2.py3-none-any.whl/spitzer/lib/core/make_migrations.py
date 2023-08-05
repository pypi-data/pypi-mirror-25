import os
import hashlib

from django.db import transaction

from spitzer.lib.core.connection import Connection
from spitzer.lib.models.spitzer_migrations import SpitzerMigrationsModel
from spitzer.lib.core.reader import Reader


class MakeMigrations(Connection, Reader):

    __targets = list
    __path = str
    files_registered = list()

    def __init__(self, targets: list, path: str):
        super(MakeMigrations, self).__init__(targets)
        Reader.__init__(self, path)
        self.__targets = targets
        self.__path = os.path.realpath(path)

    def run(self):
        migrations_file = self.get_migration_files()
        self.process_migration_files(migrations_file)

        if len(self.files_registered) > 0:
            print(
                "{0} unique(s) migration file(s) registered for at least one target. Run spitzer migrate."
                .format(len(self.files_registered))
            )
        else:
            print("No unregistered migration file was found.")

        return True

    def process_migration_files(self, migrations_file: dict):
        for file in migrations_file:
            file_spl = file.split('/')
            file_spl.reverse()
            file_name = file_spl[0]
            i = 0
            for target in self.__targets:
                search = SpitzerMigrationsModel.objects.using(target).filter(migration=file_name)
                if len(search) < 1:
                    self.make_migration(file_name, target)
                    print("Migration file registered on {0}/{1} for target {2}.".format(self.__path, file_name, i))
                    i += 1
                    if file_name not in self.files_registered:
                        self.files_registered.append(file_name)

    def make_migration(self, file_name: str, target: str):
        model = SpitzerMigrationsModel()

        model.id = os.urandom(15).hex()
        model.migration = file_name
        model.checksum = hashlib.sha256(open("{0}/{1}".format(self.__path, file_name), 'rb').read()).hexdigest()

        transaction.atomic(using=target)
        try:
            model.save(using=target)
            transaction.commit(using=target)
        except BaseException as e:
            transaction.rollback(using=target)
            print("Spitzer could not register the migration file: {0}".format(str(e)))

        return True
