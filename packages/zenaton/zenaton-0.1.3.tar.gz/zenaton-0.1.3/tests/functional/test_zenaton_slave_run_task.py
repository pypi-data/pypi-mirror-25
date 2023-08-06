"""
End-to-end test with fake remote and microserver APIs
"""
from __future__ import absolute_import, print_function, unicode_literals

import json

import responses

from zenaton.testing.compat import patch


@patch('sys.exit')
def test_zenaton_slave_run_task(mock_exit, capsys):
    from zenaton.scripts.slave import main

    with responses.RequestsMock() as rsps:

        # Get a job to do => run a task
        rsps.add(
            responses.GET,
            'http://localhost:4001/jobs/AD489DB1',
            status=200,
            json={
                'action': 'TaskScheduled',
                'uuid': '547BDD74-CE71-4762-96F6-94F5DC3CFD68',
                'name': 'zenaton.testing.examples.readme:Echo',
                'input': '{"value": "Hello world"}',
                'hash': '8749975af5306c045c5c0af268a29482',
            }
        )

        # Notify task completion => OK
        rsps.add(
            responses.POST,
            'http://localhost:4001/works/547BDD74-CE71-4762-96F6-94F5DC3CFD68',
            status=200,
            body='{}',
            content_type='application/json',
         )

        main(['AD489DB1', '8CF89842'])

        assert len(rsps.calls) == 2

        assert rsps.calls[0].request.url == 'http://localhost:4001/jobs/AD489DB1?slave_id=8CF89842'

        assert rsps.calls[1].request.url == 'http://localhost:4001/works/547BDD74-CE71-4762-96F6-94F5DC3CFD68'
        assert json.loads(rsps.calls[1].request.body) == {
            "action": "terminate",
            "status": "completed",
            "output": "null",
            "duration": 0,
            "hash": '8749975af5306c045c5c0af268a29482',
        }

    # Check that the task printed its argument
    out, err = capsys.readouterr()
    assert out == 'Hello world\n'
    assert err == ''

    mock_exit.assert_called_once_with(0)
