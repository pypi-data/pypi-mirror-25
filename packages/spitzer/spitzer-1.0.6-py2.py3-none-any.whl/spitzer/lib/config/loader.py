import os

from spitzer.lib.config.parser import ConfigParser
from spitzer.lib.config.validator import ConfigValidator


class ConfigLoader(object):
    __working_dir = str
    __configuration_file = str

    def __init__(self, wd: str):
        self.__working_dir = os.path.realpath(wd)
        self.load_config_file()

    def load_config_file(self):
        spitzer_file = "{0}/spitzer.yaml".format(self.__working_dir)

        if not os.path.isfile(spitzer_file):
            raise IOError("Spitzer could not find a spitzer.yaml file in {0}.\n"
                          "To initialize a porject, please create a spitzer.yaml file as described in "
                          " https://github.com/feliphebueno/Spitzer/wiki/spitzer.yaml".format(self.__working_dir))
        self.__configuration_file = spitzer_file
        return self

    def get_connection_tartgets(self):
        parser = ConfigParser(self.__configuration_file)

        config_contents = parser.get_parsed_file()

        validator = ConfigValidator(config_contents)

        if validator.validate_config_file() is True:
            return config_contents
