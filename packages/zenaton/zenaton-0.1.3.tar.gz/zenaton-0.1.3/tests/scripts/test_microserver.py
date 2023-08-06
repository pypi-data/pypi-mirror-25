from __future__ import absolute_import, print_function, unicode_literals

from textwrap import dedent
import sys

import pytest

from zenaton.testing.compat import MagicMock, patch


@pytest.fixture
def microserver():
    from zenaton.microserver import MicroserverAPI
    microserver = MicroserverAPI()
    microserver.session = MagicMock()
    return microserver


class TestMicroserverBaseURL:

    def test_default_base_url(self):
        from zenaton.microserver import MicroserverAPI
        microserver = MicroserverAPI()
        assert microserver.base_url == 'http://localhost:4001'

    def test_explicit_none_base_url(self):
        from zenaton.microserver import MicroserverAPI
        microserver = MicroserverAPI(base_url=None)
        assert microserver.base_url == 'http://localhost:4001'

    def test_override_base_url(self):
        from zenaton.microserver import MicroserverAPI
        microserver = MicroserverAPI(base_url='http://localhost:4002')
        assert microserver.base_url == 'http://localhost:4002'


class TestMicroServerSendConfig:

    def test_send_config(self, microserver):
        microserver._post_json = MagicMock()
        microserver._post_json.return_value = {
            'foo': 'bar',
        }

        res = microserver.send_config({'a': 1})

        microserver._post_json.assert_called_once_with(
            url='http://localhost:4001/configuration',
            data={'a': 1},
        )
        assert res == {
            'foo': 'bar',
        }


class TestMicroServerAskForJob:

    def test_ask_for_job(self, microserver):
        microserver._get_json = MagicMock()
        microserver._get_json.return_value = {
            'action': 'DecisionScheduled',
        }

        res = microserver.ask_for_job(
            instance_id='A21CA381-6F97-400B-B10C-3AAD198F33A9',
            slave_id='C5EDBCD0-DEBE-4C3C-816B-883DC4306B7B',
        )

        microserver._get_json.assert_called_once_with(
            url='http://localhost:4001/jobs/A21CA381-6F97-400B-B10C-3AAD198F33A9',
            params={
                'slave_id': 'C5EDBCD0-DEBE-4C3C-816B-883DC4306B7B',
            }
        )
        assert res == {
            'action': 'DecisionScheduled',
        }


