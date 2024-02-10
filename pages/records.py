"""
national records
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_app_utils.data_loader import filtered_df_copy

# Assuming df is your original DataFrame
filtered_df_copy['WeightClassKg'] = filtered_df_copy['WeightClassKg'].astype(str).replace('nan', 'Unknown')
weight_classes_sorted = sorted(filtered_df_copy['WeightClassKg'].unique())

# Sidebar widgets for filtering
gender = st.sidebar.selectbox('Gender', ['All'] + sorted(filtered_df_copy['Sex'].unique().tolist()))
equipment = st.sidebar.selectbox('Equipment', ['All'] + sorted(filtered_df_copy['Equipment'].unique().tolist()))
tested = st.sidebar.selectbox('Tested', ['All', True, False])
weight_class = st.sidebar.selectbox('Weight Class', ['All'] + weight_classes_sorted)
year_range = st.sidebar.slider('Select Year Range', int(filtered_df_copy['Year'].min()), int(filtered_df_copy['Year'].max()), (int(filtered_df_copy['Year'].min()), int(filtered_df_copy['Year'].max())))

# Filter DataFrame based on selections
filtered_df = filtered_df_copy[(filtered_df_copy['Year'].between(*year_range))]

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

# Display results
fig = go.Figure(data=[go.Table(
    header=dict(values=top_lifters.columns, align='left'),
    cells=dict(values=[top_lifters[col].tolist() for col in top_lifters.columns], align='left')
)])
fig.update_layout(title_text='Top 3 Lifters Records', title_x=0.5)
st.plotly_chart(fig)


