"""Zenaton worker slave.

Usage:
  zenaton_slave [options] [--microserver-url=URL] INSTANCE_ID SLAVE_ID
  zenaton_slave -h | --help

Options:
  -h --help     Show this screen.
  -v --verbose  Increase log level.
  -d --debug    Increase log level even more.
"""
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
import sys

from docopt import docopt

from zenaton.compat import JSONDecodeError
from zenaton.decider import Decider
from zenaton.errors import ZenatonError
from zenaton.microserver import MicroserverAPI
from zenaton.scripts.base import setup_logging
from zenaton.task import Task


log = logging.getLogger(__name__)


class InvalidPropertiesError(ZenatonError):
    pass


def main(argv=None):
    args = docopt(__doc__, argv=argv)
    setup_logging(verbose=args['--verbose'], debug=args['--debug'])
    try:
        process_single_job(
            instance_id=args['INSTANCE_ID'],
            slave_id=args['SLAVE_ID'],
            base_url=args['--microserver-url']
        )
        sys.exit(0)
    except Exception:
        logging.exception("Unexpected error")
        sys.exit(1)


def process_single_job(instance_id, slave_id, base_url=None):
    """
    Ask the microserver for a single job and run it
    """
    microserver = MicroserverAPI(base_url=base_url)
    resp = microserver.ask_for_job(instance_id=instance_id, slave_id=slave_id)
    if 'action' in resp:
        if resp['action'] == 'DecisionScheduled':
            run_decision(
                microserver=microserver,
                uuid=resp['uuid'],
            )
        elif resp['action'] == 'TaskScheduled':
            run_task(
                microserver=microserver,
                uuid=resp['uuid'],
                hash_=resp['hash'],
                class_path=resp['name'],
                properties=resp['input'],
            )
        else:
            raise NotImplementedError


def run_decision(microserver, uuid):
    log.debug('zenaton_slave:run_decision(uuid=%s)', uuid)

    decider = Decider(uuid=uuid, microserver=microserver)
    decider.launch()


def run_task(microserver, uuid, hash_, class_path, properties):
    log.debug(
        'zenaton_slave:run_task('
        'uuid=%s, hash_=%s, class_path=%s, properties=%s)',
        uuid, hash_, class_path, properties
    )

    try:
        properties = json.loads(properties)
    except JSONDecodeError:
        msg = "Invalid JSON value for properties: '{}'".format(properties)
        raise InvalidPropertiesError(msg)

    task = Task.create(class_path, properties)

    try:
        result = task.handle()
        microserver.notify_task_success(uuid, hash_, result)
    except ZenatonError:
        etype, value, tb = sys.exc_info()
        microserver.notify_task_internal_error(uuid, hash_, etype, value, tb)
        raise
    except Exception:
        etype, value, tb = sys.exc_info()
        microserver.notify_task_user_error(uuid, hash_, etype, value, tb)
        raise
