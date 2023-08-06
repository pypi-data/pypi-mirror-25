from __future__ import absolute_import, print_function, unicode_literals
from datetime import datetime, timedelta
from time import sleep


class Wait:

    def __init__(self, seconds=0, event=None):
        self.seconds = seconds
        self.timeout_timestamp = int((datetime.utcnow() + timedelta(seconds=self.seconds) - datetime(1970, 1, 1)).total_seconds())
        self.event = event

    def handle(self):
        sleep(self.seconds)

    def get_event(self):
        return self.event

    def get_timeout_timestamp(self):
        return self.timeout_timestamp
