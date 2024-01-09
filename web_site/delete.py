"""
This module defines a Lambda function for deleting records from the
'apl_meet_entry' DynamoDB table. It uses AWS Boto3 to interact with DynamoDB
and performs deletion operations based on a specified key.

The Lambda function is designed to be triggered with an event containing an
'Email' key. This key is used to identify the record in the DynamoDB table that
needs to be deleted. Upon invocation, the function deletes the specified record
from the table.

Usage:
    The Lambda function can be invoked manually, via AWS services, or through
    an API Gateway endpoint with an event containing the 'Email' key of the
    record to delete.

Requirements:
    - AWS SDK for Python (Boto3)
    - Properly configured AWS credentials with access to the DynamoDB table
"""
import json
import boto3
from ._config import table_name


def delete_record(event, context):
	"""
	Deletes a record from the 'apl_meet_entry' DynamoDB table.

	This Lambda function deletes a record identified by the 'Email' key
	provided in the event. It is designed to handle deletion requests for
	records in the DynamoDB table, effectively removing the specified item.

	:param event: (dict)
	A dictionary containing the 'Email' key, which specifies therecord to be
	deleted from the DynamoDB table.

	:param context: Provides information about the invocation, function, and
	runtime environment. (Unused in this function)

	:returns: dict
	A dictionary with a status code and a message indicating the
	outcome of the deletion operation.

	:usage:
	The function can be invoked with an event like:
	{'Email': 'example@email.com'} to delete the record with the
	specified Email from the DynamoDB table.
	"""
	dynamodb = boto3.resource('dynamodb')  # initialize DynamoDB
	table = dynamodb.Table(table_name)
	email = event.get('Email')  # extract the key (Email) from the event
	response = table.delete_item(Key={'Email': email})  # del item from DB
	return {
		'statusCode': 200,
		'body': json.dumps('Record deleted successfully!')
	}