class TestMicroserverDecisionStatus:

    def test_get_workflow_to_execute(self, microserver):
        microserver._post_decision_status = MagicMock()
        microserver._post_decision_status.return_value = {
            'foo': 'bar',
        }

        res = microserver.get_workflow_to_execute(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
        )

        microserver._post_decision_status.assert_called_once_with(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            {
                'action': 'start',
            }
        )
        assert res == {
            'foo': 'bar',
        }

    def test_execute(self, microserver):
        microserver._post_decision_status = MagicMock()
        microserver._post_decision_status.return_value = {
            'foo': 'bar',
        }

        res = microserver.execute(
            uuid='7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            boxes=[]
        )

        microserver._post_decision_status.assert_called_once_with(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            {
                'action': 'execute',
                'works': []
            }
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_decision_complete(self, microserver):
        microserver._post_decision_status = MagicMock()
        microserver._post_decision_status.return_value = {
            'foo': 'bar',
        }

        res = microserver.notify_decision_complete(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            {'a': 1},
        )

        microserver._post_decision_status.assert_called_once_with(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            {
                'action': 'terminate',
                'status': 'running',
                'properties': '{"a": 1}',
            }
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_decision_branch_complete(self, microserver):
        microserver._post_decision_status = MagicMock()
        microserver._post_decision_status.return_value = {
            'foo': 'bar',
        }

        res = microserver.notify_decision_branch_complete(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            {'a': 1},
            42,
        )

        microserver._post_decision_status.assert_called_once_with(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            {
                'action': 'terminate',
                'status': 'completed',
                'properties': '{"a": 1}',
                'output': '42',
            }
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_decision_user_error(self, microserver):
        try:
            raise RuntimeError('foo')
        except:
            etype, value, tb = sys.exc_info()

        microserver._notify_decision_error = MagicMock()
        microserver._notify_decision_error.return_value = {
            'foo': 'bar',
        }

        res = microserver.notify_decision_user_error(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            etype,
            value,
            tb,
        )

        microserver._notify_decision_error.assert_called_once_with(
            'failed',
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            etype,
            value,
            tb,
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_decision_internal_error(self, microserver):
        from zenaton.errors import ZenatonError

        try:
            raise ZenatonError('foo')
        except ZenatonError:
            etype, value, tb = sys.exc_info()

        microserver._notify_decision_error = MagicMock()
        microserver._notify_decision_error.return_value = {
            'foo': 'bar',
        }

        res = microserver.notify_decision_internal_error(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            etype,
            value,
            tb,
        )

        microserver._notify_decision_error.assert_called_once_with(
            'zenatonFailed',
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            etype,
            value,
            tb,
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_decision_error(self, microserver):
        try:
            raise RuntimeError('foo')
        except:
            etype, value, tb = sys.exc_info()

        dummy_stacktrace = dedent('''\
            Traceback (most recent call last):
              File "/path/to/module.py", line 42, in some_function
                raise RuntimeError(\'foo\')
            zenaton.errors.RuntimeError: foo
        ''')

        microserver._post_decision_status = MagicMock()
        microserver._post_decision_status.return_value = {
            'foo': 'bar',
        }

        with patch('zenaton.microserver.format_exception') as mock_fmt_exc:
            mock_fmt_exc.return_value = dummy_stacktrace

            with patch('zenaton.microserver.utc_timestamp') as mock_timestamp:
                mock_timestamp.return_value = 1499358596

                res = microserver._notify_decision_error(
                    'reason',
                    '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
                    etype,
                    value,
                    tb,
                )

        microserver._post_decision_status.assert_called_once_with(
            '7997851A-E0D6-4E45-A511-AE0159D4FDAB',
            {
                'action': 'terminate',
                'status': 'reason',
                'error_code': None,
                'error_name': 'RuntimeError',
                'error_message': 'foo',
                'error_stacktrace': dummy_stacktrace,
                'failed_at': 1499358596,
            }
        )
        assert res == {
            'foo': 'bar',
        }

    def test_post_decision_status(self, microserver):
        microserver._post_json = MagicMock()
        microserver._post_json.return_value = {
            'foo': 'bar',
        }

        res = microserver._post_decision_status('UUID', {'a': 1})

        microserver._post_json.assert_called_once_with(
            url='http://localhost:4001/decisions/UUID',
            data={'a': 1},
        )
        assert res == {
            'foo': 'bar',
        }


class TestMicroserverTaskStatus:

    def test_notify_task_success(self, microserver):
        microserver._post_task_status = MagicMock()
        microserver._post_task_status.return_value = {
            'foo': 'bar',
        }

        res = microserver.notify_task_success(
            uuid='197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
            hash_='1a08b1b6edbe8009ecf93969079efb92',
            result=42,
        )

        microserver._post_task_status.assert_called_once_with(
            '197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
            {
                'action': 'terminate',
                'status': 'completed',
                'output': '42',
                'duration': 0,
                'hash': '1a08b1b6edbe8009ecf93969079efb92',
            }
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_task_user_error(self, microserver):
        try:
            raise RuntimeError('foo')
        except:
            etype, value, tb = sys.exc_info()

        microserver._notify_task_error = MagicMock()
        microserver._notify_task_error.return_value = {
            'foo': 'bar',
        }

        res = microserver.notify_task_user_error(
            '197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
            '1a08b1b6edbe8009ecf93969079efb92',
            etype,
            value,
            tb,
        )

        microserver._notify_task_error.assert_called_once_with(
            reason='failed',
            uuid='197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
            hash_='1a08b1b6edbe8009ecf93969079efb92',
            etype=etype,
            value=value,
            tb=tb,
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_task_internal_error(self, microserver):
        from zenaton.errors import ZenatonError

        try:
            raise ZenatonError('foo')
        except ZenatonError:
            etype, value, tb = sys.exc_info()

        microserver._notify_task_error = MagicMock()
        microserver._notify_task_error.return_value = {
            'foo': 'bar',
        }

        res = microserver.notify_task_internal_error(
            '197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
            '1a08b1b6edbe8009ecf93969079efb92',
            etype,
            value,
            tb,
        )

        microserver._notify_task_error.assert_called_once_with(
            reason='zenatonFailed',
            uuid='197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
            hash_='1a08b1b6edbe8009ecf93969079efb92',
            etype=etype,
            value=value,
            tb=tb,
        )
        assert res == {
            'foo': 'bar',
        }

    def test_notify_task_error(self, microserver):
        try:
            raise RuntimeError('foo')
        except:
            etype, value, tb = sys.exc_info()

        dummy_stacktrace = dedent('''\
            Traceback (most recent call last):
              File "/path/to/module.py", line 42, in some_function
                raise RuntimeError(\'foo\')
            zenaton.errors.RuntimeError: foo
        ''')

        microserver._post_task_status = MagicMock()
        microserver._post_task_status.return_value = {
            'foo': 'bar',
        }

        with patch('zenaton.microserver.format_exception') as mock_fmt_exc:
            mock_fmt_exc.return_value = dummy_stacktrace

            with patch('zenaton.microserver.utc_timestamp') as mock_timestamp:
                mock_timestamp.return_value = 1499358596

                res = microserver._notify_task_error(
                    'reason',
                    '197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
                    '1a08b1b6edbe8009ecf93969079efb92',
                    etype,
                    value,
                    tb,
                )

        microserver._post_task_status.assert_called_once_with(
            '197BAA87-9AF3-4B91-AAF9-A2DC7D65CB2E',
            {
                'action': 'terminate',
                'status': 'reason',
                'error_code': None,
                'error_name': 'RuntimeError',
                'error_message': 'foo',
                'error_stacktrace': dummy_stacktrace,
                'failed_at': 1499358596,
                'hash': '1a08b1b6edbe8009ecf93969079efb92',
            }
        )
        assert res == {
            'foo': 'bar',
        }

    def test_post_task_status(self, microserver):
        microserver._post_json = MagicMock()
        microserver._post_json.return_value = {
            'foo': 'bar',
        }

        res = microserver._post_task_status('UUID', {'a': 1})

        microserver._post_json.assert_called_once_with(
            url='http://localhost:4001/works/UUID',
            data={'a': 1},
        )
        assert res == {
            'foo': 'bar',
        }


class TestMicroserverHTTP:

    def test_get_json(self, microserver):
        microserver._request_json = MagicMock()
        microserver._request_json.return_value = {'foo': 'bar'}

        microserver._get_json(
            url='http://localhost:4001/foo',
            params={'a': 1}
        )

        microserver._request_json.assert_called_once_with(
            'GET',
            'http://localhost:4001/foo',
            params={'a': 1},
        )

    def test_post_json(self, microserver):
        microserver._request_json = MagicMock()
        microserver._request_json.return_value = {'foo': 'bar'}

        microserver._post_json(
            url='http://localhost:4001/foo',
            data={'a': 1},
        )

        microserver._request_json.assert_called_once_with(
            'POST',
            'http://localhost:4001/foo',
            data={"a": 1},
            params=None,
        )

    def test_request_json(self, microserver):
        from zenaton.version import __version__

        microserver._request_json(
            'POST',
            'https://localhost:8080/api',
            data={'data': 1},
            params={'param': 1},
        )
        microserver.session.request.assert_called_once_with(
            'POST',
            'https://localhost:8080/api',
            params={
                'param': 1,
            },
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'zenaton-python/{}'.format(__version__),
            },
            data='{"data": 1}',
        )
        resp = microserver.session.request.return_value
        resp.json.assert_called_once_with()
