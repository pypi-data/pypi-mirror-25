from __future__ import absolute_import, print_function, unicode_literals

from random import randint
from time import sleep

from zenaton import Task


class BookCar(Task):

    def __init__(self, request):
        self.request = request

    def handle(self):
        print('Booking car for request ID: {}'.format(self.request['id']))
        sleep(randint(1, 3))
        self.request['booking_id'] = 'QSFG34'
        # raise Exception('Error Processing Request')
        print('Car booked: {}'.format(self.request['booking_id']))
        return self.request
