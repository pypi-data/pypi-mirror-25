import re
from spitzer.lib.core.connection import Connection


class Install(Connection):

    __path = str()

    def __init__(self, targets: list, path: str):
        super(Install, self).__init__(targets)
        self.__path = path

    def run(self):
        meta_table = re.sub(re.compile('[\n]|[\s\s]{2}'), '', self.get_meta_table_template())
        self.exec_query(meta_table)
        print("Spitzer successfully instaled =)")
        return True

    @staticmethod
    def get_meta_table_template():
        return """
            CREATE TABLE IF NOT EXISTS `spitzer_migrations` (
              `id` VARCHAR(30) PRIMARY KEY NOT NULL,
              `migration` VARCHAR(300) NOT NULL,
              `checksum` VARCHAR(255) NOT NULL COMMENT 'SHA256',
              `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              `executed` INT(1) DEFAULT '0',
              `success` INT(1) DEFAULT '0',
              `message` VARCHAR(255) DEFAULT NULL
            );
        """
