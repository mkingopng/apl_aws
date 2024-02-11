"""

"""
from streamlit_app_utils.data_loader import lifters_per_year
import plotly.express as px
import streamlit as st

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
