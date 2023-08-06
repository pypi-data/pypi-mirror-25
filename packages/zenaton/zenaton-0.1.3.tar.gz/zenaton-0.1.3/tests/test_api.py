from __future__ import absolute_import, print_function, unicode_literals

import pytest

from zenaton.testing.compat import MagicMock
from zenaton.version import __version__


@pytest.fixture
def api():
    from zenaton.api import API
    api = API(app_id='APP_ID', token='API_TOKEN', environment='APP_ENV')
    api.session = MagicMock()
    return api


class TestAPIBaseURL:

    def test_api_base_url_default(self, api):
        assert api.base_url == 'https://zenaton.com/api'

    def test_api_base_url_override(self):
        from zenaton.api import API
        api = API(
            app_id='APP_ID',
            token='API_TOKEN',
            environment='APP_ENV',
            base_url='https://localhost:8080/api',
        )
        assert api.base_url == 'https://localhost:8080/api'


class TestAPIWorkflow:

    def test_api_start_workflow(self, api):
        api._post_json = MagicMock()

        res = api.start_workflow('NAME', {'foo': 'bar'}, 'CUSTOM_ID')

        api._post_json.assert_called_once_with(
            'https://zenaton.com/api/instances',
            data={
                'name': 'NAME',
                'data': {'foo': 'bar'},
                'custom_id': 'CUSTOM_ID',
                'programming_language': 'Python',
            }
        )

    def test_api_update_workflow_instance(self, api):
        api._put_json = MagicMock()

        res = api.update_workflow_instance('ID', 'NAME', 'STATE')

        api._put_json.assert_called_once_with(
            'https://zenaton.com/api/instances/ID',
            data={
                'name': 'NAME',
                'programming_language': 'Python',
                'state': 'STATE',
            }
        )

    def test_api_get_workflow_instance(self, api):
        api._get_json = MagicMock()

        res = api.get_workflow_instance('ID', 'NAME')

        api._get_json.assert_called_once_with(
            'https://zenaton.com/api/instances/ID',
            params={
                'name': 'NAME',
                'programming_language': 'Python',
            }
        )


class TestAPISendEvent:

    def test_api_send_event(self, api):
        api._post_json = MagicMock()
        res = api.send_event('ID', 'WORKFLOW', 'EVENT', {'foo': 'bar'})
        api._post_json.assert_called_once_with(
            'https://zenaton.com/api/events',
            data={
                'custom_id': 'ID',
                'event_input': {'foo': 'bar'},
                'event_name': 'EVENT',
                'name': 'WORKFLOW',
                'programming_language': 'Python',
            }
        )


class TestAPIHTTP:

    def test_get_json(self, api):
        api._request_json = MagicMock()
        api._request_json.return_value = {'foo': 'bar'}

        res = api._get_json('URL', params={'a': 1})

        api._request_json.assert_called_once_with(
            'GET',
            'URL',
            params={'a': 1},
        )
        assert res == {'foo': 'bar'}

    def test_post_json(self, api):
        api._request_json = MagicMock()
        api._request_json.return_value = {'foo': 'bar'}

        res = api._post_json('URL', {'a': 1})

        api._request_json.assert_called_once_with(
            'POST',
            'URL',
            data={'a': 1},
            params=None,
        )
        assert res == {'foo': 'bar'}

    def test_put_json(self, api):
        api._request_json = MagicMock()
        api._request_json.return_value = {'foo': 'bar'}

        res = api._put_json('URL', {'a': 1})

        api._request_json.assert_called_once_with(
            'PUT',
            'URL',
            data={'a': 1},
            params=None,
        )
        assert res == {'foo': 'bar'}

    def test_request_json(self, api):
        api._request_json(
            'POST',
            'https://localhost:8080/api',
            data={'data': 1},
            params={'param': 1},
        )
        api.session.request.assert_called_once_with(
            'POST',
            'https://localhost:8080/api',
            params={
                'param': 1,
                'app_env': 'APP_ENV',
                'app_id': 'APP_ID',
                'api_token': 'API_TOKEN',
            },
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'zenaton-python/{}'.format(__version__),
            },
            data='{"data": 1}',
        )
        api.session.request.return_value.json.assert_called_once_with()

    def test_request_json_unauthenticated(self, api):
        from zenaton.api import UnauthenticatedError

        api.session.request.return_value.status_code = 401

        with pytest.raises(UnauthenticatedError):
            api._request_json('POST', 'https://localhost:8080/api', data={})

    def test_request_json_error_payload(self, api):
        from zenaton.api import APIError

        api.session.request.return_value.json.return_value = {
            'error': 'some error message',
        }

        with pytest.raises(APIError) as exc:
            api._request_json('POST', 'https://localhost:8080/api', data={})

        assert str(exc.value) == 'some error message'
