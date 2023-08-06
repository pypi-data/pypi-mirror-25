import logging
import coloredlogs

DEFAULT_LEVEL = 'DEBUG'
DEFAULT_FORMAT = '%(asctime)s %(processName)s [%(levelname)s] %(message)s'
DEFAULT_DATE_FORMAT = '%d-%m-%y %H:%M:%S'


def init_logger(logger_name, level=DEFAULT_LEVEL, fmt=DEFAULT_FORMAT, date_fmt=DEFAULT_DATE_FORMAT):
    """Initialize logger.

    - Create a logger instance
    - Initialize a colored log instance

    :param str logger_name: logger name.
    :param str level: log level (e.g 'DEBUG')
    :param str fmt: log messages format.
    :param str date_fmt: log messages date format.

    :return: logging.Logger instance.
    """
    new_logger = logging.getLogger(logger_name)
    new_logger.setLevel(logging.DEBUG)
    coloredlogs.install(level=level, logger=new_logger, fmt=fmt, datefmt=date_fmt)
    return new_logger


logger = init_logger(logger_name='scraping-tools')
