from spitzer.lib.config.loader import ConfigLoader
from spitzer.lib.core.create import Create
from spitzer.lib.core.make_migrations import MakeMigrations
from spitzer.lib.core.migrate import Migrate
from spitzer.lib.core.migrations import Migrations
from spitzer.lib.drivers.connector import Connector
from spitzer.lib.core.install import Install


class Main(object):

    __command = str
    __working_dir = str
    __config_loader = object

    def __init__(self, command: str, wd: str, file_path: str):
        self.__command = command
        self.__working_dir = wd
        self.__config_loader = ConfigLoader(wd, file_path)

    def run(self):

        config_connections = self.__config_loader.get_connection_tartgets()
        connector = Connector(config_connections['connections'])

        targets = connector.get_connected_targets()
        path = config_connections['path']

        cmd = self.__command

        if cmd == 'install':
            Install(targets, path).run()
        elif cmd == 'create':
            Create(targets, path).run()
        elif cmd == 'show_migrations':
            Migrations(targets, path).run()
        elif cmd == 'make_migrations':
            MakeMigrations(targets, path).run()
        elif cmd == 'migrate':
            Migrate(targets, path).run()
        elif cmd == 'clear_all':
            print("Not implemented yet.")
        else:
            raise TypeError("Unrecognized command {0}".format(cmd))

        connector.release_targets()
