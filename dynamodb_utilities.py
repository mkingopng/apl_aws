"""
This module provides methods to interact with dynamodb
"""
import logging
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


current_time = datetime.now().strftime("%Y%m%d-%H%M%S")


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
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)

		# create handlers (console and file handlers)
		c_handler = logging.StreamHandler()
		f_handler = logging.FileHandler(
			f'logs/{datetime.now().strftime("%Y%m%d-%H%M%S")}_dynamodb.log')
		c_handler.setLevel(logging.INFO)
		f_handler.setLevel(logging.INFO)

		# create formatters and add it to handlers
		formatter = logging.Formatter(
			'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		c_handler.setFormatter(formatter)
		f_handler.setFormatter(formatter)

		# add handlers to the logger
		if not self.logger.handlers:
			self.logger.addHandler(c_handler)
			self.logger.addHandler(f_handler)

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
				logging.info(f"Table {self.table_name} already exists")
				return

			# table creation code
			self.table = self.dynamodb.create_table(
				TableName=self.table_name,
				KeySchema=[{'AttributeName': 'Email', 'KeyType': 'HASH'}],
				AttributeDefinitions=[{'AttributeName': 'Email', 'AttributeType': 'S'}],
				ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
			)
			self.table.wait_until_exists()
			logging.info(f"Table {self.table_name} created successfully.")
		except ClientError as e:
			logging.error(f"Error creating table: {e}")

	def add_lifter(self, lifter_data):
		"""
		Add a new item to the DynamoDB table.
		:param lifter_data:
		:return:
		"""
		try:
			response = self.table.put_item(Item=lifter_data)
			logging.info("Lifter data added successfully: %s", response)
		except ClientError as e:
			logging.error("Error adding lifter data: %s", e)

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
			logging.info("Lifter data updated successfully. Response: %s", response)
		except ClientError as e:
			print(e)
			logging.error("Error updating lifter data: %s", e)

	def delete_lifter(self, email):
		"""
		Delete an item from the DynamoDB table.
		:param email:
		:return:
		"""
		try:
			response = self.table.delete_item(Key={'Email': email})
			logging.info(f"Lifter data deleted successfully for email {email}. Response: {response}")
		except ClientError as e:
			logging.error(f"Error deleting lifter data for email {email}: {e}")

	def get_all_lifters(self):
		"""
		Retrieve all lifter data from the DynamoDB table.
		:return: List of lifter data
		"""
		try:
			response = self.table.scan()
			lifters = response.get('Items', [])
			logging.info(f"Successfully retrieved {len(lifters)} lifters.")
			return lifters
		except ClientError as e:
			logging.error(f"Error retrieving lifter data: {e}")
			return []
