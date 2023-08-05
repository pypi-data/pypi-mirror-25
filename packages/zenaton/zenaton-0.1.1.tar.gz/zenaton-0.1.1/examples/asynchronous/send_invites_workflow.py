from __future__ import absolute_import, print_function, unicode_literals

from zenaton import Workflow

from .send_invite import SendInvite


class SendInvitesWorkflow(Workflow):

    def __init__(self, invites):
        self.invites = invites

    def handle(self):
        for invite in self.invites:
            self.execute_async(SendInvite(invite))
