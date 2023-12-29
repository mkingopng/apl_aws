"""
simple web-based entry form to collect lifter's data for meet.

output is JSON to replicate expected output from EventBrite API

"""
import os
import streamlit as st
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import re
from datetime import date

# variables
DATA_PATH = './../data'

# Define the DataFrame structure
columns = [
	"First Name",
	"Last Name",
	"Email",
	"Phone Number",
	"Gender",
	"Equipment",
	"Event",
	"Date of Birth",
	"Next of Kin Name",
	"Next of Kin Phone Number"
]

data = pd.DataFrame(columns=columns)

table_name = 'apl_meet_entry'


# functions
def validate_email(email):
	"""
	This function checks if the provided email string matches the pattern of a
	standard email address. It uses regex to ensure that the email address
	consists of characters allowed in the local part of the email, followed by
	an '@' symbol, and a domain part which includes domain labels separated by
	periods. The domain labels cannot start or end with hyphens.
	:param email: (Str) The email address to be validated.
	:return: (Bool) True if email address is in valid format, else False.
	"""
	pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	return re.match(pattern, email) is not None


def validate_phone_number(phone):
	"""
	Validate a phone number to ensure it has 10 digits and starts with 0.
	This function uses regular expression to validate the phone number format.
	The phone number is expected to be a string or an integer. It first
	converts the phone number to a string (if it isn't already),
	then checks if it matches the pattern of starting with zero followed by
	exactly nine other digits.
	:param phone: (Str or Int): The phone number to be validated.
	:return bool: True if the phone number is valid, False otherwise.
	"""
	pattern = r'^0\d{9}$'
	return re.match(pattern, str(phone)) is not None


def validate_dob(dob):
	"""
	This function checks if the provided date of birth (dob) is a valid date
	not in the future. It compares the dob against the current date. The
	function assumes that the dob is provided as a date object. If the dob is
	today or in the past, the function returns True, indicating it's valid. If
	the dob is in the future, it returns False, indicating an invalid date of
	birth.
	:param dob: (Date) The date of birth to be validated. Expected to be a
	date object.
	:return: (Bool) True if the date of birth is today or in the past,
	False if it is in the future
	"""
	today = date.today()
	return dob <= today


def create_dynamodb_table(table_name):
	"""
	This function attempts to create a new DynamoDB table using the provided
	table name. It sets up the table with 'Email' as the primary key (
	partition key). The function assumes that 'Email' is a string ('S' type in
	DynamoDB). If the table already exists, it will catch the
	'ResourceInUseException' and notify that the table exists. Otherwise, it
	will create the table and set the read and write capacity units as
	specified.
	:param table_name: Str, The name of the DynamoDB table to create.
	:return None: The function returns None. It prints a message to the
	console indicating whether the table was created successfully or if it
	already exists.
	:raises: ClientError: If any error occurs during the table creation
	process, apart from the 'ResourceInUseException', it will raise an
	exception.
	"""
	dynamodb = boto3.resource('dynamodb')

	try:
		table = dynamodb.create_table(
			TableName=table_name,
			KeySchema=[
				{
					'AttributeName': 'Email',
					'KeyType': 'HASH'  # Partition key
				}
			],
			AttributeDefinitions=[
				{
					'AttributeName': 'Email',
					'AttributeType': 'S'
				}
			],
			ProvisionedThroughput={
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
			}
		)
		table.wait_until_exists()
		print(f"Table {table_name} created successfully")
	except ClientError as e:
		if e.response['Error']['Code'] == 'ResourceInUseException':
			print(f"Table {table_name} already exists")
		else:
			raise


def save_to_dynamodb(table_name, data):
	"""
	This function takes a Pandas DataFrame and a table name as input and saves
	each row of the DataFrame as an item in the DynamoDB table. It uses the
	batch_writer of DynamoDB to efficiently write multiple items. The
	DataFrame is expected to be in a format where each row represents a unique
	item, and column names correspond to the attribute names in the DynamoDB
	table.
	:param table_name: (Str) The name of the DynamoDB table where the data
	will be saved.
	:param data: (pd.DataFrame) A Pandas DataFrame containing the data to be
	saved to DynamoDB. Each row should represent a unique item to be inserted
	into the table.
	:return None: The function does not return a value. It prints messages to
	the console indicating the success of data saving or details of any errors
	encountered.
	:raises None: ClientError If an error occurs during the data saving
	process to DynamoDB, it is caught and the error message is printed to the
	console.
	"""
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(table_name)
	try:
		with table.batch_writer() as batch:
			for entry in data.to_dict('records'):
				batch.put_item(Item=entry)
				print("Data saved to DynamoDB.")
	except ClientError as e:
		print(f"Error saving data: {e}")


if __name__ == '__main__':
	# title
	st.title("Australian Powerlifting League \nMeet Registration")

	# creating form fields
	with st.form(key='registration_form'):
		first_name = st.text_input("First Name")

		last_name = st.text_input("Last Name")

		email = st.text_input(
			"Email",
			help="Enter a valid email address"
		)

		phone_number = st.text_input("Mobile Phone Number")

		gender = st.selectbox(
			"Gender",
			options=["Male", "Female"]
		)

		equipment = st.selectbox(
			"Equipment",
			options=[
				"Sleeves",
				"Wraps",
				"Single-ply"
			]
		)

		event = st.selectbox(
			"Event",
			options=[
				"SBD",
				"Bench Only",
				"Deadlift Only"
			]
		)

		dob = st.date_input("Date of Birth")

		nok_name = st.text_input("Next of Kin Name")

		nok_phone = st.text_input("Next of Kin Mobile Phone Number")

		# submit button
		submit_button = st.form_submit_button(label="Submit")

		if submit_button:
			if validate_email(email) and validate_phone_number(phone_number):
				# create a new record as a df
				new_entry_df = pd.DataFrame([{
					"First Name": first_name,
					"Last Name": last_name,
					"Email": email,
					"Phone Number": phone_number,
					"Gender": gender,
					"Equipment": equipment,
					"Event": event,
					"Date of Birth": dob,
					"Next of Kin Name": nok_name,
					"Next of Kin Phone Number": nok_phone
				}])

				# concatenate the new record with the existing df
				data = pd.concat([data, new_entry_df], ignore_index=True)

				# save to JSON
				data.to_json(
					os.path.join(DATA_PATH, "registration_data.json"),
					index=False
				)

				# save_to_dynamodb('YourTableName', data)

				st.success("Registration successful!")
			else:
				st.error("Please enter a valid email address and phone number")
