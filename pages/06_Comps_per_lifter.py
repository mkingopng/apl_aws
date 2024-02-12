"""
how many times per year does each unique lifter compete?
how has this changed over time?
"""
import streamlit as st
import pandas as pd
from streamlit_app_utils.data_loader import filtered_df_copy  # Adjust the import path as necessary

st.title('Competitor Patterns Over Time')
st.write("""
How many times per year does each unique lifter compete?
\n- How has this changed over time?
\n- Are lifters competing more or less often each year?
""")

# Ensure 'Year' is treated as a string to keep it categorical
filtered_df_copy['Year'] = filtered_df_copy['Year'].astype(str)

# Calculate how many times lifters have competed each year
competitions_per_lifter_yearly = filtered_df_copy.groupby(['Year', 'Name']).size().reset_index(name='Competitions')
times_competing_pa = competitions_per_lifter_yearly.groupby(['Year', 'Competitions']).size().unstack(fill_value=0)

# Optionally, rename columns to clarify meaning
times_competing_pa.columns = [f'{col} times/year' for col in times_competing_pa.columns]

# Render the DataFrame in Streamlit
st.write("Summary of Competitions per Lifter Yearly:")
st.dataframe(times_competing_pa)
