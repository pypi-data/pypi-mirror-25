from __future__ import absolute_import, print_function, unicode_literals

from random import randint
from time import sleep

from zenaton import Task


class SendInvite(Task):

    def __init__(self, name):
        self.name = name

    def handle(self):
        print('Sending invite to: {}'.format(self.name))
        sleep(randint(1, 3))
        print('Invite succesfully sent to: {}'.format(self.name))
