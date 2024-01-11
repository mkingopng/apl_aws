"""
This module provides testing functions to simulate local invocations of AWS
Lambda functions for adding, reading, and updating records in a DynamoDB table.
Each function in this module corresponds to a specific Lambda function and
tests its functionality independently.

The module ensures that each Lambda function ('add_record', 'read_record',
'update_record') is working as expected before being deployed to AWS Lambda.
It uses a JSON file for test event data to simulate the event payload that
Lambda functions would receive in a production environment.
"""
from ..app import app as flask_app
import logging
from datetime import datetime
import pytest
from unittest.mock import patch
import sys
import os
import json
from crud_ops.create import add_record
from crud_ops.read import read_record
from crud_ops.update import update_record
from crud_ops.delete import delete_record


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

current_time = datetime.now().strftime("%Y%m%d-%H%M%S")

# configure logging at the beginning of the script
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_formatter)

# file handler
f_handler = logging.FileHandler(f'logs/test_lambda_{current_time}.log')
f_handler.setLevel(logging.DEBUG)
f_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_formatter)

# add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    :return:
    """
    # setup code here, if any (e.g., configuring the app for testing)
    yield flask_app
    # teardown code here, if any


@pytest.fixture
def client(app, caplog):
    """
    A test client for the app.
    :param app:
    :return:
    """
    return app.test_client()


# test class
class TestAppRoutes:
    @pytest.fixture(autouse=True)
    def setup_method(self, client, monkeypatch):
        """
        Setup for each test method; runs before each test method.
        :param client:
        :param monkeypatch:
        :return:
        """
        self.client = client
        self.monkeypatch = monkeypatch

    def test_entry_get(self, caplog):
        """
        test for GET request
        :return:
        """
        response = self.client.get('/entry')
        assert response.status_code == 200
        assert b'Australian Powerlifting League' in response.data
        # todo: other assertions

    def test_entry_post_success(self):
        """
        test for POST request
        :return:
        """
        with patch('boto3.client') as mock_s3_client:
            mock_s3_client.return_value.upload_fileobj.return_value = None
            with patch('app.handler.add_lifter') as mock_add_lifter:  # watch this line as you refactor the project
                mock_add_lifter.return_value = None

@pytest.fixture(scope="class")
def event_data():
    """
    fixture to provide event data for testing Lambda functions.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'test_event.json')
    with open(file_path, 'r') as file:
        return json.load(file)
    # todo: other assertions


class TestLambdaFunctions:
    """
    class to test Lambda functions.
    """
    @pytest.fixture(autouse=True)
    def setup_class(self, event_data):
        """
        Setup for class; runs once before all methods.
        :param event_data:
        :return:
        """
        self.event_data = event_data
        # todo: replace with actual assertions

    def test_add_record(self):
        """
        Test the add_record Lambda function by simulating its invocation.

        This function reads event data and uses it to test the add_record Lambda
        function. It simulates adding a new record to the DynamoDB table and
        prints the result.

        :param event_data: (dict)
        The event data to pass to the add_record function.

        :return: The result of the add_record function invocation.
        """
        assert add_record(self.event_data, None)
        # todo: replace with actual assertions

    def test_read_record(self):
        """
        Test the read_record Lambda function by simulating its invocation.

        This function uses the provided event data to test the read_record
        Lambda function. It simulates reading a record from the DynamoDB table
        and prints the result.

        :param event_data: (dict) The event data to pass to the read_record
        function.
        :return: The result of the read_record function invocation.
        """
        assert read_record(self.event_data, None)
        # todo: replace with actual assertions

    def test_update_record(self):
        """
        Test the update_record Lambda function by simulating its invocation.

        This function uses the provided event data to test the update_record
        Lambda function. It simulates updating a record in the DynamoDB table
        and prints the result.

        :param event_data: (dict)
        The event data to pass to the update_record function
        :return: The result of the update_record function invocation.
        """
        assert update_record(self.event_data, None)
        # todo: replace with actual assertions

    def test_delete_record(self):
        """
        Test the delete_record Lambda function by simulating its invocation.

        This function uses the provided event data to test the delete_record
        Lambda function. It simulates deleting a record from the DynamoDB table
        and prints the result.

        :params event_data: (dict)
        The event data to pass to the delete_record function

        :return: The result of the delete_record function invocation.
        """
        assert delete_record(self.event_data, None)
        # todo: replace with actual assertions

