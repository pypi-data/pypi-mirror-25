from __future__ import absolute_import, print_function, unicode_literals

from random import randint
from time import sleep

from zenaton import Task


class SendOrder(Task):

    def __init__(self, item, address):
        self.item = item
        self.address = address

    def handle(self):
        print('Sending {} to {}... '.format(self.item, self.address), end='')
        sleep(randint(5, 10))
        print('sent.')
