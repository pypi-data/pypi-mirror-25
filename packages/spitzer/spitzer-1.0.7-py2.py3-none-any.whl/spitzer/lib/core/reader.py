from glob import glob


class Reader(object):
    __path = str()

    def __init__(self, path):
        self.__path = path

    def get_migration_files(self):
        files = list()
        for file in glob("{0}/*.sql".format(self.__path)):
            files.append(file)

        return files
