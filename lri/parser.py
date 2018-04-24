import configparser
import json
import abc

class Parser(abc.ABC):
    keywordlist = []  # List of all keywords to search for in .json file
    cfg = None        # Instance of configparser.ConfigParser
    section = None

    def __init__(self, configfile=None, section=None):
        if configfile is None:
            self.configfile = "parserconfig.ini"
        else:
            self.configfile = configfile
        self.cfg = configparser.ConfigParser(allow_no_value=True)

        if section is not None:
            self.section = section

        try:
            self.cfg.read(self.configfile)
        except configparser.Error:
            print("[WARNING]: Base file parserconfig.ini not found and no file specified in Parser.__init__")
        except FileNotFoundError:
            print("[WARNING]: Base file parserconfig.ini not found and no file specified in Parser.__init__")

    # Returns a dict from read text containing keys in keywordlist
    @abc.abstractmethod
    def parse(self, text):
        pass

    # Returns a dict from a file, either filepath or fileobject must be valid or an exception will be raised
    @abc.abstractmethod
    def process(self, filepath=None, fileobject=None):
        pass

    def getKeywordList(self, section=None):
        if len(self.keywordlist) > 0:
            return self.keywordlist
        if not self.cfg:
            raise ModuleNotFoundError("No .ini file found or configured")

        if section is not None:
            self.section = section

        try:
            for key in self.cfg[self.section]:
                self.keywordlist.append(key)
        except configparser.Error as e:
            print(e)

        return self.keywordlist

    # Requires to mention the section even if a section has been specified at init
    def addSearchKey(self, section, key):
        if self.cfg is not None:
            self.cfg.set(section, key)

        with open(self.configfile, 'w') as configfile:
            self.cfg.write(configfile)
        self.getKeywordList(section)

    # Requires to mention the section even if a section has been specified at init
    def removeSearchKey(self, section, key):
        if self.cfg.has_option(section, key):
            self.cfg.remove_option(section, key)

        with open(self.configfile, 'w') as configfile:
            self.cfg.write(configfile)
        self.getKeywordList(section)



