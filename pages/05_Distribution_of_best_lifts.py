"""
box & whisker plot showing the distributio of best lift by gender and weight class
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_app_utils.data_loader import df  # Make sure this path is correct

st.title('Distribution of Lifts by Gender, Lift Type, and Equipment')
st.write("""
Exploring the distribution across all lifters provides insights beyond just the top performers.
\n - What's the distribution of the best lifts by gender, weight class, lift type, and equipment?
\n - This can be visualized using a box & whisker plot.
""")

# Assuming df is already filtered for 'AusPL' federation
df = df[df['Federation'] == 'AusPL']
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Widgets for selecting the gender, lift type, and equipment
gender_choice = st.selectbox("Select Gender", ["M", "F"])
lift_choice = st.selectbox("Select Lift Type", ["Squat", "Bench Press", "Deadlift"])
equipment_choice = st.selectbox("Select Equipment", df['Equipment'].unique())

# Mapping user selections to column names
lift_map = {
    "Squat": "Best3SquatKg",
    "Bench Press": "Best3BenchKg",
    "Deadlift": "Best3DeadliftKg"
}
lift_column = lift_map[lift_choice]

# Filtering the data based on the selected gender, lift type, and equipment
filtered_df = df[(df["Sex"] == gender_choice) & (df["Equipment"] == equipment_choice)]

# Creating the box plot for the selected lift, gender, and equipment
fig = px.box(
    filtered_df,
    x="WeightClassKg",
    y=lift_column,
    color="WeightClassKg",
    labels={lift_column: f"{lift_choice} Weight (kg)"},
    title=f"Distribution of {lift_choice} Weights by Weight Class for {gender_choice} using {equipment_choice}")

fig.update_layout(
    xaxis_title="Weight Class (kg)",
    yaxis_title=f"{lift_choice} Weight (kg)"
)

st.plotly_chart(fig)

