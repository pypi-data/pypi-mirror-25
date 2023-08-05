from __future__ import absolute_import, print_function, unicode_literals

import logging

from six import binary_type, text_type

from zenaton.api import API
from zenaton.errors import ZenatonError
from zenaton.proxy import WorkflowProxy
from zenaton.serialization import (
    get_class_path,
    get_properties,
    serialize,
)
from zenaton.utils import has_method


MAX_ID_BYTES = 191


log = logging.getLogger(__name__)


class Client:
    """
    Zenaton API client.

    Arguments:
        app_id (str): The ID of the app you created on https://zenaton.com/.
            (Note that this is not the name you chose for your app
            (e.g. `test`), but the unique ID given by Zenaton, which
            looks like ``WMBAVMXSHQ``.
        token (str): An API access token that you created on
            https://zenaton.com/.
        environment (str): An arbitrary string that you can use to
            differentiate between environments, such as `dev`, `staging`
            or `production`.
        base_url (str, optional): Used to override the base URL of the
            Zenaton API server.
    """

    def __init__(self, app_id, token, environment, base_url=None):
        self.api = API(app_id, token, environment, base_url)

    def start(self, workflow):
        """
        Start execution of a new workflow instance.
        """
        if not has_method(workflow, 'handle'):
            raise ZenatonError('Workflow must implement the handle() method')

        name = get_class_path(workflow.__class__)

        response_data = self.api.start_workflow(
            name=name,
            data=serialize(get_properties(workflow)),
            custom_id=self._get_custom_id(workflow),
        )

        log.debug("started workflow: %s", response_data)

        return WorkflowProxy(
            api=self.api,
            id=response_data['custom_id'],
            name=name,
        )

    def _get_custom_id(self, workflow):
        if hasattr(workflow, 'get_id') and callable(workflow.get_id):
            custom_id = workflow.get_id()
            if custom_id is None:
                return None
            if isinstance(custom_id, binary_type):
                custom_id = custom_id.decode()
            if not isinstance(custom_id, text_type):
                raise ZenatonError('Workflow ID must be a string')
            if len(custom_id.encode('utf-8')) > MAX_ID_BYTES:
                raise ZenatonError('Workflow ID is too long')
            log.info(custom_id)
            return custom_id
        return None
