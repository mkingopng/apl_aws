"""

"""
import json
import boto3


def read_record(event, context):
	"""

	:param event:
	:param context:
	:return:
	"""
	# initialize DynamoDB
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('apl_meet_entry')

	# extract the key from the event
	email = event.get('Email')

	# fetch the item from DynamoDB
	response = table.get_item(Key={'Email': email})

	# check if the item was found
	item = response.get('Item', {})
	if not item:
		return {
			'statusCode': 404,
			'body': json.dumps('Item not found')
		}

	# return the found item
	return {
		'statusCode': 200,
		'body': json.dumps(item)
	}
