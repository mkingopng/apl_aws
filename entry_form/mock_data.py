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
from config import CFG
import pandas as pd
from datetime import datetime, timedelta
import random

# pandas display settings
pd.options.display.max_rows = 50
pd.options.display.max_columns = 50
pd.options.display.max_colwidth = 50
pd.options.display.max_info_columns = 100
pd.options.display.precision = 15
pd.options.display.float_format = '{:.2f}'.format

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
		'Name', 'Sex', 'Equipment', 'Age', 'Division', 'BodyweightKg',
		'Country', 'State', 'Federation', 'Date', 'MeetCountry', 'MeetState',
		'MeetTown', 'MeetName'
	]


def get_final_columns():
	"""

	:return:
	"""
	return [
		'first_name', 'last_name', 'age', 'birth_date', 'body_weight_kg',
		'lifter_state', 'lifter_country', 'federation', 'meet_name',
		'meet_date', 'meet_town', 'meet_state', 'meet_country'
	]


def get_fixed_columns_config():
	"""
	Retrieve a list of final column names for the processed lifter dataset.

	This function returns a list of column names that represent the final
	structure
	of the powerlifting dataset after processing. These columns include
	personal
	details of the lifters, such as their names and birth dates, along with
	information about the powerlifting meet they participated in. The function
	is designed to ensure consistency in the dataset's format, particularly
	after
	transformations like splitting names and calculating new fields.

	:return: list of str
		A list containing the final column names to be used in the processed
		dataset.
	"""
	return {
		'federation': CFG.federation,
		'meet_name': CFG.meet_name,
		'meet_date': CFG.meet_date,
		'meet_town': CFG.meet_town,
		'meet_state': CFG.meet_state,
		'meet_country': CFG.meet_country
	}


def split_and_rename_columns(df, split_column, new_columns, rename_dict):
	"""
	Splits a specified column into two new columns and renames existing
	columns.

	This function takes a DataFrame and a column name to split. The specified
	column is split based on a space character, creating two new columns.
	Additionally, it renames existing columns in the DataFrame based on a
	provided mapping dictionary.

	:param df: Pandas DataFrame
		The DataFrame on which the operation will be performed.
	:param split_column: str
		The name of the column in the DataFrame to be split.
	:param new_columns: list of str
		A list containing two new column names that will be created as a
		result of the split.
	:param rename_dict: dict
		A dictionary where keys are old column names and values are new
		column names for renaming.
	:return: Pandas DataFrame
		The modified DataFrame with the specified column split into two new
		columns and other columns renamed as per the rename_dict.
	"""
	df[new_columns] = df[split_column].str.split(' ', expand=True)
	df.rename(columns=rename_dict, inplace=True)
	return df


def clean_data(df, split_column, new_columns, rename_dict):
	"""
	Perform initial cleaning operations on the provided DataFrame.
	This function is designed to handle the preliminary cleaning steps for a
	DataFrame. It currently includes splitting a specified column into two new
	columns and renaming existing columns based on a provided dictionary. The
	function is structured to allow for additional data cleaning steps to be
	easily added in the future.

	:param df: Pandas DataFrame
		The DataFrame to be cleaned.
	:param split_column: str
		The name of the column in the DataFrame to be split.
	:param new_columns: list of str
		A list containing the names of the new columns that will result from
		the split.
	:param rename_dict: dict
		A dictionary mapping current column names to their new names.
	:return: Pandas DataFrame
		The cleaned DataFrame with columns split and renamed, and potentially
		other cleaning operations applied.
	"""
	df = split_and_rename_columns(df, split_column, new_columns, rename_dict)
	# todo: any other data cleaning steps
	return df


def calculate_birth_date(age, current_date):
	"""
	Calculate a synthetic birth date for a lifter based on their age and a
	given date.

	This function estimates a birth date by subtracting the lifter's age from
	the year of the provided current date. It then adds a random number of
	days
	to the start of that year to generate a birth date. This method ensures
	that the calculated birth date is consistent with the lifter's age as of
	the current date.

	Note: The function randomly generates the day and month, so the exact
	birth
	date is synthetic.

	:param age: int
		The age of the lifter, as recorded in meet records.
	:param current_date: datetime
		The current date, used as a reference to calculate the birth year.
	:return: datetime
		The estimated synthetic birth date of the lifter.
	"""
	random_day = random.randint(1, 365)  # random day and month
	birth_year = current_date.year - age  # calculate birth year based on age
	birth_date = datetime(birth_year, 1, 1) + timedelta(
		days=random_day - 1)  # calculate birthdate
	return birth_date


def main():
	"""
	Main function to execute the workflow of generating synthetic lifter data.

	This function orchestrates the process of loading, processing, and
	displaying synthetic data for powerlifting meet participants. It begins
	by loading data from a specified file, retains necessary columns,
	calculates synthetic birth dates, splits and renames columns, and applies
	any other specified cleaning operations. Finally, it consolidates and
	displays the processed data with a predefined set of final columns.

	Steps:
	1. Load data from the specified file path.
	2. Filter the data to keep only the relevant columns.
	3. Calculate synthetic birth dates for each lifter.
	4. Clean the data by splitting and renaming columns.
	5. Apply additional fixed column values from configuration.
	6. Restructure the DataFrame to include only the final set of columns.
	7. Display the first five rows of the processed DataFrame.

	Note: The file path and other configurations are sourced from an
	external configuration module.

	:return: None
		The function doesn't return any value; instead, it prints the first
		five rows of the processed DataFrame.
	"""
	file_path = CFG.BULK_DATA
	df = load_data(file_path)
	columns_to_keep = get_columns_to_keep()
	df = df[columns_to_keep]
	df['birth_date'] = df['Age'].apply(
		lambda age: calculate_birth_date(age, CFG.today))
	df = clean_data(df, 'Name', ['first_name', 'last_name'], rename_dict)
	fixed_cols = get_fixed_columns_config()
	for c, v in fixed_cols.items():
		df[c] = v
	final_columns = get_final_columns()
	new_df = df[final_columns]
	print(new_df.head(5))


# todo:
#  tests
#  randomly populate lifter_state from list,
#  format first name,
#  format last name,
#  correct dtype for dates x2
#  make up names for CFG.constants


if __name__ == "__main__":
	main()
