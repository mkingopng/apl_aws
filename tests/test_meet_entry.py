"""

"""
from unittest.mock import patch
import pytest
from entry_form.meet_entry import StreamlitApp


@pytest.fixture(autouse=True)
def mock_dynamodb_handler():
    with patch('entry_form.meet_entry.DynamoDBHandler') as MockHandler:
        MockHandler.return_value = MockHandler()  # Mock instance
        yield


# Example of testing non-UI logic in StreamlitApp
def test_streamlit_app_logic():
    """

    :return:
    """
    # Implement tests for non-UI methods of StreamlitApp
    pass
    # todo: add more tests
