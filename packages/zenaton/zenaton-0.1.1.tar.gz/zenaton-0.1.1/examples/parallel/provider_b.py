from __future__ import absolute_import, print_function, unicode_literals

from random import randint
from time import sleep

from zenaton import Task


class GetPrice(Task):

    def handle(self):
        # Fake API request to get price from provider B
        print("Contacting provider B to get the price...")
        # raise Exception('Cannot reach provider B')
        sleep(randint(5, 10))
        price = randint(80, 100)
        print('Price from provider B is: {}'.format(price))
        return price


class Order(Task):

    def handle(self):
        print('Ordering "{}" from provider B'.format(self.item['name']))
