import os


class ConfigValidator(object):

    __config = dict
    __template = {
        'host': str,
        'name': str,
        'user': str,
        'password': str,
        'driver': str,
        'port': int
    }

    def __init__(self, config: dict):
        self.__config = config

    def validate_config_file(self):
        if 'path' in self.__config and os.path.isdir(self.__config['path']) is False:
            raise NotADirectoryError(
                "Mal-formed spitzer configuration file: the path {0} doesn't exist or can't be readed."
                .format(self.__config['path'])
             )

        if 'connections' not in self.__config:
            raise ValueError("Mal-formed spitzer configuration file: missing 'connections' object.")

        if type(self.__config['connections']) is not list:
            raise ValueError("Mal-formed spitzer configuration file: 'connections' object's value should be a list.")

        i = 0
        for config in self.__config['connections']:
            for key in self.__template.keys():
                if key not in config:
                    raise ValueError("Mal-formed spitzer configuration file: connection {0} is missing the key {1}."
                                     .format(i, key))

                if type(config[key]) is not self.__template[key]:
                    raise ValueError("Mal-formed spitzer configuration file: connection {0} value for key {1} should be"
                                     " {2}. {3} given."
                                     .format(i, key, self.__template[key], type(config[key])))
                continue
            i = i + 1
        return True
