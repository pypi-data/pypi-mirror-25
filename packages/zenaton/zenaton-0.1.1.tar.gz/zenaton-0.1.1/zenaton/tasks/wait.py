from __future__ import absolute_import, print_function, unicode_literals

from time import sleep, time


class Wait:

    def __init__(self, seconds=0, event=None):
        self.seconds = seconds
        self.timeout_timestamp = int(time() + self.seconds)
        self.event = event

    def handle(self):
        sleep(self.seconds)

    def get_event(self):
        return self.event

    def get_timeout_timestamp(self):
        return self.timeout_timestamp
