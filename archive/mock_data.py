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
from CFG import federation, meet_name, meet_date, meet_town, meet_state, \
	meet_country, BULK_DATA, today
import pandas as pd
from datetime import datetime, timedelta
import random
from faker import Faker

# pandas display settings
pd.options.display.max_rows = 50
pd.options.display.max_columns = 50
pd.options.display.max_colwidth = 50
pd.options.display.max_info_columns = 100
pd.options.display.precision = 15
pd.options.display.float_format = '{:.2f}'.format

fake = Faker()

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


def generate_email(first_name, last_name):
	return f"{first_name}.{last_name}@example.com".lower()


def generate_phone_number():
	"""
	Generate an Australian-style mobile phone number.

	Australian mobile phone numbers typically start with '04' and are 10 digits long.
	"""
	# Generate a random number with 8 digits to append to '04'
	random_number = random.randint(10000000, 99999999)
	return f"04{random_number}"


def generate_nok_name():
	return fake.name()


def generate_nok_phone():
	"""
		Generate an Australian-style mobile phone number.

		Australian mobile phone numbers typically start with '04' and are 10 digits long.
		"""
	# Generate a random number with 8 digits to append to '04'
	random_number = random.randint(10000000, 99999999)
	return f"04{random_number}"


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
		'meet_name',  # config
		'meet_date',  # config
		'meet_town',  # config
		'meet_state',  # config
		'meet_country'  # config
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
		'birth_date'
	]].copy()

	# Generate synthetic data
	final_df['email'] = final_df.apply(lambda x: generate_email(x['first_name'], x['last_name']), axis=1)
	final_df['phone_number'] = final_df.apply(lambda _: generate_phone_number(), axis=1)
	final_df['nok_name'] = final_df.apply(lambda _: generate_nok_name(), axis=1)
	final_df['nok_phone'] = final_df.apply(lambda _: generate_nok_phone(), axis=1)

	print(final_df.head(5))
	final_df.to_csv('./../data/synthetic_data.csv', index=False)

"""
todo:
	- randomly populate lifter_state from list, 
	- format first name, make first letter uppercase
	- format last name, make first letter uppercase
	- correct dtype for dates x2
	- make up names for CFG.constants, 
	- tests
"""
