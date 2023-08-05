from __future__ import absolute_import, print_function, unicode_literals

from zenaton import Workflow, Wait

from .send_welcome_email1 import SendWelcomeEmail1
from .send_welcome_email2 import SendWelcomeEmail2
from .send_welcome_email3 import SendWelcomeEmail3


class WelcomeWorkflow(Workflow):

    def __init__(self, user):
        self.user = user

    def handle(self):
        self.execute(SendWelcomeEmail1(self.user['email']))
        self.execute(Wait(seconds=4))
        self.execute(SendWelcomeEmail2(self.user['email']))
        self.execute(Wait(seconds=4))
        self.execute(SendWelcomeEmail3(self.user['email']))
