"""

"""
import streamlit as st

# This file can be kept minimal since Streamlit automatically handles page navigation
st.title('Australian Powerlifting League Analysis')
st.write("""
This is a series of questions i found myself asking as i looked at the Open Powerlifting data. 
\nEach page attempts to answer a question stated in the plot tite, using plots of the data from Open Powerlifting.
\nThe plots are interactive: however you mouse over the plot elements to see hover text showing details of the data.
\n This is a work in progress so expect there to be ongoing additions of new questions and plots
\nPlease select a page from the left sidebar to view different analyses.
""")




######

# streamlit widgets
# gender widget
# equipment widget
# weight class widget
# tested widget

# year_range = st.sidebar.slider('Select Year Range', int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))
#
# record holders by weight class
# max_totals = filtered_df_copy.groupby(['WeightClassKg', 'Equipment', 'Tested'])['TotalKg'].max().reset_index()
# top_lifters = pd.merge(max_totals, filtered_df, on=['WeightClassKg', 'Equipment', 'Tested', 'TotalKg'], how='left')
# sorted_top_lifters = top_lifters.sort_values(by=['Tested', 'Equipment', 'Sex', 'WeightClassKg'], ascending=[True, True, True, True])
# dfs = {}
#
# instead of having a loop, use the widgets to filter the data
# for gender in sorted_top_lifters['Sex'].unique():
#     for tested in sorted_top_lifters['Tested'].unique():
#         for equipment in sorted_top_lifters['Equipment'].unique():
#             # Create a key for the dictionary
#             key = f"{gender}_{tested}_{equipment}"
#
#             # Filter the DataFrame for the current combination
#             df_filtered = sorted_top_lifters[
#                 (sorted_top_lifters['Sex'] == gender) &
#                 (sorted_top_lifters['Tested'] == tested) &
#                 (sorted_top_lifters['Equipment'] == equipment)
#                 ]
#
#             # only add to dictionary if the filtered DataFrame is not empty
#             if not df_filtered.empty:
#                 dfs[key] = df_filtered
#
# # Male & not tested, equipment=Raw
# male_not_tested_raw = dfs['M_False_Raw']
#
# # Male & not tested, equipment=Wraps
# male_not_tested_wraps = dfs['M_False_Wraps']
#
# # Male & not tested, equipment=Single-ply
# male_not_tested_single_ply = dfs['M_False_Single-ply']
#
# # Male & not tested, equipment=Multi-ply
# male_not_tested_multi_ply = dfs['M_False_Multi-ply']
#
# # female & not tested, equipment=Raw
# female_not_tested_raw = dfs['F_False_Raw'].reset_index(drop=True)
# _female_not_tested_raw = female_not_tested_raw[['Name', 'WeightClassKg', 'Equipment', 'Tested', 'TotalKg', 'Date', 'MeetName']].drop_duplicates()
#
# # Initialize a figure with go.Figure
# fig = go.Figure(data=[go.Table(
#     header=dict(
#         values=list(_female_not_tested_raw.columns),
#         align='left'
#     ),
#     cells=dict(
#         values=[_female_not_tested_raw[k].tolist() for k in _female_not_tested_raw.columns],
#         align='left'
#     ))
# ])
# fig.update_layout(
#     title_text='National Records Female Raw Untested',
#     title_x=0.5,
#     width=800,
#     height=600
# )
# st.plotly_chart(fig)
#
# # Female & not tested, equipment=Wraps
# female_not_tested_wraps = dfs['F_False_Wraps']
#
# # Female & not tested, equipment=Single-ply
# female_not_tested_single_ply = dfs['F_False_Single-ply']
#
# # Female & not tested, equipment=Multi-ply
# female_not_tested_multi_ply = dfs['F_False_Multi-ply']
#
# # Male & tested, equipment=Raw
# male_tested_raw = dfs['M_True_Raw']
#
# # Female & tested, equipment=Raw
# female_tested_raw = dfs['F_True_Raw']
