from collections import OrderedDict

from spitzer.lib.core.connection import Connection
from spitzer.lib.models.spitzer_migrations import SpitzerMigrationsModel

from terminaltables import AsciiTable


class Migrations(Connection):

    __targets = list()
    __path = str()

    def __init__(self, targets: list, path: str):
        super(Migrations, self).__init__(targets)
        self.__targets = targets
        self.__targets = targets

    def run(self):
        migrations = OrderedDict()
        for target in self.__targets:
            lines = SpitzerMigrationsModel.objects.using(target).all().order_by('datetime')
            migrations[target] = list()
            for line in lines:
                migrations[target].append(self.get_migration_data(line))

        return self.print_migration_data(migrations)

    @staticmethod
    def get_migration_data(line: SpitzerMigrationsModel):
        obj = OrderedDict()
        obj['id'] = line.id
        obj['migration'] = line.migration
        obj['checksum'] = line.checksum
        obj['datetime'] = line.datetime.strftime("%Y-%m-%d %H:%M:%S")
        obj['executed'] = line.executed
        obj['success'] = line.success
        obj['message'] = line.message

        return obj

    def print_migration_data(self, migrations: dict):
        i = 0
        for target in self.__targets:
            print("Migrations from target {0}".format(i))
            table_data = [
                [
                    'id', 'migration', 'checksum', 'datetime', 'executed', 'success', 'message'
                ],
            ]
            for line in migrations[target]:
                if line['executed'] == 1:
                    executed = '√'
                    success = '√' if line['success'] == 1 else 'X'
                else:
                    executed = None
                    success = None

                table_data.append([
                    line['id'],
                    line['migration'],
                    line['checksum'][0:15],
                    line['datetime'],
                    executed,
                    success,
                    line['message'][0:20] if line['message'] is not None else None
                ])
            table = AsciiTable(table_data)
            print(table.table)
            print()
            i = i + 1
        return True
