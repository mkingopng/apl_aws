"""
iterate through all csv files
"""
import pandas as pd
import os
from variables import directory, expected_dtypes

pd.options.display.max_rows = 50
pd.options.display.max_columns = 50
pd.options.display.max_colwidth = 50
pd.options.display.max_info_columns = 100
pd.options.display.precision = 15
pd.options.display.float_format = '{:.2f}'.format

combined_df = pd.DataFrame()  # create empty df

# iterate through files in dir
for filename in os.listdir(directory):
	if filename.endswith('.csv'):  # check that file
		file_path = os.path.join(directory, filename)  # construct filepath
		df = pd.read_csv(file_path)  # read CSV
		combined_df = pd.concat([combined_df, df], ignore_index=True)

print(combined_df)
