"""
End-to-end test with fake remote and microserver APIs
"""
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging

import responses

from zenaton.testing.compat import patch


log = logging.getLogger(__name__)


@patch('sys.exit')
def test_zenaton_slave_run_decider(mock_exit, capsys):
    from zenaton.scripts.slave import main

    with responses.RequestsMock() as rsps:

        # Get a job to do => run a decision
        rsps.add(
            responses.GET,
            'http://localhost:4001/jobs/AD489DB1',
            status=200,
            json={
                'action': 'DecisionScheduled',
                'uuid': '95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            }
        )

        # === 1st run of the decider: schedule a task

        # {"action": "start"}
        rsps.add(
            responses.POST,
            'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            json={
                'properties': '{"count": 1}',
                'name': 'zenaton.testing.examples.readme:MyWorkflow',
                'event': None,
            },
        )

        # {"action": "execute"}
        rsps.add(
            responses.POST,
            'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            json={
                'status': 'scheduled',
            },
        )

        # {"action": "terminate"}
        rsps.add(
            responses.POST,
            'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            json={
                'properties': '{"count": 0}',
                'status': 'running',
            },
        )

        # === 2nd run of the decider: task is completed

        # {"action": "start"}
        rsps.add(
            responses.POST,
            'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            json={
                'properties': '{"count": 1}',
                'name': 'zenaton.testing.examples.readme:MyWorkflow',
                'event': None,
            },
        )

        # {"action": "execute"}
        rsps.add(
            responses.POST,
            'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            json={
                'status': 'completed',
                'properties': '{"count": 1}',
                'outputs': ['null'],
            },
        )

        # {"action": "terminate"}
        rsps.add(
            responses.POST,
            'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            json={
                'properties': '{"count": 0}',
                'status': 'completed',
            },
        )

        # === 3rd run of the decider: we're done

        # {"action": "start"}
        rsps.add(
            responses.POST,
            'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF',
            body='[]',
            content_type='application/json',
        )

        main(['AD489DB1', '8CF89842'])

        assert len(rsps.calls) == 8

        assert rsps.calls[0].request.url == 'http://localhost:4001/jobs/AD489DB1?slave_id=8CF89842'

        # == 1st run of the decider: schedule a task

        assert rsps.calls[1].request.url == 'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF'
        assert json.loads(rsps.calls[1].request.body) == {
            'action': 'start',
        }

        assert rsps.calls[2].request.url == 'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF'
        assert json.loads(rsps.calls[2].request.body) == {
            'action': 'execute',
            'works': [
                {
                    'input': '{"value": 1}',
                    'name': 'zenaton.testing.examples.readme:Echo',
                    'position': '1',
                    'timeout': 2147483647,
                    'type': 'task',
                }
            ],
        }

        assert rsps.calls[3].request.url == 'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF'
        assert json.loads(rsps.calls[3].request.body) == {
            'action': 'terminate',
            'properties': '{"count": 1}',
            'status': 'running',
        }

        # === 2nd run of the decider: task is completed

        assert rsps.calls[4].request.url == 'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF'
        assert json.loads(rsps.calls[4].request.body) == {
            'action': 'start',
        }

        assert rsps.calls[5].request.url == 'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF'
        assert json.loads(rsps.calls[5].request.body) == {
            'action': 'execute',
            'works': [
                {
                    'input': '{"value": 1}',
                    'name': 'zenaton.testing.examples.readme:Echo',
                    'position': '1',
                    'timeout': 2147483647,
                    'type': 'task',
                }
            ],
        }

        assert rsps.calls[6].request.url == 'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF'
        assert json.loads(rsps.calls[6].request.body) == {
            'action': 'terminate',
            'properties': '{"count": 0}',
            'output': 'null',
            'status': 'completed',
        }

        # === 3rd run of the decider: we're done

        assert rsps.calls[7].request.url == 'http://localhost:4001/decisions/95BBD85D-CC3F-4401-9337-D329FC4CDBEF'
        assert json.loads(rsps.calls[7].request.body) == {
            'action': 'start',
        }


    # out, err = capsys.readouterr()
    # assert out == '10\n'
    # assert err == ''

    mock_exit.assert_called_once_with(0)
