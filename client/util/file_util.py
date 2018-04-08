try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

DEFAULT_CONFIG_PATH = '..'


def load_file_config(config_file_path):
    config_parser = ConfigParser()
    config_parser.optionxform = str
    config_parser.read(config_file_path)

    return dict((key, val) for key, val in config_parser.items('default'))
