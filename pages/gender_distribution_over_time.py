from streamlit_app_utils.data_loader import gender_distribution_yearly
import plotly.express as px
import streamlit as st


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