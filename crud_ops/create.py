"""
This function adds a new record to the DynamoDB table 'apl-meet-entry'.
"""
import json
import boto3
import logging


def add_record(event, context):
	"""
	Adds a new record to the DynamoDB table 'apl_meet_entry'.
	This function is designed to be used as an AWS Lambda function. It extracts
	record data from the 'event' parameter, adds the record to the DynamoDB
	table, logs the response for debugging, and returns a success response.

	:param event: (dict)
		A dictionary containing the event data. The 'record' key should contain
		the data to be added to the DynamoDB table.
	:param context: (LambdaContext)
		The context in which the Lambda function is running. This parameter is
		not used in the function but is required by AWS Lambda.

	:returns: dict
	A dictionary with a status code indicating success (200) and a body with a
	success message.
	"""
	dynamodb = boto3.resource('dynamodb')  # initialize DynamoDB
	table = dynamodb.Table('apl_meet_entry')

	# extract record data 'event' assuming 'event' contains the new record data
	new_record = event['record']

	response = table.put_item(Item=new_record)  # add new record to table

	logging.info(f"DynamoDB response: {response}")  # log response

	# return a success response
	return {
		'statusCode': 200,
		'body': json.dumps('Record added successfully!')
	}
