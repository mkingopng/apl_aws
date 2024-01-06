"""
This module generates synthetic lifter data based on historical powerlifting
meet records. It simulates an API call by creating a structured dataset that
mimics the response format typically received from a powerlifting meet data
API.

The synthetic data is derived from past meet results, including details such as
lifter names, ages, equipment used, and performance metrics. This data is
processed to generate realistic birth dates and other required fields. The
resulting dataset is structured to resemble JSON-like API responses, making it
suitable for testing data processing, loading routines, and integration with a
DynamoDB database.

The module's functions handle various aspects of data manipulation such as
reading historical data, splitting and renaming columns, generating new columns
with fixed values, and calculating birth dates based on lifter's age and
current date.

Usage:
- To generate a DataFrame of synthetic lifter data for development and testing
purposes.
- To simulate API responses for testing downstream data processing and database
integration.
"""
# from config import CFG
from config import federation, meet_name, meet_date, meet_town, meet_state, \
	meet_country, BULK_DATA, today
import pandas as pd
from datetime import datetime, timedelta
import random

# pandas display settings
# pd.options.display.max_rows = 50
# pd.options.display.max_columns = 50
# pd.options.display.max_colwidth = 50
# pd.options.display.max_info_columns = 100
# pd.options.display.precision = 15
pd.options.display.float_format = '{:.2f}'.format

# list of Australian states and territories
states = ['QLD', 'NSW', 'VIC', 'SA', 'WA', 'TAS', 'NT', 'ACT']

# define a dictionary mapping old column names to new ones
rename_dict = {
	'Sex': 'gender',
	'Equipment': 'equipment',
	'Age': 'age',
	'Division': 'division',
	'Country': 'lifter_country',
	'State': 'lifter_state',
	'BodyweightKg': 'body_weight_kg',
}


def load_data(file_path):
	"""
	Load data from a CSV file into a Pandas DataFrame.

	This function reads a CSV file specified by the file path and loads it
	into
	a DataFrame using Pandas. It assumes that the first line of the CSV file
	contains the column headers.

	:param file_path: str
		The path to the CSV file to be loaded.

	:return: DataFrame
		A Pandas DataFrame containing the data loaded from the CSV file.
	"""
	return pd.read_csv(file_path)


def get_columns_to_keep():
	"""
	Define a list of column names to be retained from the powerlifting
	dataset.

	This function provides a predefined list of column names that are
	considered
	relevant for further data processing and analysis. These columns are
	selected
	based on their importance in representing key aspects of powerlifting meet
	records, such as lifter details, equipment used, and meet information.

	:return: List of str
		A list containing the names of the columns to be kept from the
		dataset.
	"""
	return [
		'Name',
		'Sex',
		'Equipment',
		'Age',
		'Date',
		'Division',
		'BodyweightKg',
		'Country',
		'State',
		'Federation',
		'MeetName',
		'MeetTown',
		'MeetState',
		'MeetCountry',
	]


def get_final_columns():
	return [
		'first_name',
		'last_name',
		'age',
		'birth_date',  # calculated
		'gender',
		# 'weight_class',  # given at entry
		# 'division',
		# 'equipment',
		'body_weight_kg',  # comes in during weigh-in
		'meet_name',  # system generated
		'meet_date',  # system generated
		'meet_town',  # system generated
		'meet_state',  # system generated
		'meet_country'  # system generated
	]


def get_fixed_columns_config():
	return {
		'federation': federation,
		'meet_name': meet_name,
		'meet_date': meet_date,
		'meet_town': meet_town,
		'meet_state': meet_state,
		'meet_country': meet_country
	}


def split_and_rename_columns(df, split_column, new_columns, rename_dict):
	df[new_columns] = df[split_column].str.split(' ', expand=True)
	df.rename(columns=rename_dict, inplace=True)
	return df


def clean_data(df, split_column, new_columns, rename_dict):
	df = split_and_rename_columns(df, split_column, new_columns, rename_dict)
	return df


def calculate_birth_date(age, current_date):
	random_day = random.randint(1, 365)  # random day and month
	birth_year = current_date.year - age  # calculate birth year based on age
	birth_date = datetime(birth_year, 1, 1) + timedelta(
		days=random_day - 1)  # calculate birthdate
	return birth_date


# def main():
# file_path = BULK_DATA
# df = load_data(file_path)
# columns_to_keep = get_columns_to_keep()
# df = df[columns_to_keep]
# df['birth_date'] = df['Age'].apply(
# 	lambda age: calculate_birth_date(age, today))
# df = clean_data(df, 'Name', ['first_name', 'last_name'], rename_dict)
# fixed_cols = get_fixed_columns_config()
# for c, v in fixed_cols.items():
# 	df[c] = v
# final_columns = get_final_columns()
# new_df = df[final_columns]
# print(new_df.head(5))


if __name__ == "__main__":
	# main()
	file_path = BULK_DATA
	df = load_data(file_path)
	columns_to_keep = get_columns_to_keep()
	df = df[columns_to_keep]
	df['birth_date'] = df['Age'].apply(
		lambda age: calculate_birth_date(age, today))
	df = clean_data(df, 'Name', ['first_name', 'last_name'], rename_dict)
	fixed_cols = get_fixed_columns_config()
	for c, v in fixed_cols.items():
		df[c] = v
	final_columns = get_final_columns()
	new_df = df[final_columns]
	# print(new_df.head(5))

	final_df = new_df[[
		'first_name',
		'last_name',
		'gender',
		'birth_date',
		# 'email',  # synthetic
		# 'phone_number',  # synthetic
		# 'nok_name',  # synthetic
		# 'nok_phone'  # synthetic
	]]

	print(final_df.head(5))

"""
todo:
	- randomly populate lifter_state from list, 
	- format first name, make first letter uppercase
	- format last name, make first letter uppercase
	- correct dtype for dates x2
	- make up names for CFG.constants, 
	- tests
"""
