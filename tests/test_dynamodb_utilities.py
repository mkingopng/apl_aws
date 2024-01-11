"""
Each test method should simulate the corresponding DynamoDB operation and
assert the expected outcomes.
"""
import pytest
from unittest.mock import MagicMock
from ..dynamodb_utilities import DynamoDBHandler
from botocore.exceptions import ClientError
import sys
import os
import logging
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

# Configure logging
logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

# Add a file handler to log to a file
log_handler = logging.FileHandler(f'logs/test_dynamodb_utilities_{current_time}.log')
log_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logging.getLogger().addHandler(log_handler)


class TestDynamoDBHandler:
	@pytest.fixture(autouse=True)
	def setup_method(self, monkeypatch, caplog):
		"""
		Setup for each test method; runs before each test method.
		:param monkeypatch:
		:param caplog:
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

	def test_create_table_success(self, monkeypatch, caplog):
		"""
		Test creating a table successfully
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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

	def test_create_table_failure(self, monkeypatch, caplog):
		"""
		Test failure in creating a table (e.g., due to ClientError)
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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

		# assertions
		error_message = ("Error creating table: An error occurred (InternalError) when calling the CreateTable operation: Internal Error")
		assert any(error_message in record.message for record in caplog.records), "Expected log message not found"
		# todo: other assertions

	def test_add_lifter_success(self, monkeypatch, caplog):
		"""
		Test adding a lifter successfully
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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

	def test_add_lifter_failure(self, monkeypatch, caplog):
		"""
		Test failure in adding a lifter
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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
			assert any(phrase in record.message for record in caplog.records), f"Expected log message '{phrase}' not found"
			# todo: other assertions

	def test_update_lifter_success(self, monkeypatch, caplog):
		"""
		Test updating a lifter successfully
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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

	def test_update_lifter_failure(self, monkeypatch, caplog):
		"""
		Test failure in updating a lifter
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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
			# todo: include other attributes to be updated
		}

		# mock the update_item method to simulate an error during item update
		error_response = {
			'Error': {'Code': 'InternalError', 'Message': 'Internal Error'}}
		mock_table.update_item.side_effect = ClientError(error_response, 'UpdateItem')

		# instantiate DynamoDBHandler and call update_lifter
		handler = DynamoDBHandler('mock_table')
		handler.update_lifter(test_email, update_data)

		# assertions
		error_message = "Error updating lifter data: An error occurred (InternalError) when calling the UpdateItem operation: Internal Error"
		assert any(error_message in record.message for record in caplog.records), "Expected log message not found"
		# todo: other assertions

	def test_delete_lifter_success(self, monkeypatch, caplog):
		"""
		Test deleting a lifter successfully
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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

	def test_delete_lifter_failure(self, monkeypatch, caplog):
		"""
		Test failure in deleting a lifter
		:param monkeypatch:
		:param caplog:
		:return:
		"""
		caplog.set_level(logging.INFO)

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

		# assertions
		error_message = "Error deleting lifter data for email test@example.com: An error occurred (InternalError) when calling the DeleteItem operation: Internal Error"
		assert any(error_message in record.message for record in caplog.records), "Expected log message not found"
		# todo: other assertions

	def test_logging(self, caplog):
		caplog.set_level(logging.DEBUG)
		logging.debug("This is a debug message")

		assert "This is a debug message" in caplog.text
