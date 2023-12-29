"""

"""
from unittest.mock import patch, Mock
from entry_form.dynamodb_utilities import DynamoDBHandler


# Example of testing DynamoDBHandler's create_table method
def test_create_table():
    with patch('entry_form.dynamodb_utilities.boto3') as mock_boto3:
        mock_dynamodb = Mock()
        mock_boto3.resource.return_value = mock_dynamodb

        # Setting up mock return value for list_tables()
        mock_dynamodb.meta.client.list_tables.return_value = {'TableNames': ['existing_table', 'another_table']}

        handler = DynamoDBHandler("test_table")
        handler.create_table()

        # Assertions
        mock_dynamodb.create_table.assert_called_once()
