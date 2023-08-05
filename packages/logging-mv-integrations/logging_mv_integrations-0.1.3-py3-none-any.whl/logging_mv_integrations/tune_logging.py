import logging
import logging.config
from .logging_json_formatter import LoggingJsonFormatter


class CustomAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):

        extra = kwargs.get('extra')
        if extra:
            kwargs['extra'].update({'version': self.extra['version']})
        else:
            kwargs['extra'] = {'version': self.extra['version']}
        return msg, kwargs


def get_logging_level(str_logging_level):

    assert str_logging_level
    str_logging_level = str_logging_level.upper()

    return {
        'NOTSET': logging.NOTSET,
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }.get(str_logging_level, logging.INFO)


def get_logger(logger_name, logger_version=None, logger_level=logging.INFO, logger_format=None):

    formatter = LoggingJsonFormatter(
        logger_name,
        logger_version,
        fmt='%(asctime)s %(levelname)s %(name)s %(version)s %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)
    logger.addHandler(handler)

    adapter = CustomAdapter(logger, {'version': logger_version})

    return adapter





