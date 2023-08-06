from __future__ import absolute_import, print_function, unicode_literals

import logging


def setup_logging(verbose=False, debug=False):
    log_level = logging.WARN
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    logging.getLogger('urllib3').setLevel(logging.WARN)
