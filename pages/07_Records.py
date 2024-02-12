"""
national records
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_app_utils.data_loader import filtered_df_copy  # Adjust the import path as necessary

# Define weight classes for each gender
weight_classes_women = ['44', '48', '52', '56', '60', '67.5', '75', '82.5', '90', '100', '110', '110+']
weight_classes_men = ['56', '60', '67.5', '75', '82.5', '90', '100', '110', '125', '140', '140+']

st.title('Top Lifters Records')

# Ensure 'Year' is correctly typed as an integer for filtering
filtered_df_copy['Date'] = pd.to_datetime(filtered_df_copy['Date'])
filtered_df_copy['Year'] = filtered_df_copy['Date'].dt.year

# Sidebar widgets for filtering
gender = st.sidebar.selectbox('Gender', ['All'] + sorted(filtered_df_copy['Sex'].unique().tolist()))

# Determine the relevant weight classes based on selected gender
if gender == 'M':
    relevant_weight_classes = ['All'] + weight_classes_men
elif gender == 'F':
    relevant_weight_classes = ['All'] + weight_classes_women
else:
    relevant_weight_classes = ['All'] + sorted(list(set(weight_classes_men + weight_classes_women)))

weight_class = st.sidebar.selectbox('Weight Class', relevant_weight_classes)
equipment = st.sidebar.selectbox('Equipment', ['All'] + sorted(filtered_df_copy['Equipment'].unique().tolist()))
tested = st.sidebar.selectbox('Tested', ['All', True, False])

# Year range slider
year_range = st.sidebar.slider('Select Year Range', int(filtered_df_copy['Year'].min()), int(filtered_df_copy['Year'].max()), (int(filtered_df_copy['Year'].min()), int(filtered_df_copy['Year'].max())))

# Apply filtering based on selections
filtered_df = filtered_df_copy[(filtered_df_copy['Year'] >= year_range[0]) & (filtered_df_copy['Year'] <= year_range[1])]

if gender != 'All':
    filtered_df = filtered_df[filtered_df['Sex'] == gender]
if equipment != 'All':
    filtered_df = filtered_df[filtered_df['Equipment'] == equipment]
if tested != 'All':
    filtered_df = filtered_df[filtered_df['Tested'] == tested]
if weight_class != 'All':
    filtered_df = filtered_df[filtered_df['WeightClassKg'] == weight_class]

# Selecting the top 3 records for each combination
top_lifters = filtered_df.groupby(['WeightClassKg', 'Equipment', 'Tested', 'Sex']).apply(lambda x: x.nlargest(3, 'TotalKg')).reset_index(drop=True)
top_lifters = top_lifters[['Name', 'WeightClassKg', 'Equipment', 'Tested', 'Sex', 'TotalKg', 'Date', 'MeetName']]

# Display results with a table
fig = go.Figure(data=[go.Table(
    header=dict(values=list(top_lifters.columns), align='left'),
    cells=dict(values=[top_lifters[col].tolist() for col in top_lifters.columns], align='left')
)])
fig.update_layout(title_text='Top 3 Lifters Records', title_x=0.5)
st.plotly_chart(fig)
