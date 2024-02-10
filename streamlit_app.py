"""

"""
import boto3
import pandas as pd
from io import StringIO
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


aws_access_key_id = st.secrets['AWS_ACCESS_KEY_ID']
aws_secret_access_key = st.secrets['AWS_SECRET_ACCESS_KEY']


s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

bucket_name = 'open-powerlifting'
object_key = 'open-powerlifting-australia.csv'

obj = s3.get_object(Bucket=bucket_name, Key=object_key)

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


df = pd. read_csv(
    StringIO(obj['Body'].read().decode('utf-8')),
    dtype=dtype_dict,
    converters={'Tested': yes_no_to_bool}
)

filtered_df = df[df['Federation'] == 'AusPL']
filtered_df_copy = filtered_df.copy()
filtered_df_copy['Date'] = pd.to_datetime(filtered_df_copy['Date'])
filtered_df_copy['Year'] = filtered_df_copy['Date'].dt.year


yearly_meet_counts = filtered_df_copy.groupby('Year')['MeetName'].nunique()
# fig = ff.create_table(yearly_meet_counts)
# fig.update_layout(title_text="Number of Meets per Year", title_x=0.5)
# st.plotly_chart(fig)

fig1 = px.bar(
    yearly_meet_counts.reset_index(), x='Year', y='MeetName',
    title='How many meets per year were there?',
    labels={'MeetName': 'Number of Meets'},
    color='MeetName',
    color_continuous_scale=px.colors.sequential.Agsunset
)
fig1.update_layout(
    title_font=dict(size=24),
    xaxis_title='Year',
    yaxis_title='Number of Meets'
)
st.plotly_chart(fig1)

# how many lifters have competed in each year?
yearly_lifter_counts = filtered_df_copy.groupby('Year')['Name'].count()
print(yearly_lifter_counts)

fig2 = px.bar(
    yearly_lifter_counts.reset_index(), x='Year', y='Name',
    title='How many lifters have competed in each year?',
    labels={'Name': 'Total Participants'},
    color='Name',
    color_continuous_scale=px.colors.sequential.Agsunset
)
fig2.update_layout(
    title_font=dict(size=24),
    xaxis_title='Year',
    yaxis_title='Total Participants'
)
st.plotly_chart(fig2)


lifters_per_year = filtered_df_copy.groupby('Year')['Name'].nunique()
print(lifters_per_year)

fig3 = px.bar(
    lifters_per_year.reset_index(),
    x='Year',
    y='Name',
    title='How many Unique Lifters are there per Year?',
    labels={'Name': 'Unique Lifters'},
    color='Name',
    color_continuous_scale=px.colors.sequential.Agsunset
)
fig3.update_layout(
    title_font=dict(size=24),
    xaxis_title='Year',
    yaxis_title='Unique Lifters'
)
st.plotly_chart(fig3)

# how many times have lifters competed each year?
competitions_per_lifter_yearly = filtered_df_copy.groupby(['Year', 'Name']).size().reset_index(name='Competitions')
print(competitions_per_lifter_yearly)

times_competing_pa = competitions_per_lifter_yearly.groupby(['Year', 'Competitions']).size().unstack(fill_value=0)
print(times_competing_pa)

eight_comps_23 = competitions_per_lifter_yearly[(competitions_per_lifter_yearly['Year'] == 2023) & (competitions_per_lifter_yearly['Competitions'] == 8)]
print(eight_comps_23)

# has the gender distribution changed over time?
gender_distribution_yearly = filtered_df_copy.groupby(['Year', 'Sex']).size().unstack(fill_value=0)
gender_distribution_yearly['Total'] = gender_distribution_yearly.sum(axis=1)
gender_distribution_yearly['% Male'] = ((gender_distribution_yearly['M'] / gender_distribution_yearly['Total']) * 100).round(0)
gender_distribution_yearly['% Female'] = ((gender_distribution_yearly['F'] / gender_distribution_yearly['Total']) * 100).round(0)

