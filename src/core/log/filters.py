import logging


class DebugLevelFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG


class InfoLevelFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


class WarningLevelFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING


class ErrorLevelFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR
