import pytest


@pytest.fixture
def position():
    from zenaton.position import Position

    return Position()


def test_default(position):
    assert str(position) == '0'


def test_next(position):
    position.next()
    assert str(position) == '1'

    position.next()
    assert str(position) == '2'


def test_next_parallel(position):
    position.next_parallel()
    assert str(position) == '1p0'

    position.next_parallel()
    assert str(position) == '1p1'
