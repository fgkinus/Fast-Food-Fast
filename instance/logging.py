"""credit to Toptal blog on advanced logging for python :https://www.toptal.com/python/in-depth-python-logging"""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

import coloredlogs

LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs\\app_logs.log')


class Logging(object):
    """Methods to handle logging"""

    @staticmethod
    def get_console_handler():
        console_handler = logging.StreamHandler(sys.stdout)
        return console_handler

    @staticmethod
    def get_file_handler():
        file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
        return file_handler

    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        # logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        coloredlogs.install(level='DEBUG', milliseconds=True)
        return logger
