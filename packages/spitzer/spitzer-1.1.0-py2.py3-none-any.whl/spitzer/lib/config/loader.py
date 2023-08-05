import os

from spitzer.lib.config.parser import ConfigParser
from spitzer.lib.config.validator import ConfigValidator


class ConfigLoader(object):
    __working_dir = str
    __configuration_file = str
    __file_path = None

    def __init__(self, wd: str, file_path: str):
        self.__working_dir = os.path.realpath(wd)
        self.__file_path = file_path
        self.load_config_file()

    def load_config_file(self):
        if self.__file_path is None:
            spitzer_file = "{0}/spitzer.yaml".format(self.__working_dir)
        else:
            spitzer_file = self.__file_path

        if not os.path.isfile(spitzer_file):
            raise IOError("Spitzer could not find a spitzer.yaml file in {0}.\n"
                          "To initialize a porject, please create a spitzer.yaml file as described in "
                          " https://github.com/feliphebueno/Spitzer/wiki/spitzer.yaml".format(spitzer_file))
        self.__configuration_file = spitzer_file
        return self

    def get_connection_tartgets(self):
        parser = ConfigParser(self.__configuration_file)

        config_contents = parser.get_parsed_file()

        validator = ConfigValidator(config_contents)

        if validator.validate_config_file() is True:
            return config_contents
