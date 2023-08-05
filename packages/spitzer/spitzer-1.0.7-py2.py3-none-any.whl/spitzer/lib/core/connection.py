from django.db import connections, transaction


class Connection(object):

    __targets = list

    def __init__(self, targets: list):
        self.__targets = targets

    def get_targets(self):
        return self.__targets

    def exec_query(self, sql: str, create=False):
        if create is False:
            self.start_transaction()
        rollback = False
        result = dict()
        for target in self.__targets:
            cursor = connections[target].cursor()
            try:
                cursor.execute(sql)

                result[target] = {
                    'success': True,
                    'result': cursor.fetchall()
                }
            except BaseException as e:
                rollback = True

                result = {
                    'success': False,
                    'result': str(e)
                }

                if create is False:
                    self.rollback()

                if create is True:
                    raise RuntimeError("Spitzer could not install: {0}".format(e))

        if rollback is False and create is False:
            self.commit()

        return result

    @staticmethod
    def exec_single_target(target: str, query: str):
        try:
            cursor = connections[target].cursor()
            cursor.execute(query)

            result = {
                'success': True,
                'result': cursor.fetchall()
            }
        except BaseException as e:
            result = {
                'success': False,
                'result': str(e)
            }

        return result

    def start_transaction(self):
        for target in self.__targets:
            transaction.savepoint(using=target)
            transaction.atomic(using=target)
        return self

    def commit(self):
        for target in self.__targets:
            transaction.commit(using=target)
        return self

    def rollback(self):
        for target in self.__targets:
            transaction.rollback(using=target)
        return self
