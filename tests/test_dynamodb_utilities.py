"""

"""
from unittest.mock import patch, Mock
from entry_form.dynamodb_utilities import DynamoDBHandler


# Example of testing DynamoDBHandler's create_table method
def test_create_table():
    """

    :return:
    """
    with patch('web_site.dynamodb_utilities.boto3') as mock_boto3:
        mock_dynamodb = Mock()
        mock_boto3.resource.return_value = mock_dynamodb

        # setting up mock return value for list_tables()
        mock_dynamodb.meta.client.list_tables.return_value = {'TableNames': ['existing_table', 'another_table']}

        handler = DynamoDBHandler("test_table")
        handler.create_table()

        # assertions
        mock_dynamodb.create_table.assert_called_once()
        # todo: add more tests
