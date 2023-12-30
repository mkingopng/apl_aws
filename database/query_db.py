"""
This module provides functionality to scan and retrieve all items from a
specified
DynamoDB table. It uses AWS Boto3 to interact with DynamoDB, allowing for the
retrieval of small datasets stored in the table.

The script initializes a DynamoDB client, performs a Scan operation on the
specified table, and prints out all the items it retrieves. This is
particularly
useful for tables with small amounts of data, where the Scan operation's
simplicity
outweighs its inefficiency compared to more targeted queries.

Usage:
    Run the script in a Python environment with Boto3 installed and configured
    with the appropriate AWS credentials. The script will output all items from
    the specified DynamoDB table to the console.

Requirements:
    - AWS SDK for Python (Boto3)
    - AWS credentials with DynamoDB access
"""
import boto3


def scan_dynamodb_table(table_name):
	"""
	Scans and retrieves all items from a specified DynamoDB table.

	This function creates a DynamoDB resource client, performs a Scan
	operation
	on the specified table, and returns all the items found. It is designed
	for
	use with tables containing small amounts of data.

	Parameters:
		table_name (str): The name of the DynamoDB table to scan.

	Returns:
		list: A list of dictionaries, where each dictionary represents an item
		found in the specified DynamoDB table.

	Usage:
		Call this function with the name of the DynamoDB table. The function
		will return a list of all items in that table.
	"""
	dynamodb = boto3.resource('dynamodb')  # initialize a DynamoDB client
	table = dynamodb.Table(table_name)  # specify the DynamoDB table
	response = table.scan()  # perform a Scan operation to retrieve all items
	return response['Items']  # return the items


if __name__ == "__main__":
	table_name = 'apl_meet_entry'
	items = scan_dynamodb_table(table_name)

	# print each item
	for item in items:
		print(item)

# todo: output parser to convert json to dataframe
