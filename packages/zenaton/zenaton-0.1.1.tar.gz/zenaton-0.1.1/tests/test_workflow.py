from __future__ import absolute_import, print_function, unicode_literals

import pytest

from zenaton.task import Task


class MyTask(Task):

    def __init__(self, x):
        self.x = x

    def handle(self):
        return self.x + 1


@pytest.fixture
def workflow():
    from zenaton.workflow import Workflow

    return Workflow()


class TestExecuteSyncNormal:

    def test_execute_nothing(self, workflow):
        res = workflow.execute()

        assert res is None

    def test_execute_a_task(self, workflow):
        from zenaton.task import Task

        task = MyTask(x=1)

        res = workflow.execute(task)

        assert res == 2

    def test_execute_two_tasks(self, workflow):
        task1 = MyTask(x=1)
        task2 = MyTask(x=2)

        res = workflow.execute(task1, task2)

        assert res == [2, 3]

    def test_execute_not_a_task(self, workflow):
        from zenaton.workflow import NotExecutableError
        with pytest.raises(NotExecutableError):
            workflow.execute(42)


class TestExecuteAsyncNormal:

    def test_execute_nothing(self, workflow):
        res = workflow.execute_async()

        assert res is None

    def test_execute_a_task(self, workflow):
        from zenaton.task import Task

        task = MyTask(x=1)

        res = workflow.execute_async(task)

        assert res is None

    def test_execute_two_tasks(self, workflow):
        task1 = MyTask(x=1)
        task2 = MyTask(x=2)

        res = workflow.execute_async(task1, task2)

        assert res is None
