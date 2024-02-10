import streamlit as st
from streamlit_app_utils.data_loader import yearly_meet_counts
import plotly.express as px


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
