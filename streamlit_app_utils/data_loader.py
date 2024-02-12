import pandas as pd
import streamlit as st
import boto3
from io import StringIO, BytesIO


s3_url = "s3://open-powerlifting/open-powerlifting-australia.csv"
aws_access_key_id = st.secrets['AWS_ACCESS_KEY_ID']
aws_secret_access_key = st.secrets['AWS_SECRET_ACCESS_KEY']


s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

bucket_name = 'open-powerlifting'
object_key = 'open-powerlifting-australia.csv'

dtype_dict = {
    'State': 'string',
    'ParentFederation': 'string',
    'MeetState': 'string',
    'Bench4kg': 'float'
}


def yes_no_to_bool(value):
    """
    converts "Yes" to True and empty values to False
    :param value:
    :return:
    """
    if value == 'Yes':
        return True
    else:
        return False


def load_data(bucket_name, object_key):
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    data = pd.read_csv(BytesIO(obj['Body'].read()), dtype=dtype_dict,
                       converters={'Tested': yes_no_to_bool})
    return data


def home_page():
    st.title("Home page")
    # contents


df = load_data(bucket_name, object_key)
filtered_df = df[df['Federation'] == 'AusPL']
filtered_df_copy = filtered_df.copy()
filtered_df_copy['Date'] = pd.to_datetime(filtered_df_copy['Date'])
filtered_df_copy['Year'] = filtered_df_copy['Date'].dt.year

# how many meets per year?
yearly_meet_counts = filtered_df_copy.groupby('Year')['MeetName'].nunique()

# how many lifters have competed in each year?
yearly_lifter_counts = filtered_df_copy.groupby('Year')['Name'].count()

# how many unique lifters per year?
lifters_per_year = filtered_df_copy.groupby('Year')['Name'].nunique()

# has the gender distribution changed over time?
gender_distribution_yearly = filtered_df_copy.groupby(['Year', 'Sex']).size().unstack(fill_value=0)
gender_distribution_yearly['Total'] = gender_distribution_yearly.sum(axis=1)
gender_distribution_yearly['% Male'] = ((gender_distribution_yearly['M'] / gender_distribution_yearly['Total']) * 100).round(0)
gender_distribution_yearly['% Female'] = ((gender_distribution_yearly['F'] / gender_distribution_yearly['Total']) * 100).round(0)

# how many times have lifters competed each year?
competitions_per_lifter_yearly = filtered_df_copy.groupby(['Year', 'Name']).size().reset_index(name='Competitions')
times_competing_pa = competitions_per_lifter_yearly.groupby(['Year', 'Competitions']).size().unstack(fill_value=0)
print(times_competing_pa)

eight_comps_23 = competitions_per_lifter_yearly[(competitions_per_lifter_yearly['Year'] == 2023) & (competitions_per_lifter_yearly['Competitions'] == 8)]
print(eight_comps_23)
