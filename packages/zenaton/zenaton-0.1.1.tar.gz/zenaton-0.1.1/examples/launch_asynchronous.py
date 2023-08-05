from __future__ import absolute_import, print_function, unicode_literals

from client import client
from asynchronous.send_invites_workflow import SendInvitesWorkflow


def main():

    notifications = ['Gilles', 'Julien', 'Oussama', 'Alice', 'Charlotte', 'Balthazar', 'Annabelle', 'Louis']
    workflow = SendInvitesWorkflow(notifications)

    # Direct synchronous execution
    # workflow.handle()

    # Execution through Zenaton
    instance = client.start(workflow)
    print('Launched workflow instance {}'.format(instance.id))


if __name__ == '__main__':
    main()
