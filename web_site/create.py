"""

"""
import json
import boto3
import logging


def add_record(event, context):
	"""

	:param event:
	:param context:
	:return:
	"""
	# Initialize DynamoDB
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('apl_meet_entry')

	# Extract record data 'event' assuming 'event' contains the new record data
	new_record = event['record']

	# Add the new record to the table
	response = table.put_item(Item=new_record)

	# log the response (useful for debugging)
	logging.info(f"DynamoDB response: {response}")

	# Return a success response
	return {
		'statusCode': 200,
		'body': json.dumps('Record added successfully!')
	}


# todo: update IAM creds
#  test locally
#  connect to dynamo db in IDE so i can see the data
#  add logging throughout
