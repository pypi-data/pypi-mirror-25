from __future__ import absolute_import, print_function, unicode_literals

import json
import logging
from pprint import pformat
from traceback import format_exception

import requests

from zenaton.serialization import serialize
from zenaton.utils import utc_timestamp
from zenaton.version import __version__


BASE_URL = 'http://localhost:4001'


log = logging.getLogger(__name__)


class MicroserverAPI:

    def __init__(self, base_url=None):
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

    # ===== Initialization =====

    def send_config(self, config):
        return self._post_json(
            url=self.base_url + '/configuration',
            data=config,
        )

    # ===== Jobs =====

    def ask_for_job(self, instance_id, slave_id):
        return self._get_json(
            url=self.base_url + '/jobs/{}'.format(instance_id),
            params={
                'slave_id': slave_id,
            }
        )

    # ===== Decision status =====

    def get_workflow_to_execute(self, uuid):
        log.debug('MicroserverAPI.get_workflow_to_execute(uuid=%s)', uuid)
        return self._post_decision_status(
            uuid,
            {
                'action': 'start',
            }
        )

    def execute(self, uuid, boxes):
        log.debug('MicroserverAPI.execute(uuid=%s, boxes=%s)', uuid, boxes)
        work_items = []
        for box in boxes:
            work_items.append(box.get_work_item())
        return self._post_decision_status(
            uuid,
            {
                'action': 'execute',
                'works': work_items,
            }
        )

    def notify_decision_complete(self, uuid, properties):
        return self._post_decision_status(
            uuid,
            {
                'action': 'terminate',
                'status': 'running',
                'properties': serialize(properties),
            }
        )

    def notify_decision_branch_complete(self, uuid, properties, output):
        return self._post_decision_status(
            uuid,
            {
                'action': 'terminate',
                'status': 'completed',
                'properties': serialize(properties),
                'output': serialize(output),
            }
        )

    def notify_decision_user_error(self, uuid, etype, value, tb):
        return self._notify_decision_error(
            'failed', uuid, etype, value, tb
        )

    def notify_decision_internal_error(self, uuid, etype, value, tb):
        return self._notify_decision_error(
            'zenatonFailed', uuid, etype, value, tb
        )

    def _notify_decision_error(self, reason, uuid, etype, value, tb):
        stacktrace = ''.join(format_exception(etype, value, tb))
        return self._post_decision_status(
            uuid,
            {
                'action': 'terminate',
                'status': reason,
                'error_code': None,
                'error_name': etype.__name__,
                'error_message': str(value),
                'error_stacktrace': stacktrace,
                'failed_at': utc_timestamp(),
            }
        )

    def _post_decision_status(self, uuid, data):
        return self._post_json(
            url=self.base_url + '/decisions/' + str(uuid),
            data=data,
        )

    # ===== Task status =====

    def notify_task_success(self, uuid, hash_, result):
        log.debug(
            'notify_task_success(uuid=%s, hash_=%s, result=%s',
            uuid, hash_, repr(result),
        )
        return self._post_task_status(
            uuid,
            {
                'action': 'terminate',
                'status': 'completed',
                'output': serialize(result),
                'duration': 0,
                'hash': hash_,
            }
        )

    def notify_task_user_error(self, uuid, hash_, etype, value, tb):
        return self._notify_task_error(
            reason='failed',
            uuid=uuid,
            hash_=hash_,
            etype=etype,
            value=value,
            tb=tb,
        )

    def notify_task_internal_error(self, uuid, hash_, etype, value, tb):
        return self._notify_task_error(
            reason='zenatonFailed',
            uuid=uuid,
            hash_=hash_,
            etype=etype,
            value=value,
            tb=tb,
        )

    def _notify_task_error(self, reason, uuid, hash_, etype, value, tb):
        stacktrace = ''.join(format_exception(etype, value, tb))
        return self._post_task_status(
            uuid,
            {
                'action': 'terminate',
                'status': reason,
                'error_code': None,
                'error_name': etype.__name__,
                'error_message': str(value),
                'error_stacktrace': stacktrace,
                'failed_at': utc_timestamp(),
                'hash': hash_,
            }
        )

    def _post_task_status(self, uuid, data):
        return self._post_json(
            url=self.base_url + '/works/' + str(uuid),
            data=data,
        )

    # ==== HTTP communication =====

    def _get_json(self, url, params=None):
        log.debug("GET %s", url)
        return self._request_json('GET', url, params=params)

    def _post_json(self, url, data, params=None):
        log.debug("POST %s", url)
        return self._request_json('POST', url, data=data, params=params)

    def _request_json(self, method, url, data=None, params=None):
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

        log.debug("Request headers: %s", resp.request.headers)
        if resp.request.method != 'GET':
            log.debug("Request body: %s", format_json(resp.request.body))
        log.debug("Response status: %s", resp.status_code)
        log.debug("Response headers: %s", resp.headers)
        log.debug("Response body: %s", format_json(resp.text))

        return resp.json()


def format_json(data):
    try:
        return pformat(json.loads(data), indent=4)
    except:
        return data
