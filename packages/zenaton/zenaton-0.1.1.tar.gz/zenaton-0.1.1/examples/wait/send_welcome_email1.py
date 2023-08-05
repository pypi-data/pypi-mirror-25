from __future__ import absolute_import, print_function, unicode_literals

from random import randint
from time import sleep

from zenaton import Task


class SendWelcomeEmail1(Task):

    def __init__(self, email):
        self.email = email

    def handle(self):
        print('Sending welcome email #1 to: {}'.format(self.email))
        sleep(randint(1, 3))
        print('Email #1 sent')
