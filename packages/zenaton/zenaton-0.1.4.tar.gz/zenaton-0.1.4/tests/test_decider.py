from __future__ import absolute_import, print_function, unicode_literals

import pytest

from zenaton.event import Event
from zenaton.workflow import Workflow

from zenaton.testing.compat import MagicMock, call, patch


class MyWorkflow(Workflow):
    def __init__(self, a):
        self.a = a


class MyEvent(Event):
    pass


@pytest.fixture
def decider():
    from zenaton.decider import Decider
    return Decider(
        uuid='F26C7548-F6AB-4C2C-A5EB-745D8BD38D61',
        microserver=MagicMock(),
    )


class TestLaunch:

    def test_launch(self, decider):
        mock_branch1 = MagicMock()
        mock_branch2 = MagicMock()

        decider.get_next_workflow_branch = MagicMock()
        decider.get_next_workflow_branch.side_effect = [
            mock_branch1,
            mock_branch2,
            None,
        ]

        decider.process_workflow_branch = MagicMock()

        decider.launch()

        decider.process_workflow_branch.assert_has_calls([
            call(mock_branch1),
            call(mock_branch2),
        ])

    def test_launch_nothing_to_run(self, decider):
        decider.get_next_workflow_branch = MagicMock()
        decider.get_next_workflow_branch.return_value = None

        decider.process_workflow_branch = MagicMock()

        decider.launch()

        assert not decider.process_workflow_branch.called


def test_get_next_workflow_branch(decider):
    from zenaton.decider import Branch

    decider.microserver.get_workflow_to_execute.return_value = {
        'name': 'MODULE:CLASS',
        'properties': '{"a": 1}',
        'event': '{"name":"test_decider:MyEvent","properties":{}}',
    }
    branch = decider.get_next_workflow_branch()

    decider.microserver.get_workflow_to_execute.assert_called_once_with(
        'F26C7548-F6AB-4C2C-A5EB-745D8BD38D61'
    )
    assert isinstance(branch, Branch)
    assert branch.name == 'MODULE:CLASS'
    assert branch.properties == {"a": 1}
    assert isinstance(branch.event, MyEvent)


class TestHandleErrors:

    def test_handle_errors_ok(self, decider):

        with decider.handle_errors():
            pass

        m_notify_user = decider.microserver.notify_decision_user_error
        assert not m_notify_user.called

        m_notify_internal = decider.microserver.notify_decision_internal_error
        assert not m_notify_internal.called

    @patch('sys.exc_info')
    def test_handle_errors_internal_error(self, mock_exc_info, decider):
        from zenaton.errors import ZenatonError

        mock_exc_info.return_value = ('ETYPE', 'VALUE', 'TB')

        with pytest.raises(ZenatonError):
            with decider.handle_errors():
                raise ZenatonError

        mock_notify = decider.microserver.notify_decision_internal_error
        mock_notify.assert_called_once_with(
            'F26C7548-F6AB-4C2C-A5EB-745D8BD38D61',
            'ETYPE',
            'VALUE',
            'TB',
        )

    @patch('sys.exc_info')
    def test_handle_errors_user_error(self, mock_exc_info, decider):

        mock_exc_info.return_value = ('ETYPE', 'VALUE', 'TB')

        with pytest.raises(RuntimeError):
            with decider.handle_errors():
                raise RuntimeError

        mock_notify = decider.microserver.notify_decision_user_error
        mock_notify.assert_called_once_with(
            'F26C7548-F6AB-4C2C-A5EB-745D8BD38D61',
            'ETYPE',
            'VALUE',
            'TB',
        )


class TestProcessWorkflowBranch:

    def test_process_workflow_branch(self, decider):
        from zenaton.decider import Branch

        m_workflow = MyWorkflow(a=1)

        decider.create_workflow = MagicMock()
        decider.create_workflow.return_value = m_workflow

        decider.run_handler = MagicMock()
        decider.run_handler.return_value = 'OUTPUT'

        m_event = MyEvent()

        decider.process_workflow_branch(
            branch=Branch(
                name='MODULE:CLASS',
                properties={"a": 1},
                event=m_event,
            )
        )

        decider.create_workflow.assert_called_once_with(
            name='MODULE:CLASS',
            properties={"a": 1},
        )

        decider.run_handler.assert_called_once_with(m_workflow, m_event)

        mock_notify = decider.microserver.notify_decision_branch_complete
        mock_notify.assert_called_once_with(
            uuid='F26C7548-F6AB-4C2C-A5EB-745D8BD38D61',
            properties={
                'a': 1,
            },
            output='OUTPUT',
        )

        mock_notify_complete = decider.microserver.notify_decision_complete
        assert not mock_notify_complete.called

    def test_process_workflow_branch_box_exception(self, decider):
        from zenaton.decider import Branch, ScheduledBoxException

        decider.create_workflow = MagicMock()
        decider.create_workflow.return_value = MyWorkflow(a=1)

        decider.run_handler = MagicMock()
        decider.run_handler.side_effect = ScheduledBoxException

        m_event = MyEvent()

        decider.process_workflow_branch(
            branch=Branch(
                name='MODULE:CLASS',
                properties={"a": 1},
                event=m_event,
            )
        )

        mock_notify = decider.microserver.notify_decision_branch_complete
        assert not mock_notify.called

        mock_notify_complete = decider.microserver.notify_decision_complete
        mock_notify_complete.assert_called_once_with(
            uuid='F26C7548-F6AB-4C2C-A5EB-745D8BD38D61',
            properties={
                'a': 1,
            }
        )
