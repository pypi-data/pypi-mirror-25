from __future__ import absolute_import, print_function, unicode_literals

import logging

from zenaton.errors import ZenatonError
from zenaton.output_box import OutputBox
from zenaton.position import Position
from zenaton.serialization import deserialize


log = logging.getLogger(__name__)


class DeciderWasModifiedError(ZenatonError):
    pass


class ScheduledBoxException(ZenatonError):
    pass


class WorkflowExecutor:

    def __init__(self, uuid, microserver):
        self.uuid = uuid
        self.microserver = microserver
        self.position = Position()

    def execute(self, workflow, executables, async_):
        log.debug(
            'WorkflowExecutor.execute(workflow=%s, executables=%s, async_=%s)',
            workflow,
            executables,
            async_,
        )

        boxes = self._build_boxes(executables, async_)
        resp = self.microserver.execute(self.uuid, boxes)

        log.debug('WorkflowExecutor.execute status=%s', resp['status'])

        if resp['status'] == 'modified':
            raise DeciderWasModifiedError(
                "Error: your workflow has changed - please use versioning"
            )

        if async_:
            return

        if resp['status'] == 'scheduled':
            raise ScheduledBoxException

        if resp['status'] == 'completed':
            workflow.update_properties(
                properties=deserialize(resp['properties'])
            )
            outputs = [deserialize(output) for output in resp['outputs']]
            log.debug('WorkflowExecutor.execute returning %s', outputs)
            return outputs if len(outputs) > 1 else outputs[0]

        raise ZenatonError(
            'InputBox with unknown status at position {}'.format(
                self.position,
            )
        )

    def _build_boxes(self, executables, async_):
        log.debug(
            'WorkflowExecutor._build_boxes(executables=%s, async_=%s)',
            executables,
            async_,
        )

        boxes = []

        for executable in executables:
            if async_:
                self.position.next_async()
            elif len(executables) > 1:
                self.position.next_parallel()
            else:
                self.position.next()
            box = OutputBox(executable, position=self.position)
            boxes.append(box)

        log.debug('boxes = %s)', boxes)
        return boxes
