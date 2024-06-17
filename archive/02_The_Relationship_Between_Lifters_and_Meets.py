"""

"""
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_app_utils.data_loader import df  # Adjust the import path as necessary

st.title('Yearly Trends in Powerlifting Meets and Participation')
df['Year'] = pd.to_datetime(df['Date']).dt.year
filtered_df = df[df['Federation'] == 'AusPL']
yearly_meet_counts = filtered_df.groupby('Year')['MeetName'].nunique().reset_index(name='Number of Meets')
yearly_lifter_counts = filtered_df.groupby('Year')['Name'].count().reset_index(name='Lifter Entries')
yearly_data = pd.merge(yearly_meet_counts, yearly_lifter_counts, on='Year')

fig = px.scatter(
    yearly_data,
    x='Year',
    y='Number of Meets',
    size='Lifter Entries',
    color='Lifter Entries',
    hover_name='Year',
    size_max=80,
    color_continuous_scale=px.colors.sequential.Inferno,
    title='Annual Powerlifting Meets and Lifter Participation')

fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Number of Meets',
    coloraxis_colorbar=dict(title='Number of Lifter Entries'))

st.plotly_chart(fig)

st.write("""
There's a very clear positive relationship between the number of meets held 
per year and the total number of lifters who compete under APL per year. 

If we combine that with the information from the last visualisation, we can 
conclude that more meets that cater to disaffected APU and GPC members, and 
lifters who want to compete IPF, with maximise APL's growth potential over the 
next year or two.
""")
