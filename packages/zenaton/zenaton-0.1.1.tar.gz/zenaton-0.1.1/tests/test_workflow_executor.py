from __future__ import absolute_import, print_function, unicode_literals

import pytest

from zenaton.testing.compat import MagicMock


@pytest.fixture
def microserver():
    return MagicMock()


@pytest.fixture
def executor(microserver):
    from zenaton.workflow_executor import WorkflowExecutor

    return WorkflowExecutor(
        uuid='88282738-7A5C-48A5-BEF7-043FD66B7CD1',
        microserver=microserver,
    )


class Task1:
    pass


class Task2:
    pass


class TestBuildBoxes:

    def test_build_boxes_single_sync(self, executor):

        boxes = executor._build_boxes(executables=[Task1], async_=False)

        assert len(boxes) == 1

        assert boxes[0].executable == Task1
        assert boxes[0].position_str == '1'

    def test_build_boxes_multiple_sync(self, executor):

        boxes = executor._build_boxes(executables=[Task1, Task2], async_=False)

        assert len(boxes) == 2

        assert boxes[0].executable == Task1
        assert boxes[0].position_str == '1p0'

        assert boxes[1].executable == Task2
        assert boxes[1].position_str == '1p1'

    def test_build_boxes_single_async(self, executor):

        boxes = executor._build_boxes(executables=[Task1], async_=True)

        assert len(boxes) == 1

        assert boxes[0].executable == Task1
        assert boxes[0].position_str == '1a'

    def test_build_boxes_multiple_async(self, executor):

        boxes = executor._build_boxes(executables=[Task1, Task2], async_=True)

        assert len(boxes) == 2

        assert boxes[0].executable == Task1
        assert boxes[0].position_str == '1a'

        assert boxes[1].executable == Task2
        assert boxes[1].position_str == '2a'
