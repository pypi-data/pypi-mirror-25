"""Initialize the microserver.

Usage:
  zenaton_init [options] [--microserver-url=URL]
  zenaton_init -h | --help

Options:
  -h --help     Show this screen.
  -v --verbose  Increase log level.
  -d --debug    Increase log level even more.
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging
import sys

from docopt import docopt

from zenaton.config import Config
from zenaton.microserver import MicroserverAPI
from zenaton.scripts.base import setup_logging


log = logging.getLogger(__name__)


def main(argv=None):
    args = docopt(__doc__, argv=argv)
    setup_logging(verbose=args['--verbose'], debug=args['--debug'])
    try:
        init_microserver(base_url=args['--microserver-url'])
        sys.exit(0)
    except Exception:
        logging.exception("Unexpected error")
        sys.exit(1)


def init_microserver(base_url=None):
    microserver = MicroserverAPI(base_url=base_url)
    log.debug('Sending config to microserver on {}'.format(
        microserver.base_url
    ))

    config = Config().to_dict()
    log.debug(config)

    microserver.send_config(config=config)
