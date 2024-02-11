from streamlit_app_utils.data_loader import yearly_lifter_counts
import plotly.express as px
import streamlit as st


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
