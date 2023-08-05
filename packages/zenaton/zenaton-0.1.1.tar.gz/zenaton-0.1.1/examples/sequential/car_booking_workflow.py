from __future__ import absolute_import, print_function, unicode_literals

from zenaton import Workflow

from .book_car import BookCar
from .send_booking_confirmation import SendBookingConfirmation


class CarBookingWorkflow(Workflow):

    def __init__(self, request):
        self.request = request

    def handle(self):
        request = self.execute(BookCar(self.request))
        self.execute(SendBookingConfirmation(request))
