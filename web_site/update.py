"""
This module provides functionality to update existing records in the
'apl_meet_entry'  DynamoDB table. It defines a Lambda function that can be
triggered to perform update operations on specific items identified by their
primary key (Email).

The script uses AWS Boto3 to interact with DynamoDB and applies updates to
specified fields of a record. The update operation is dynamic, allowing for
variable fields to be updated based on the input provided.

Usage:
    - The function expects an event object containing an 'Email' key for
    identifying the record and an 'UpdateData' dictionary with fields and
    values to be updated.
    - The Lambda function can be triggered manually, via AWS services, or
    through an API Gateway endpoint.

Requirements:
    - AWS SDK for Python (Boto3)
    - Properly configured AWS credentials with access to the DynamoDB table
"""
import json
import boto3
# from config import CFG
from web_site import table_name


def update_record(event, context):
	"""

	:param event:
	:param context:
	:return:
	"""
	dynamodb = boto3.resource('dynamodb')  # initialize DynamoDB
	table = dynamodb.Table(table_name)  # specify table

	email = event.get('Email')  # extract data from the event
	update_data = event.get('UpdateData')  # contains fields to be updated

	# update expression
	update_expression = "SET " + ", ".join(f"{k}=:{k}" for k in update_data.keys())

	# expression attribute values
	expr_attribute_values = {f":{k}": v for k, v in update_data.items()}

	# update item in DynamoDB
	response = table.update_item(
		Key={'Email': email},
		UpdateExpression=update_expression,
		ExpressionAttributeValues=expr_attribute_values,
		ReturnValues="UPDATED_NEW"
	)

	return {
		'statusCode': 200,
		'body': json.dumps('Record updated successfully!')
	}
