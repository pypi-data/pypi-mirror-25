"""Proxy objects that allows a convenient interface to thrift connections."""

# Setup logging
import logging.config
from logging import NullHandler
from .client import TClient
from .server import TServer

logging.getLogger(__name__).addHandler(NullHandler())
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] (%(asctime)s) %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
})
