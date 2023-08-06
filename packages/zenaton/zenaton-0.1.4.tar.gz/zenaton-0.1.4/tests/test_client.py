from __future__ import absolute_import, print_function, unicode_literals

import pytest

from zenaton.errors import ZenatonError
from zenaton.testing.compat import MagicMock
from zenaton.workflow import Workflow


@pytest.fixture
def client():
    from zenaton.client import Client

    client = Client(
        app_id='MY_APP_ID',
        token='MY_TOKEN',
        environment='TEST',
    )
    client.api = MagicMock()
    return client


class WF(Workflow):

    def __init__(self, id=None):
        self._id = id
        self.a = 1

    def get_id(self):
        return self._id


class TestClientStartWorkflow:

    def test_workflow_has_no_custom_id(self, client):
        client.api.start_workflow.return_value = {
            'msg': 'test_client:WF launched',
            'custom_id': 'c8rbrivw188ws4s',
            'instance_id':'c8rbrivw188ws4s-bipmzra7qfsckcc',
        }

        instance = client.start(WF())

        client.api.start_workflow.assert_called_once_with(
            name='test_client:WF',
            data='{"a": 1}',
            custom_id=None,
        )
        assert instance.id == 'c8rbrivw188ws4s'

    def test_workflow_has_a_string_custom_id(self, client):
        client.api.start_workflow.return_value = {
            'msg': 'test_client:WF launched',
            'custom_id': '55gffs7c2ykg804w',
            'instance_id': '55gffs7c2ykg804w-bipmzra7qfsckcc',
        }

        instance = client.start(WF(id='55gffs7c2ykg804w'))

        client.api.start_workflow.assert_called_once_with(
            name='test_client:WF',
            data='{"a": 1}',
            custom_id='55gffs7c2ykg804w',
        )
        assert instance.id == '55gffs7c2ykg804w'

    def test_workflow_has_a_binary_custom_id(self, client):
        client.api.start_workflow.return_value = {
            'msg': 'test_client:WF launched',
            'custom_id': '55gffs7c2ykg804w',
            'instance_id': '55gffs7c2ykg804w-bipmzra7qfsckcc',
        }

        instance = client.start(WF(id=b'custom id'))

        client.api.start_workflow.assert_called_once_with(
            name='test_client:WF',
            data='{"a": 1}',
            custom_id='custom id',
        )
        assert instance.id == '55gffs7c2ykg804w'

    def test_error_workflow_custom_id_is_not_a_string(self, client):
        workflow = WF(id=42)

        with pytest.raises(ZenatonError) as exc:
            instance = client.start(workflow)

        assert str(exc.value) == 'Workflow ID must be a string'

    def test_error_workflow_custom_id_is_too_long(self, client):
        workflow = WF(id=(b'a' * 192))

        with pytest.raises(ZenatonError) as exc:
            instance = client.start(workflow)

        assert str(exc.value) == 'Workflow ID is too long'

    def test_error_not_a_workflow(self, client):
        class NotAWorkflow:
            pass

        with pytest.raises(ZenatonError):
            client.start(NotAWorkflow())
