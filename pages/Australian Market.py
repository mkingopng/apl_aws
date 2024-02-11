"""
which powerlifting federation has what marketshare in Australia?
How as this changed over time?
"""
import streamlit as st
from streamlit_app_utils.data_loader import df
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


st.title('Australian Powerlifting Market')
st.write("""
The questions that occur to me are:
\n- is powerlifting growing in Australia?
\n- which powerlifting federation has what market-share in Australia?
\n- How as this changed over time?
""")

# Assuming 'df' is your DataFrame
df['Year'] = pd.to_datetime(df['Date']).dt.year

# df = df[df['Year'] >= 1990]
# Determine the range of years in your DataFrame
min_year = df['Year'].min()
max_year = df['Year'].max()

# Add a slider for selecting the year range
selected_years = st.slider(
    'Select Year Range',
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year))  # Default value is the full range
)

# Filter the DataFrame based on the selected year range
filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]

# Count unique lifters per year and federation
lifters_per_year_federation = filtered_df.groupby(['Year', 'Federation'])['Name'].size().reset_index(name='Lifters')
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
    showlegend=False
)

st.plotly_chart(fig)

st.write("""
My observations:
- The sport of Powerlifting in Australia has been growing consistently over 
the years. It took a hit in 2020 due to COVID but has quickly rebounded to be 
bigger than pre-COVID
- PA was the biggest federation until 2019. It took a massive hit in 2020, and 
has been in decline since.
- GPC is a similar story, albeit less drastic.
- THe big winners / growers over the same period are APL / AusPL and USAPL
- APU has growing rapidly from 2020 but dipped in 2023. Given the recent exodus 
of members from APU and the end of their IPF affiliation, it seems reasonable 
to expect that APU numbers will tank in 2024
- There is every reason to expect continued triple digit year on year growth 
from APL, if it can capitalise on the ongoing changes in the market
- there are 3 obvious vectors for growth in the short term - organic growth; 
attracting former APU members; attracting GPC members
""")
