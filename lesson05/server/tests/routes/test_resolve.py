import pytest
from routes import resolve


@pytest.fixture
def controller():
    return lambda arg: arg


@pytest.fixture
def routes(controller):
    return [
        {'action': 'upper_text', 'controller': controller},
    ]


def test_resolve(routes, controller):
    resolved = resolve('upper_text', routes)
    assert resolved == controller
