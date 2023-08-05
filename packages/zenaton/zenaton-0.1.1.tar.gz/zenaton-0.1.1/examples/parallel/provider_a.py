from __future__ import absolute_import, print_function, unicode_literals

from random import randint
from time import sleep

from zenaton import Task


class GetPrice(Task):

    def handle(self):
        # Fake API request to get price from provider A
        print("Contacting provider A to get the price...")
        sleep(randint(5, 10))
        price = randint(80, 100)
        print('Price from provider A is: {}'.format(price))
        return price


class Order(Task):

    def handle(self):
        print('Ordering "{}" from provider A'.format(self.item['name']))
