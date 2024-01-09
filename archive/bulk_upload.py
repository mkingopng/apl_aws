"""
simulate an API call to the Eventbrite API, parse the returned JSON, and then
perform a bulk upload of the lifter data to a DynamoDB database:
	- simulate the API call
	- load and parse the JSOn file
	- transform the data for DynamoDB

"""
import json
import boto3
from entry_form.config import CFG


def load_json_data(json_file_path):
	"""

	:param json_file_path:
	:return:
	"""
	with open(json_file_path, 'r') as file:
		data = json.load(file)
	return data


def upload_to_dynamodb(table_name, items):
	"""

	:param table_name:
	:param items:
	:return:
	"""
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(table_name)
	with table.batch_writer() as batch:
		for item in items:
			batch.put_item(Item=item)


if __name__ == "__main__":
	lifter_data = load_json_data(CFG.json_file_path)
	upload_to_dynamodb(CFG.table_name, lifter_data)