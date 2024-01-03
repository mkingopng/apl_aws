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
import pytest
import sys
import os
import json
sys.path.insert(0, '')
from create import add_record
from read import read_record
from update import update_record
from delete import delete_record


@pytest.fixture
def event_data():
    """
    Fixture to provide event data for testing Lambda functions.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'test_event.json')
    with open(file_path, 'r') as file:
        return json.load(file)


def test_add_record(event_data):
    """
    Test the add_record Lambda function by simulating its invocation.

    This function reads event data and uses it to test the add_record Lambda
    function. It simulates adding a new record to the DynamoDB table and
    prints the result.

    Parameters:
        event_data (dict): The event data to pass to the add_record function.

    Returns:
        The result of the add_record function invocation.
    """
    return add_record(event_data, None)


def test_read_record(event_data):
    """
    Test the read_record Lambda function by simulating its invocation.

    This function uses the provided event data to test the read_record Lambda
    function. It simulates reading a record from the DynamoDB table and prints
    the result.

    Parameters:
        event_data (dict): The event data to pass to the read_record function.

    Returns:
        The result of the read_record function invocation.
    """
    return read_record(event_data, None)


def test_update_record(event_data):
    """
    Test the update_record Lambda function by simulating its invocation.

    This function uses the provided event data to test the update_record Lambda
    function. It simulates updating a record in the DynamoDB table and prints
    the result.

    Parameters:
        event_data (dict): The event data to pass to the update_record function

    Returns:
        The result of the update_record function invocation.
    """
    return update_record(event_data, None)


def test_delete_record(event_data):
    """
    Test the delete_record Lambda function by simulating its invocation.

    This function uses the provided event data to test the delete_record Lambda
    function. It simulates deleting a record from the DynamoDB table and prints
    the result.

    Parameters:
        event_data (dict): The event data to pass to the delete_record function

    Returns:
        The result of the delete_record function invocation.
    """
    return delete_record(event_data, None)


def lambda_test():
    """

    :return:
    """
    with open('test_event.json', 'r') as file:
        event_data = json.load(file)

    print("Add Record Result:", test_add_record(event_data))
    print("Read Record Result:", test_read_record(event_data))
    print("Update Record Result:", test_update_record(event_data))
    print("Delete Record Result:", test_delete_record(event_data))


# if __name__ == "__main__":
#     lambda_test()
