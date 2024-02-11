import streamlit as st
import pandas as pd
from streamlit_app_utils.data_loader import df
import plotly.express as px


st.title('Meets per Year')
st.write("""
The questions that occur to me are:
\n- Have the number of meets per year increased over time for APL?
\n- How does this compare to other Federations?
\n- is there a relationship between number of meets per year and total 
competitors per year?
""")

unique_federations = df['Federation'].unique()
default_index = unique_federations.tolist().index('AusPL') if 'AusPL' in unique_federations else 0
selected_federation = st.selectbox(
    'Select Federation',
    unique_federations,
    index=default_index
)

# Use '==' for direct comparison since selected_federation is a single value
filtered_df = df[df['Federation'] == selected_federation]
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
filtered_df['Year'] = filtered_df['Date'].dt.year

# how many meets per year?
yearly_meet_counts = filtered_df.groupby('Year')['MeetName'].nunique()

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

st.write("""
My observations are:
\n- The number of meets per year has doubled year on year since 2021
\n- How does this compare to other Federations?
\n- There is a strong positive correlation between the number of meets per 
year and the total number of competitors per year
""")
