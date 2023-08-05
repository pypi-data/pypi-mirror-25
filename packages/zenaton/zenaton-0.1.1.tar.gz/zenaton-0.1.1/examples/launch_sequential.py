from __future__ import absolute_import, print_function, unicode_literals

from client import client
from sequential.car_booking_workflow import CarBookingWorkflow


def main():
    request = {
        'id': 12345,
        'customer_id': '2DER45G',
        'transport': 'car',
    }
    workflow = CarBookingWorkflow(request)

    # Direct synchronous execution
    # workflow.handle()

    # Execution through Zenaton
    instance = client.start(workflow)
    print('Launched workflow instance {}'.format(instance.id))


if __name__ == '__main__':
    main()
