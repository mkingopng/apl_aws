"""
national records
"""
import streamlit as st
from streamlit_app_utils.data_loader import df
import pandas as pd
import plotly.express as px

# Define weight classes for each gender
weight_classes_women = ['44', '48', '52', '56', '60', '67.5', '75', '82.5', '90', '100', '110', '110+']
weight_classes_men = ['56', '60', '67.5', '75', '82.5', '90', '100', '110', '125', '140', '140+']

# Filter by Federation
df = df[df['Federation'] == 'AusPL']

# Extract unique events and sort them
event_options = sorted(df['Event'].unique())

# Streamlit widgets for user input
gender = st.selectbox('Select Gender', ['', 'Male', 'Female'])
if gender == 'Female':
    weight_classes = weight_classes_women
elif gender == 'Male':
    weight_classes = weight_classes_men
else:
    weight_classes = []

# Ask user for the number of top performers they want to see
n = st.number_input('Select number of top performers to display', min_value=1, value=5, step=1)
weight_class = st.selectbox('Select Weight Class', [''] + weight_classes)
equipment = st.selectbox('Select Equipment', ['', 'Raw', 'Wraps', 'Single-ply', 'Multi-ply'])
selected_event = st.selectbox('Select Event', [''] + event_options)
tested = st.selectbox('Select Tested Status', ['', True, False])

if gender and weight_class and equipment and tested != '' and selected_event and n > 0:

    # Apply filters based on user selection
    if gender:
        df = df[df['Sex'] == ('M' if gender == 'Male' else 'F')]
    if weight_class:
        df = df[df['WeightClassKg'] == weight_class]
    if equipment:
        df = df[df['Equipment'] == equipment]
    if selected_event:
        df = df[df['Event'] == selected_event]
    if tested != '':
        df = df[df['Tested'] == tested]

    # Check if DataFrame is not empty after filtering
    if not df.empty:
        # Sort by TotalKg to find the top performers
        df = df.sort_values(by='TotalKg', ascending=False)
        df['TotalKg'] = df['TotalKg'].round(2)
        df_top_n = df.head(n).reset_index(drop=True)
        st.table(df_top_n[['Name', 'TotalKg', 'MeetName', 'Date']])
    else:
        st.write("No records found. Please adjust the filters.")
else:
    st.write("Please make a selection for all filters to see the records")
