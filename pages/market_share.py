"""
which powerlifting federation has what marketshare in Australia?
How as this changed over time?
"""
import streamlit as st
from streamlit_app_utils.data_loader import df
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


st.title('Australian Powerlifting Marketshare')
st.write("""
which powerlifting federation has what marketshare in Australia?
\nHow as this changed over time?
\nIs powerlifting growing in australia?
""")

# Assuming 'df' is your DataFrame
df['Year'] = pd.to_datetime(df['Date']).dt.year

df = df[df['Year'] >= 1990]

# Count unique lifters per year and federation
lifters_per_year_federation = df.groupby(['Year', 'Federation'])['Name'].size().reset_index(name='Lifters')
pivot_df = lifters_per_year_federation.pivot(
    index='Year',
    columns='Federation',
    values='Lifters'
).fillna(0)


fig = go.Figure()
for federation in pivot_df.columns:
    fig.add_trace(go.Bar(
        name=federation,
        x=pivot_df.index,
        y=pivot_df[federation],
        )
    )

fig.update_layout(
    barmode='stack',
    title_text='Number of Lifters Competing Each Year by Federation',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Number of Lifters'),
)

st.plotly_chart(fig)
