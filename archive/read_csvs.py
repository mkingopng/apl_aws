"""

"""
import os
import pandas as pd

pd.options.display.max_rows = 50
pd.options.display.max_columns = 50
pd.options.display.max_colwidth = 50
pd.options.display.max_info_columns = 100
pd.options.display.precision = 15
pd.options.display.float_format = '{:.2f}'.format

data_dir = '../data'
file_name = '2023-07-09_strength_quest_3.csv'
path = os.path.join(data_dir, file_name)

df = pd.read_csv(path)
# print(df.info())
print(df.head())
