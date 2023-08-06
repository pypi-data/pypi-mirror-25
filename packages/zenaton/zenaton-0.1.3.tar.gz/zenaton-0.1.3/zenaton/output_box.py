from __future__ import absolute_import, print_function, unicode_literals

import logging

from zenaton.errors import ZenatonError
from zenaton.serialization import (
    get_class_path,
    get_properties,
    serialize,
)
from zenaton.task import Task
from zenaton.tasks.wait import Wait
from zenaton.workflow import Workflow


DEFAULT_TIMEOUT = (2 ** 31) - 1


log = logging.getLogger(__name__)


class OutputBox:

    def __init__(self, executable, position):
        self.executable = executable
        self.position_str = str(position)

    def __repr__(self):
        return 'OutputBox(executable={}, position={})'.format(
            self.executable,
            self.position_str,
        )

    def get_work_item(self):
        log.debug('OutputBox.get_work_item()')
        data = {
            'type': self.type,
            'name': self.name,
            'position': self.position_str,
            'input': self.input,
            'timeout': self.timeout,
        }
        if hasattr(self.executable, 'get_event'):
            data['event'] = self.executable.get_event()
        log.debug('work item = %s', data)
        return data

    @property
    def type(self):
        if self.is_task():
            return 'task'
        if self.is_workflow():
            return 'workflow'
        if self.is_wait():
            return 'wait'
        if self.is_wait_while():
            return 'while'
        raise ZenatonError('Unknown type')

    @property
    def name(self):
        if self.is_wait():
            return 'Wait'
        else:
            return get_class_path(self.executable.__class__)

    @property
    def input(self):
        if self.is_wait():
            return None
        else:
            return serialize(get_properties(self.executable))

    @property
    def timeout(self):
        if self.is_wait() or self.is_wait_while():
            return self.executable.get_timeout_timestamp()
        else:
            if hasattr(self.executable, 'get_timeout'):
                return self.executable.get_timeout()
            else:
                return DEFAULT_TIMEOUT

    def is_task(self):
        return isinstance(self.executable, Task)

    def is_workflow(self):
        return isinstance(self.executable, Workflow)

    def is_wait(self):
        return isinstance(self.executable, Wait)

    def is_wait_while(self):
        return False  # FIXME
