from __future__ import absolute_import, print_function, unicode_literals

from time import sleep

from client import client
from event.order_workflow import OrderWorkflow
from event.address_updated_event import AddressUpdatedEvent


def main():

    workflow = OrderWorkflow(
        item={
            'name': 'shirt',
        },
        address='1600 Pennsylvania Ave NW, Washington, DC 20500, USA',
    )

    # Direct synchronous execution
    # workflow.handle()

    # Execution through Zenaton
    instance = client.start(workflow)
    print('Launched workflow instance {}'.format(instance.id))

    sleep(2)

    instance.send_event(AddressUpdatedEvent(
        address='One Infinite Loop Cupertino, CA 95014',
    ))
    print('Event sent!')


if __name__ == '__main__':
    main()
