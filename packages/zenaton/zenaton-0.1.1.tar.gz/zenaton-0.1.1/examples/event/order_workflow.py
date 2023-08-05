from __future__ import absolute_import, print_function, unicode_literals

from zenaton import Workflow

from .address_updated_event import AddressUpdatedEvent
from .prepare_order import PrepareOrder
from .send_order import SendOrder


class OrderWorkflow(Workflow):

    def __init__(self, item, address):
        self.item = item
        self.address = address

    def handle(self):
        self.execute(PrepareOrder(self.item))
        self.execute(SendOrder(self.item, self.address))

    def on_event(self, event):
        if isinstance(event, AddressUpdatedEvent):
            self.address = event.address
