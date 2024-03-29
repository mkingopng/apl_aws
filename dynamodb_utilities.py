"""
This module provides methods to interact with dynamodb
"""
import logging
import csv
import io
import boto3
from botocore.exceptions import ClientError
from CFG import current_time


# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# add handlers once, check if they already exist
if not logger.handlers:
    c_handler = logging.StreamHandler()  # console handler
    c_handler.setLevel(logging.INFO)

    f_handler = logging.FileHandler(f'logs/dynamodb_log_{current_time}.log')
    f_handler.setLevel(logging.INFO)  # file handler

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(formatter)  # Create formatters & add to handlers
    f_handler.setFormatter(formatter)

    logger.addHandler(c_handler)  # add handlers to the logger
    logger.addHandler(f_handler)


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

    def process_csv(self, file_stream):
        """
        Process a CSV file and return a list of dictionaries for each row.
        :param file_stream: File stream of the CSV file.
        :return: List of dictionaries.
        """
        required_headers = {'Email', 'first_name', 'last_name'}   # Add all required headers
        stream = io.StringIO(file_stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)

        if not required_headers.issubset(set(csv_input.fieldnames)):
            missing_headers = required_headers - set(csv_input.fieldnames)
            logger.error(f"Missing required headers: {missing_headers}")
            return []

        lifters = []
        for row in csv_input:
            lifters.append(row)

        return lifters

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

    def get_all_lifters_emails(self):
        """
        Retrieve all lifter data from the DynamoDB table.
        :return: List of lifter data
        """
        try:
            response = self.table.scan()
            lifters = response.get('Items', [])
            emails = [lifter['Email'] for lifter in lifters]  # Extract only emails
            logging.info(f"Successfully retrieved {len(lifters)} lifters.")
            return emails
        except ClientError as e:
            logging.error(f"Error retrieving lifter data: {e}")
            return []

    def update_lifter_data(self, email, weigh_in_data):
        """
        Update the lifter's record in DynamoDB
        :param email:
        :param weigh_in_data:
        :return:
        """
        try:
            response = self.table.update_item(
                Key={'Email': email},
                UpdateExpression="set #bw = :bw, #so = :so",
                ExpressionAttributeNames={
                    '#bw': 'body_weight',
                    '#so': 'squat_opener',
                    # todo: add other fields here
                },
                ExpressionAttributeValues={
                    ':bw': weigh_in_data['body_weight'],
                    ':so': weigh_in_data['squat_opener'],
                    # Add other fields here
                },
                ReturnValues="UPDATED_NEW"
            )
            return response
        except ClientError as e:
            logger.error(f"Error updating lifter data in DynamoDB: {e.response['Error']['Message']}")
            return None

    def get_lifters_details(self, email):
        """
        Retrieve all lifter emails from the DynamoDB table.
        :return: List of emails or an empty list if there are no lifters
        """
        try:
            response = self.table.get_item(Key={'Email': email})
            if 'Item' in response:
                logger.info(f"Retrieved data for {email}: {response['Item']}")
                return response['Item']
            else:
                return None
        except ClientError as e:
            logging.error(f"Error retrieving lifter data: {e}")
            raise

    def get_all_lifters(self):
        """
        Retrieve all lifter data from the DynamoDB table to be displayed in summary page.
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