# display the updated DataFrame
print(gender_distribution_yearly)

# plot 4
fig4 = px.bar(
    gender_distribution_yearly.reset_index(),
    x='Year',
    y=['F', 'M'],
    title='How has the gender balance of competitors changed over time?',
    labels={'value': 'Number of Competitors', 'variable': 'Gender'},
    barmode='group'
)
fig4.update_layout(
    title_font=dict(size=24),
    xaxis_title='Year',
    yaxis_title='Number of Competitors',
    legend_title='Gender'
)
st.plotly_chart(fig4)

######
# streamlit widgets
# federation_select = st.sidebar.selectbox('Select Federation', df['Federation'].unique())
# year_range = st.sidebar.slider('Select Year Range', int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))

# record holders by weight class
# max_totals = filtered_df_copy.groupby(['WeightClassKg', 'Equipment', 'Tested'])['TotalKg'].max().reset_index()
# top_lifters = pd.merge(max_totals, filtered_df, on=['WeightClassKg', 'Equipment', 'Tested', 'TotalKg'], how='left')
# sorted_top_lifters = top_lifters.sort_values(by=['Tested', 'Equipment', 'Sex', 'WeightClassKg'], ascending=[True, True, True, True])
# dfs = {}

# instead of having a loop, use the widgets to filter the data
# for gender in sorted_top_lifters['Sex'].unique():
#     for tested in sorted_top_lifters['Tested'].unique():
#         for equipment in sorted_top_lifters['Equipment'].unique():
#             # Create a key for the dictionary
#             key = f"{gender}_{tested}_{equipment}"
#
#             # Filter the DataFrame for the current combination
#             df_filtered = sorted_top_lifters[
#                 (sorted_top_lifters['Sex'] == gender) &
#                 (sorted_top_lifters['Tested'] == tested) &
#                 (sorted_top_lifters['Equipment'] == equipment)
#                 ]
#
#             # only add to dictionary if the filtered DataFrame is not empty
#             if not df_filtered.empty:
#                 dfs[key] = df_filtered
#
# # Male & not tested, equipment=Raw
# male_not_tested_raw = dfs['M_False_Raw']
#
# # Male & not tested, equipment=Wraps
# male_not_tested_wraps = dfs['M_False_Wraps']
#
# # Male & not tested, equipment=Single-ply
# male_not_tested_single_ply = dfs['M_False_Single-ply']
#
# # Male & not tested, equipment=Multi-ply
# male_not_tested_multi_ply = dfs['M_False_Multi-ply']
#
# # female & not tested, equipment=Raw
# female_not_tested_raw = dfs['F_False_Raw'].reset_index(drop=True)
# _female_not_tested_raw = female_not_tested_raw[['Name', 'WeightClassKg', 'Equipment', 'Tested', 'TotalKg', 'Date', 'MeetName']].drop_duplicates()
#
# # Initialize a figure with go.Figure
# fig = go.Figure(data=[go.Table(
#     header=dict(
#         values=list(_female_not_tested_raw.columns),
#         align='left'
#     ),
#     cells=dict(
#         values=[_female_not_tested_raw[k].tolist() for k in _female_not_tested_raw.columns],
#         align='left'
#     ))
# ])
# fig.update_layout(
#     title_text='National Records Female Raw Untested',
#     title_x=0.5,
#     width=800,
#     height=600
# )
# st.plotly_chart(fig)
#
# # Female & not tested, equipment=Wraps
# female_not_tested_wraps = dfs['F_False_Wraps']
#
# # Female & not tested, equipment=Single-ply
# female_not_tested_single_ply = dfs['F_False_Single-ply']
#
# # Female & not tested, equipment=Multi-ply
# female_not_tested_multi_ply = dfs['F_False_Multi-ply']
#
# # Male & tested, equipment=Raw
# male_tested_raw = dfs['M_True_Raw']
#
# # Female & tested, equipment=Raw
# female_tested_raw = dfs['F_True_Raw']
