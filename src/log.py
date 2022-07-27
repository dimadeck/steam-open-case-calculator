import logging
from typing import Optional

from config import settings_app

LOGGER_LEVELS = {
    'sqlalchemy': logging.INFO
}

for logger, log_level in LOGGER_LEVELS.items():
    logging.getLogger(logger).setLevel(level=log_level)

_log: Optional[logging.Logger] = None


def config_logging(formatter=None, datefmt=None, level=None, output_filename=None):
    global _log
    log_levels = {'info': logging.INFO, 'debug': logging.DEBUG, 'error': logging.ERROR, 'critical': logging.CRITICAL}
    formatter = formatter or '[%(asctime)s | %(levelname)s]: %(message)s'
    datefmt = datefmt or '%d.%m.%Y %H:%M:%S'
    console_out = logging.StreamHandler()
    level = log_levels.get(level.lower(), logging.INFO)
    handlers = []
    if settings_app.LOG_CONSOLE:
        handlers.append(console_out)
    if output_filename:
        handlers.append(logging.FileHandler(output_filename))

    logging.basicConfig(handlers=handlers, format=formatter, datefmt=datefmt, level=level)
    _log = logging.getLogger()


config_logging(level=settings_app.LOG_LEVEL, output_filename=settings_app.LOG_FILENAME)


def get_log_channel(name=None):
    return _log.getChild(name) if name else _log
