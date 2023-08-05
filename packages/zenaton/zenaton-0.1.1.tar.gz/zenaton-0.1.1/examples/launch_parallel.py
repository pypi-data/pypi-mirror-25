from __future__ import absolute_import, print_function, unicode_literals

from client import client
from parallel.parallel_workflow import ParallelWorkflow


def main():
    item = {
        'name': 'shirt',
    }
    workflow = ParallelWorkflow(item)

    # Direct synchronous execution
    # workflow.handle()

    # Execution through Zenaton
    instance = client.start(workflow)
    print('Launched workflow instance {}'.format(instance.id))


if __name__ == '__main__':
    main()
