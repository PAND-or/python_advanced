import pytest
from datetime import datetime
from text.controllers import get_lower_text


@pytest.fixture
def lower_text_request():
    return {
        'action': 'lower_text',
        'time': datetime.now().timestamp(),
        'data': 'LOWER TEXT',
    }


@pytest.fixture
def lower_text_response_data():
    return 'lower text'


@pytest.fixture
def empty_request():
    return {
        'action': 'upper_text',
        'time': datetime.now().timestamp()
    }


def test_get_lower_text_is_lower(
    lower_text_request,
    lower_text_response_data
):
    response = get_lower_text(lower_text_request)
    assert response.get('data') == lower_text_response_data


def test_get_lower_text_empty(empty_request):
    response = get_lower_text(empty_request)
    assert response.get('response') == 400
