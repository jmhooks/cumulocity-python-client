"""Module for setting up a logger object"""
import logging
from logging.handlers import RotatingFileHandler
import sys

LOG_PATH = '/var/log'
LOG_FILE = LOG_PATH + '/uiot_client.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def get_rotating_handler():
    rotating_handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=9)
    rotating_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)
    rotating_handler.setFormatter(formatter)
    return rotating_handler


def get_stdout_handler():
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    stdout_handler.setFormatter(formatter)
    return stdout_handler


def get_logger(name):
    """Returns logger based on log name provided"""

    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)
    logger = logging.getLogger(name)

    logger.addHandler(get_rotating_handler())
    logger.addHandler(get_stdout_handler())

    logger.propagate = False

    return logger
