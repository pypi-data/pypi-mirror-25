from __future__ import absolute_import, print_function, unicode_literals

from zenaton import Event


class AddressUpdatedEvent(Event):

    def __init__(self, address):
        self.address = address
