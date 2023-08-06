"""
Example from the README
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging
import os

from zenaton import Client, Task, Workflow


log = logging.getLogger(__name__)


class Echo(Task):

    def __init__(self, value):
        self.value = value

    def handle(self):
        log.debug('Echo.handle()')
        print(self.value)


class MyWorkflow(Workflow):

    def __init__(self, count):
        self.count = count

    def handle(self):
        log.debug('MyWorkflow.handle() start')
        while self.count > 0:
            self.execute(Echo(self.count))
            self.count -= 1
        log.debug('MyWorkflow.handle() end')


def main():
    logging.basicConfig(level=logging.DEBUG)

    # Create a simple workflow
    workflow = MyWorkflow(count=1)

    # Ask Zenaton to start an instance of this workflow
    client = Client(
        app_id=os.environ['ZENATON_APP_ID'],
        token=os.environ['ZENATON_API_TOKEN'],
        environment=os.environ['ZENATON_APP_ENV'],
        base_url=os.getenv('ZENATON_BASE_URL'),
    )
    instance = client.start(workflow)
    print(instance.id)


if __name__ == '__main__':
    main()
