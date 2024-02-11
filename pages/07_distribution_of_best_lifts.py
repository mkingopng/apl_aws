"""
box & whisker plot showing the distributio of best lift by gender and weight class
"""

import streamlit as st

st.title('Distribution of Lifts?')
st.write("""
we often focus on the records, the top lifters. But I'd like to know what the 
whole field looks like.
\n - whats the average best lifter by gender, weight class, and equipment?
\n - how is this distributed? (standard deviation, IQR, outliers)

\n we can show this with a box & whisker plot
""")
