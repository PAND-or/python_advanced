import pytest
from datetime import datetime
from text.controllers import get_upper_text


@pytest.fixture
def valid_request():
    return {
        'action': 'upper_text',
        'time': datetime.now().timestamp(),
        'data': 'upper text',
    }


@pytest.fixture
def empty_request():
    return {
        'action': 'upper_text',
        'time': datetime.now().timestamp()
    }


@pytest.fixture
def upper_text_response_data():
    return 'UPPER TEXT'


def test_get_upper_text_is_upper(
    valid_request,
    upper_text_response_data
):
    response = get_upper_text(valid_request)
    assert response.get('data') == upper_text_response_data


def test_get_upper_text_empty(empty_request):
    response = get_upper_text(empty_request)
    assert response.get('response') == 400
