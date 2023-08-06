from __future__ import absolute_import, print_function, unicode_literals

from collections import OrderedDict
import json

import pytest

from zenaton.event import Event
from zenaton.testing.compat import MagicMock


@pytest.fixture
def api():
    return MagicMock()


@pytest.fixture
def workflow(api):
    from zenaton.proxy import WorkflowProxy
    return WorkflowProxy(api, 'ID', 'NAME')


class DummyEvent(Event):

    def __init__(self, a):
        self.a = a


def test_workflow_proxy_send_event(api, workflow):
    event = DummyEvent(42)

    workflow.send_event(event)

    api.send_event.assert_called_once_with(
        custom_id='ID',
        workflow_name='NAME',
        event_name='test_proxy:DummyEvent',
        event_input=json.dumps(OrderedDict([
            ("name", "test_proxy:DummyEvent"),
            ("properties", {"a": 42}),
        ])),
    )


class TestProxySignals:

    def test_workflow_proxy_kill(self, workflow):
        from zenaton.proxy import Signal
        workflow._send_signal = MagicMock()
        workflow.kill()
        workflow._send_signal.assert_called_once_with(Signal.KILL)

    def test_workflow_proxy_pause(self, workflow):
        from zenaton.proxy import Signal
        workflow._send_signal = MagicMock()
        workflow.pause()
        workflow._send_signal.assert_called_once_with(Signal.PAUSE)

    def test_workflow_proxy_resume(self, workflow):
        from zenaton.proxy import Signal
        workflow._send_signal = MagicMock()
        workflow.resume()
        workflow._send_signal.assert_called_once_with(Signal.RUN)

    def test_workflow_proxy_send_signal(self, api, workflow):
        workflow._send_signal('SIGNAL')
        api.update_workflow_instance.assert_called_once_with(
            'ID',
            'NAME',
            'SIGNAL',
        )


# def test_workflow_proxy_get_properties(api, workflow):
#     api.get_workflow_instance.return_value = {
#         'instance': {
#             'a': 1,
#             'b': 2,
#         }
#     }

#     properties = workflow.get_properties()

#     api.get_workflow_instance.assert_called_once_with('ID', 'NAME')
#     assert properties == {
#         'a': 1,
#         'b': 2,
#     }
