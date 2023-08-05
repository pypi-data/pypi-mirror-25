import os
from django.db import connections


class Connector(object):
    """
    Adds each target to the Django's ORM connection handler
    """
    __targets = list()

    def __init__(self, config_connections: list):
        self.__connect_targets(config_connections)

    def __connect_targets(self, config_connections):

        for conn in config_connections:
            db_id = os.urandom(8).hex()
            connections.databases[db_id] = {
                "id": db_id,
                "HOST": conn['host'],
                "NAME": conn['name'],
                "USER": conn['user'],
                "PASSWORD": conn['password'],
                "ENGINE": self.get_db_engine(conn['driver']),
                "PORT": conn['port'],
                "CHARSET": conn['charset'] if 'charset' in conn else 'utf-8',
                "AUTOCOMMIT": False,
            }

            self.__targets.append(db_id)
        return self

    @staticmethod
    def get_db_engine(driver: str):
        if driver == 'mysql':
            return 'mysql_cymysql'
        elif driver == 'sqlite':
            return 'django.db.backends.sqlite3'
        elif driver == 'postgres':
            return 'django.db.backends.postgresql'
        elif driver == 'oracle':
            return 'django.db.backends.oracle'

    def get_connected_targets(self):
        return self.__targets

    def release_targets(self):
        for target in self.__targets:
            connections[target].close()
        return True
