from __future__ import absolute_import, print_function, unicode_literals

from random import randint
from time import sleep

from zenaton import Task


class PrepareOrder(Task):

    def __init__(self, item):
        self.item = item

    def handle(self):
        print('Preparing order for item {}... '.format(self.item))
        sleep(randint(5, 10))
        print('Order prepared')
