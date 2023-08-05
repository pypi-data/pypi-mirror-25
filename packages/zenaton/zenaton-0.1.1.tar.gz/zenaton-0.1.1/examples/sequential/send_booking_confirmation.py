from __future__ import absolute_import, print_function, unicode_literals

from zenaton import Task


class SendBookingConfirmation(Task):

    def __init__(self, request):
        self.request = request

    def handle(self):
        print('Sending notification to customer:')
        print('- Customer ID: {}'.format(self.request['customer_id']))
        print('- Request ID: {}'.format(self.request['id']))
        print('- Car ID: {}'.format(self.request['booking_id']))
