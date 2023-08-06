

import logging
import os

import yaml

logger = logging.getLogger()


class SmartConfigFile():
    POSSIBLE_FOLDERS = ["/etc/default",
                        os.path.join(os.path.expanduser("~"), ".sibus"),
                        os.getcwd(),
                        ]
    DEFAULT_CONFIGILE = "sibus.yml"

    def __init__(self, configfile=None):
        self.__set_configfile(configfile)
        self.load()

    def __set_configfile(self, configfile):
        if configfile is None:
            configfile = self.DEFAULT_CONFIGILE

        self.configfilepath = self.__find_configfile(configfile)

        if self.configfilepath is None:
            logger.error("No Config file found! "+ configfile)
            raise Exception("No Config file found: '%s' in %s"%(configfile, str(self.POSSIBLE_FOLDERS)))

    def __find_configfile(self, configfile):
        for folder in self.POSSIBLE_FOLDERS:
            t = os.path.join(folder, configfile)
            if os.path.isfile(t):
                logger.info("Config file found in: " + folder)
                return t
            else:
                logger.warning("Config file not found in: "+folder)
        return None

    def load(self):
        stream = file(self.configfilepath, 'r')
        self.__config = yaml.load(stream)

    def get(self, keys, default_value=None):
        dct = self.__config
        for key in keys:
            try:
                dct = dct[key]
            except KeyError:
                return default_value
        return dct






