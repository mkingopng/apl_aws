"""
Each test method should simulate the corresponding DynamoDB operation and
assert the expected outcomes.
"""
import pytest
from unittest.mock import MagicMock, patch
from web_site.dynamodb_utilities import DynamoDBHandler
from botocore.exceptions import ClientError


class TestDynamoDBHandler:
	@pytest.fixture(autouse=True)
	def setup_method(self, monkeypatch):
		"""
		Setup for each test method; runs before each test method.
		:param monkeypatch:
		:return:
		"""
		# mock the boto3 resource
		self.mock_dynamodb_resource = MagicMock()
		self.mock_table = MagicMock()
		self.mock_dynamodb_resource.Table.return_value = self.mock_table
		monkeypatch.setattr('boto3.resource', self.mock_dynamodb_resource)

		# instantiate DynamoDBHandler with a mock table name
		self.test_table_name = 'mock_table'
		self.handler = DynamoDBHandler(self.test_table_name)

	def test_create_table_success(self, monkeypatch):
		"""
		Test creating a table successfully
		:param monkeypatch:
		:return:
		"""
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# Mock the list_tables method to simulate that the table does not exist
		mock_dynamodb_client = MagicMock()
		mock_dynamodb_client.list_tables.return_value = {'TableNames': []}
		mock_dynamodb_resource.meta.client = mock_dynamodb_client

		# mock the create_table method to simulate table creation
		mock_dynamodb_resource.create_table.return_value = mock_table

		# use monkeypatch to replace boto3 resource with our mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# instantiate DynamoDBHandler and call create_table
		handler = DynamoDBHandler('mock_table')
		handler.create_table()

		# assertions
		mock_dynamodb_resource.create_table.assert_called_once()
		mock_table.wait_until_exists.assert_called_once()
		# todo: other assertions

	def test_create_table_failure(self, monkeypatch, capsys):
		"""
		Test failure in creating a table (e.g., due to ClientError)
		:param monkeypatch:
		:param capsys:
		:return:
		"""
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# mock the list_tables method to simulate that the table does not exist
		mock_dynamodb_client = MagicMock()
		mock_dynamodb_client.list_tables.return_value = {'TableNames': []}
		mock_dynamodb_resource.meta.client = mock_dynamodb_client

		# mock create_table method to simulate an error during table creation
		error_response = {
			'Error': {'Code': 'InternalError', 'Message': 'Internal Error'}}
		mock_dynamodb_resource.create_table.side_effect = ClientError(
			error_response, 'CreateTable')

		# use monkeypatch to replace boto3 resource with our mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# instantiate DynamoDBHandler and call create_table
		handler = DynamoDBHandler('mock_table')
		handler.create_table()

		# capture the output
		captured = capsys.readouterr()

		# assertions
		error_message = (
			"Error creating table: An error occurred (InternalError) when "
			"calling the CreateTable operation: Internal Error"
		)
		assert error_message in captured.out
		# todo: other assertions

	def test_add_lifter_success(self, monkeypatch, capsys):
		"""
		Test adding a lifter successfully
		:param monkeypatch:
		:param capsys:
		:return:
		"""
		# mock DynamoDB table
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# use monkeypatch to replace boto3 resource with mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# prepare test data
		test_lifter_data = {
			'Email': 'test@example.com',
			'Name': 'Test Lifter',
			# todo: add other necessary lifter attributes
		}

		# instantiate DynamoDBHandler and call add_lifter
		handler = DynamoDBHandler('mock_table')
		handler.add_lifter(test_lifter_data)

		# assertions
		mock_table.put_item.assert_called_once_with(Item=test_lifter_data)
		# todo: other assertions

	def test_add_lifter_failure(self, monkeypatch, capsys):
		"""
		Test failure in adding a lifter
		:param monkeypatch:
		:param capsys:
		:return:
		"""
		# mock DynamoDB Table
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# use monkeypatch to replace boto3 resource with our mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# mock the put_item method to simulate an error during item addition
		error_response = {
			'Error': {'Code': 'InternalError', 'Message': 'Internal Error'}}
		mock_table.put_item.side_effect = ClientError(error_response, 'PutItem')

		# prepare test data
		test_lifter_data = {
			'Email': 'test@example.com',
			'Name': 'Test Lifter',
			# todo: add other necessary lifter attributes
		}

		# instantiate DynamoDBHandler and call add_lifter
		handler = DynamoDBHandler('mock_table')
		handler.add_lifter(test_lifter_data)

		# capture the output
		captured = capsys.readouterr()
		# print("Captured Output:", captured.out)

		# break down the error message into key phrases
		phrases = [
			"Error adding lifter data:",
			"An error occurred",
			"(InternalError)",
			"when calling the PutItem operation",
			"Internal Error"
		]

		# check each phrase is in the captured output
		for phrase in phrases:
			assert phrase in captured.out
			# todo: other assertions

	def test_update_lifter_success(self, monkeypatch):
		"""
		Test updating a lifter successfully
		:param monkeypatch:
		:return:
		"""
		# mock DynamoDB Table
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# use monkeypatch to replace boto3 resource with our mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# prepare test data
		test_email = 'test@example.com'
		update_data = {
			'Name': 'Updated Name',
			# include other attributes to be updated
		}

		# instantiate DynamoDBHandler and call update_lifter
		handler = DynamoDBHandler('mock_table')
		handler.update_lifter(test_email, update_data)

		# assertions
		mock_table.update_item.assert_called_once()
		args, kwargs = mock_table.update_item.call_args
		assert kwargs['Key'] == {'Email': test_email}
		assert 'set Name=:Name' in kwargs['UpdateExpression']
		for key, value in update_data.items():
			assert kwargs['ExpressionAttributeValues'][f':{key}'] == value
			# todo: other assertions

	def test_update_lifter_failure(self, monkeypatch, capsys):
		"""
		Test failure in updating a lifter
		:param monkeypatch:
		:param capsys:
		:return:
		"""
		# mock DynamoDB Table
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# use monkeypatch to replace boto3 resource with our mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# prepare test data
		test_email = 'test@example.com'
		update_data = {
			'Name': 'Updated Name',
			# include other attributes to be updated
		}

		# mock the update_item method to simulate an error during item update
		error_response = {
			'Error': {'Code': 'InternalError', 'Message': 'Internal Error'}}
		mock_table.update_item.side_effect = ClientError(error_response, 'UpdateItem')

		# instantiate DynamoDBHandler and call update_lifter
		handler = DynamoDBHandler('mock_table')
		handler.update_lifter(test_email, update_data)

		# capture the output
		captured = capsys.readouterr()

		# assertions
		error_message = "Error updating lifter data: An error occurred (InternalError) when calling the UpdateItem operation: Internal Error"
		assert error_message in captured.out
		# todo: other assertions

	def test_delete_lifter_success(self, monkeypatch):
		"""
		Test deleting a lifter successfully
		:param monkeypatch:
		:param capsys:
		:return:
		"""
		# mock DynamoDB Table
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# use monkeypatch to replace boto3 resource with our mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# prepare test data
		test_email = 'test@example.com'

		# instantiate DynamoDBHandler and call delete_lifter
		handler = DynamoDBHandler('mock_table')
		handler.delete_lifter(test_email)

		# assertions
		mock_table.delete_item.assert_called_once_with(
			Key={'Email': test_email})
		# todo: other assertions

	def test_delete_lifter_failure(self, monkeypatch, capsys):
		"""
		Test failure in deleting a lifter
		:param monkeypatch:
		:param capsys:
		:return:
		"""
		# mock DynamoDB Table
		mock_dynamodb_resource = MagicMock()
		mock_table = MagicMock()
		mock_dynamodb_resource.Table.return_value = mock_table

		# use monkeypatch to replace boto3 resource with our mock
		monkeypatch.setattr('boto3.resource', lambda
			service_name: mock_dynamodb_resource if service_name == 'dynamodb' else None)

		# prepare test data
		test_email = 'test@example.com'

		# mock the delete_item method to simulate an error during item deletion
		error_response = {
			'Error': {'Code': 'InternalError', 'Message': 'Internal Error'}}
		mock_table.delete_item.side_effect = ClientError(error_response, 'DeleteItem')

		# instantiate DynamoDBHandler and call delete_lifter
		handler = DynamoDBHandler('mock_table')
		handler.delete_lifter(test_email)

		# capture the output
		captured = capsys.readouterr()

		# assertions
		error_message = "Error deleting lifter data: An error occurred (InternalError) when calling the DeleteItem operation: Internal Error"
		assert error_message in captured.out
		# todo: other assertions
