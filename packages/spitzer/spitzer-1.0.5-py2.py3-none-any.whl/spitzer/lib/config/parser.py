import yaml


class ConfigParser(object):
    """
    Parses the configuration file contents into a python dictionary object
    """

    __file_contents = dict

    def __init__(self, file_path: str):
        self.__parse_config_file(file_path)

    def __parse_config_file(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                loaded = yaml.safe_load(file)

                if len(loaded) < 1:
                    raise ValueError("Spitzer could not parse configuration file: blank file.")

                self.__file_contents = loaded

        except OSError as e:
            raise IOError("Spitzer could not parse configuration file: {0}".format(str(e)))

    def get_parsed_file(self):
        return self.__file_contents
