from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
from collections import OrderedDict

import requests

from zenaton.config import PROGRAMMING_LANGUAGE
from zenaton.errors import (
    APIError,
    UnauthenticatedError,
)
from zenaton.version import __version__


BASE_URL = 'https://zenaton.com/api'


log = logging.getLogger(__name__)


class API:
    """
    Zenaton.io API client.

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
        self.app_id = app_id
        self.token = token
        self.environment = environment
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

    def start_workflow(self, name, data, custom_id=None):
        return self._post_json(
            self.base_url + '/instances',
            data={
                'name': name,
                'data': data,
                'custom_id': custom_id,
                'programming_language': PROGRAMMING_LANGUAGE,
            },
        )

    def get_workflow_instance(self, id, name):
        # Feels like a workflow instance's ID should be unique
        # within an (app_id, app_env) context. Why do we need
        # to send the name too?
        return self._get_json(
            self.base_url + '/instances/' + id,
            params=OrderedDict([
                ('name', name),
                ('programming_language', PROGRAMMING_LANGUAGE),
            ])
        )

    def update_workflow_instance(self, id, name, state):
        return self._put_json(
            self.base_url + '/instances/' + id,
            data={
                'name': name,
                'programming_language': PROGRAMMING_LANGUAGE,
                'state': state,
            }
        )

    def send_event(self, custom_id, workflow_name, event_name, event_input):
        return self._post_json(
            self.base_url + '/events',
            data={
                'custom_id': custom_id,
                'event_input': event_input,
                'event_name': event_name,
                'name': workflow_name,
                'programming_language': PROGRAMMING_LANGUAGE,
            }
        )

    def _get_json(self, url, params=None):
        return self._request_json('GET', url, params=params)

    def _post_json(self, url, data, params=None):
        return self._request_json('POST', url, data=data, params=params)

    def _put_json(self, url, data, params=None):
        return self._request_json('PUT', url, data=data, params=params)

    def _request_json(self, method, url, data=None, params=None):
        if params is None:
            params = OrderedDict()
        params.update(OrderedDict([
            ('api_token', self.token),
            ('app_env', self.environment),
            ('app_id', self.app_id),
        ]))
        resp = self.session.request(
            method,
            url,
            params=params,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'zenaton-python/{}'.format(__version__),
            },
            data=json.dumps(data),
        )

        if resp.status_code == 401:
            raise UnauthenticatedError("Check your API token")

        log.debug("Request headers: %s", resp.request.headers)
        log.debug("Request body: %s", resp.request.body)
        log.debug("Response status: %s", resp.status_code)
        log.debug("Response headers: %s", resp.headers)
        log.debug("Response body: %s", resp.text)

        json_data = resp.json()

        if set(json_data.keys()) == {'error'}:
            raise APIError(json_data['error'])

        return json_data
