"""
box & whisker plot showing the distributio of best lift by gender and weight class
"""

import streamlit as st

st.title('Distribution of Lifts?')
st.write("""
We often focus on the records, the top lifters. But I'd like to know what the 
whole field looks like.
\n - Whats the average best lift (SBD) by gender, weight class, and equipment?
\n - How is this distributed? (standard deviation, IQR, outliers)

\nWe can show this with a box & whisker plot
""")
