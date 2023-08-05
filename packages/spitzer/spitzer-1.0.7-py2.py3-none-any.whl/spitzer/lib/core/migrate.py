import hashlib
import os

import sys

from spitzer.lib.core.connection import Connection
from spitzer.lib.core.reader import Reader
from spitzer.lib.models.spitzer_migrations import SpitzerMigrationsModel


class Migrate(Connection, Reader):

    __targets = list()
    __path = str()
    migrated = list()

    def __init__(self, targets: list, path: str):
        super(Migrate, self).__init__(targets)
        Reader.__init__(self, path)
        self.__targets = targets
        self.__path = os.path.realpath(path)

    def run(self):
        self.start_transaction()
        rollback = False
        results = list()
        for target in self.__targets:
            search = SpitzerMigrationsModel.objects.using(target).filter(executed=None).order_by('datetime')
            for line in search:
                migration = self.get_migration_content(line.migration)
                result = self.migrate(target, migration)

                if line.migration not in self.migrated:
                    self.migrated.append(line.migration)

                results.append({'target': target, 'line': line, 'result': result})

                if result['success'] is False:
                    rollback = True

        if rollback is True:
            self.rollback()
            self.register_result(results)
            raise Exception("One or more migration could not be executed successfully.")

        self.register_result(results)

        self.commit()

        if len(self.migrated) > 0:
            print("{0} migration(s) executed successfully.".format(len(self.migrated)))
        else:
            print("No pending migration found.")

        return True

    def register_result(self, results: list):
        for result in results:
            line = result['line']
            target = result['target']
            result_line = result['result']

            line.checksum = self.get_migration_checksum(line.migration)
            line.message = 'OK' if len(result_line['result']) < 1 else result_line['result']
            line.success = 1 if result_line['success'] is True else 0
            line.executed = 1

            line.save(using=target)
        return True

    def migrate(self, target: str, migration: str):
        if migration.find(';') > 0:
            for line in migration.split(';')[:-1]:
                result = self.exec_single_target(target, line)
            return result
        else:
            return self.exec_single_target(target, migration)

    def get_migration_content(self, file_name: str):
        file = "{0}/{1}".format(self.__path, file_name)
        data = None
        try:
            with open(file) as handle:
                data = handle.read()
                if len(data) < 1:
                    raise IOError("empty file.")
                handle.close()
        except BaseException as e:
            print("Migration error: {0}".format(str(e)))
            sys.exit(3)
        return data

    def get_migration_checksum(self, file_name: str):
        file = "{0}/{1}".format(self.__path, file_name)
        with open(file, 'rb') as handle:
            return hashlib.sha256(handle.read()).hexdigest()
            handle.close()
