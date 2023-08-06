from __future__ import absolute_import, print_function, unicode_literals

import logging

from zenaton.errors import ZenatonError
from zenaton.serialization import Serializable
from zenaton.task import Task
from zenaton.tasks.wait import Wait


log = logging.getLogger(__name__)


class NotExecutableError(ZenatonError):
    pass


class Workflow(Serializable):
    """
    Base class for workflows.
    """

    def handle(self):
        """
        You need to implement this method in your derived class.
        """
        raise NotImplementedError  # pragma: nocover

    def execute(self, *executables, **kwargs):
        log.debug('Workflow.execute(args=%s, kwargs=%s)', executables, kwargs)
        for executable in executables:
            if not isinstance(executable, (Task, Workflow, Wait)):
                raise NotExecutableError("'{}' is not a Task or a Workflow")
        async_ = kwargs.pop('async_', False)
        if self._is_running_within_zenaton():
            return self.__zenaton_executor__.execute(self, executables, async_)
        else:
            return self._execute_normal(executables, async_=async_)

    def _is_running_within_zenaton(self):
        return getattr(self, '__zenaton_executor__', None) is not None

    def _execute_normal(self, executables, async_):
        outputs = []
        for executable in executables:
            outputs.append(executable.handle())
        if executables and not async_:
            return outputs if len(outputs) > 1 else outputs[0]

    def execute_async(self, *executables):
        return self.execute(*executables, async_=True)
