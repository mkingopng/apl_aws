"""

"""
from unittest.mock import patch, Mock
import pytest
from archive.meet_entry import StreamlitApp


@pytest.fixture(autouse=True)
def mock_dynamodb_handler():
    """

    :return:
    """
    with patch('web_site.meet_entry.boto3.resource') as mock_resource:
        mock_resource.return_value.Table.return_value = Mock()
        yield


# Example of testing non-UI logic in StreamlitApp
def test_streamlit_app_logic():
    """

    :return:
    """
    app = StreamlitApp()
    # Implement tests for non-UI methods of StreamlitApp
    pass
    # todo: add more tests
