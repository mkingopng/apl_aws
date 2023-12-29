"""
This module provides methods to interact with dynamodb
"""
import boto3
from botocore.exceptions import ClientError


class DynamoDBHandler:
	"""
	This class provides methods to
		- create a DynamoDB table,
		- add a new item to the table,
		- update an existing item in the table, and
		- delete an item from the table.
	"""
	def __init__(self, table_name):
		self.dynamodb = boto3.resource('dynamodb')
		self.table_name = table_name
		self.table = self.dynamodb.Table(table_name)

	def create_table(self):
		"""
		Create a DynamoDB table if it does not already exist.
		:return:
		"""
		try:
			existing_tables = self.dynamodb.meta.client.list_tables()['TableNames']
			if self.table_name in existing_tables:
				print(f"Table {self.table_name} already exists")
				return

			# table creation code
			self.table = self.dynamodb.create_table(
				TableName=self.table_name,
				KeySchema=[{'AttributeName': 'Email', 'KeyType': 'HASH'}],
				AttributeDefinitions=[{'AttributeName': 'Email', 'AttributeType': 'S'}],
				ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
			)
			self.table.wait_until_exists()
			print(f"Table {self.table_name} created successfully.")
		except ClientError as e:
			print(f"Error creating table: {e}")

	def add_lifter(self, lifter_data):
		"""
		Add a new item to the DynamoDB table.
		:param lifter_data:
		:return:
		"""
		try:
			self.table.put_item(Item=lifter_data)
			print("Lifter data added successfully.")
		except ClientError as e:
			print(f"Error adding lifter data: {e}")

	def update_lifter(self, email, update_data):
		"""
		Update an existing item in the DynamoDB table.
		:param email:
		:param update_data:
		:return:
		"""
		try:
			response = self.table.update_item(
				Key={'Email': email},
				UpdateExpression="set " + ", ".join([f"{k}=:{k}" for k in update_data.keys()]),
				ExpressionAttributeValues={f":{k}": v for k, v in update_data.items()},
				ReturnValues="UPDATED_NEW"
			)
			print("Lifter data updated successfully:", response)
		except ClientError as e:
			print(f"Error updating lifter data: {e}")

	def delete_lifter(self, email):
		"""
		Delete an item from the DynamoDB table.
		:param email:
		:return:
		"""
		try:
			self.table.delete_item(Key={'Email': email})
			print("Lifter data deleted successfully.")
		except ClientError as e:
			print(f"Error deleting lifter data: {e}")
