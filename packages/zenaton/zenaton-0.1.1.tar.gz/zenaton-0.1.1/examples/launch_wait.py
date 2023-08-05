from __future__ import absolute_import, print_function, unicode_literals

from client import client
from wait.welcome_workflow import WelcomeWorkflow


def main():
    user = {
        'email': 'user@example.com',
    }
    workflow = WelcomeWorkflow(user)

    # Direct synchronous execution
    # workflow.handle()

    # Execution through Zenaton
    instance = client.start(workflow)
    print('Launched workflow instance {}'.format(instance.id))


if __name__ == '__main__':
    main()
