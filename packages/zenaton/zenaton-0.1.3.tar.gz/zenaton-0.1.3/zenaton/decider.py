from __future__ import absolute_import, print_function, unicode_literals

from collections import namedtuple
from contextlib import contextmanager
import logging
import sys

from zenaton.errors import ZenatonError
from zenaton.serialization import (
    deserialize,
    get_properties,
)
from zenaton.workflow import Workflow
from zenaton.workflow_executor import (
    ScheduledBoxException,
    WorkflowExecutor,
)


log = logging.getLogger(__name__)


Branch = namedtuple('Branch', ['name', 'properties', 'event'])


class Decider:

    def __init__(self, uuid, microserver):
        self.uuid = uuid
        self.microserver = microserver

    def launch(self):
        log.debug('Decider.launch()')
        while True:
            branch = self.get_next_workflow_branch()
            if branch is None:
                break
            with self.handle_errors():
                self.process_workflow_branch(branch)

    def get_next_workflow_branch(self):
        log.debug('Decider.get_next_workflow_branch()')
        data = self.microserver.get_workflow_to_execute(self.uuid)
        log.debug('Decider.get_next_workflow_branch() => %s', data)
        if data == []:
            return None
        return Branch(
            name=data['name'],
            event=deserialize(data['event']) if data['event'] else None,
            properties=deserialize(data['properties']),
        )

    @contextmanager
    def handle_errors(self):
        try:
            yield
        except ZenatonError:
            etype, value, traceback = sys.exc_info()
            self.microserver.notify_decision_internal_error(
                self.uuid, etype, value, traceback
            )
            raise
        except Exception:
            etype, value, traceback = sys.exc_info()
            self.microserver.notify_decision_user_error(
                self.uuid, etype, value, traceback
            )
            raise

    def process_workflow_branch(self, branch):
        log.debug('Decider.process_workflow_branch(%s)', branch)
        workflow = self.create_workflow(
            name=branch.name,
            properties=branch.properties,
        )
        try:
            output = self.run_handler(workflow, branch.event)
        except ScheduledBoxException:
            self.microserver.notify_decision_complete(
                uuid=self.uuid,
                properties=get_properties(workflow),
            )
            return
        self.microserver.notify_decision_branch_complete(
            uuid=self.uuid,
            properties=get_properties(workflow),
            output=output,
        )

    def create_workflow(self, name, properties):
        log.debug(
            'Decider.create_workflow(name=%s, properties=%s)',
            name,
            properties,
        )
        workflow = Workflow.create(name, properties)
        workflow.__zenaton_executor__ = WorkflowExecutor(
            uuid=self.uuid,
            microserver=self.microserver,
        )
        return workflow

    def run_handler(self, workflow, event):
        log.debug(
            'Decider.run_handler(workflow=%s, event=%s)',
            workflow,
            event,
        )
        if event is not None and hasattr(workflow, 'on_event'):
            return workflow.on_event(event)
        return workflow.handle()
