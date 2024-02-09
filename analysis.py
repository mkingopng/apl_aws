import pandas as pd
import matplotlib.pyplot as plt


dtype_dict = {
    'State': 'string',
    'ParentFederation': 'string',
    'MeetState': 'string',
    'Bench4kg': 'float'
}


def yes_no_to_bool(value):
    """
    converts "Yes" to True and empty values to False
    :param value:
    :return:
    """
    if value == 'Yes':
        return True
    else:
        return False


df = pd. read_csv(
    'data/openpowerlifting-2024-02-03-a32a2f7d.csv',
    dtype=dtype_dict,
    converters={'Tested': yes_no_to_bool}
)

filtered_df = df[df['Federation'] == 'AusPL']
filtered_df_copy = filtered_df.copy()

# Convert 'Date' to datetime and extract the year
filtered_df_copy['Date'] = pd.to_datetime(filtered_df_copy['Date'])
filtered_df_copy['Year'] = filtered_df_copy['Date'].dt.year

# how many meets per year are there?
yearly_meet_counts = filtered_df_copy.groupby('Year')['MeetName'].nunique()
print(yearly_meet_counts)

yearly_meet_counts.plot(kind='bar', figsize=(10, 6)) # You can adjust the figure size as needed
plt.title('Unique MeetNames per Year')
plt.xlabel('Year')
plt.ylabel('Unique MeetNames Count')
plt.xticks(rotation=90) # Rotate labels to make them readable
plt.tight_layout() # Adjusts subplot params so that the subplot(s) fits into the figure area
plt.show()

# how many lifters have competed in each year?
yearly_lifter_counts = filtered_df_copy.groupby('Year')['Name'].count()
print(yearly_lifter_counts)

yearly_lifter_counts.plot(kind='bar', figsize=(10, 6))
plt.title('Total Number of Competitors per Year')
plt.xlabel('Year')
plt.ylabel('Total Participations')
plt.xticks(rotation=45)  # Rotate x-axis labels to make them readable
plt.yticks(rotation=0)  # Ensure y-axis labels are vertical
plt.tight_layout()  # Adjust subplot params so that the subplot(s) fits into the figure area
plt.show()

lifters_per_year = filtered_df_copy.groupby('Year')['Name'].nunique()
print(lifters_per_year)


lifters_per_year.plot(kind='bar', figsize=(10, 6))
plt.title('Number of Unique Lifters per Year')
plt.xlabel('Year')
plt.ylabel('Number of Lifters')
plt.xticks(rotation=45)  # Rotate x-axis labels to make them readable
plt.yticks(rotation=0)  # Ensure y-axis labels are vertical
plt.tight_layout()  # Adjusts subplot params so that the subplot(s) fits into the figure area
plt.show()

# how many times have lifters competed each year?
competitions_per_lifter_yearly = filtered_df_copy.groupby(['Year', 'Name']).size().reset_index(name='Competitions')
print(competitions_per_lifter_yearly)

times_competing_pa = competitions_per_lifter_yearly.groupby(['Year', 'Competitions']).size().unstack(fill_value=0)
print(times_competing_pa)

eight_comps_23 = competitions_per_lifter_yearly[(competitions_per_lifter_yearly['Year'] == 2023) & (competitions_per_lifter_yearly['Competitions'] == 8)]
print(eight_comps_23)

# has the gender distribution changed over time?
# group by 'Year' and 'Gender' and count competitors
gender_distribution_yearly = filtered_df_copy.groupby(['Year', 'Sex']).size().unstack(fill_value=0)

# calculate the total competitors per year
gender_distribution_yearly['Total'] = gender_distribution_yearly.sum(axis=1)

# calculate the percentage of total for each gender
gender_distribution_yearly['% Male'] = ((gender_distribution_yearly['M'] / gender_distribution_yearly['Total']) * 100).round(0)
gender_distribution_yearly['% Female'] = ((gender_distribution_yearly['F'] / gender_distribution_yearly['Total']) * 100).round(0)

# display the updated DataFrame
print(gender_distribution_yearly)

gender_distribution_yearly[['F', 'M']].plot(kind='bar', figsize=(12, 6))
plt.title('Number of Competitors by Gender Each Year')
plt.xlabel('Year')
plt.ylabel('Number of Competitors')
plt.xticks(rotation=45)
plt.legend(title='Gender')
plt.tight_layout()
plt.show()

# plotting the gender distribution as a stacked bar chart
gender_distribution_yearly[['F', 'M']].plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Number of Competitors by Gender Each Year (Stacked)')
plt.xlabel('Year')
plt.ylabel('Number of Competitors')
plt.xticks(rotation=45)
plt.legend(title='Gender')
plt.tight_layout()
plt.show()


# record holders by weight class
max_totals = filtered_df_copy.groupby(['WeightClassKg', 'Equipment', 'Tested'])['TotalKg'].max().reset_index()
top_lifters = pd.merge(max_totals, filtered_df, on=['WeightClassKg', 'Equipment', 'Tested', 'TotalKg'], how='left')
_top_lifters = top_lifters[['Name', 'WeightClassKg', 'Equipment', 'Tested', 'TotalKg']]
sorted_top_lifters = top_lifters.sort_values(by=['Tested', 'Equipment', 'Sex', 'WeightClassKg'], ascending=[True, True, True, True])
_sorted_top_lifters = sorted_top_lifters[['Name', 'WeightClassKg', 'Equipment', 'Tested', 'TotalKg', 'Date']]

dfs = {}

# Iterate over each combination of Gender, Tested, and Equipment
for gender in sorted_top_lifters['Sex'].unique():
    for tested in sorted_top_lifters['Tested'].unique():
        for equipment in sorted_top_lifters['Equipment'].unique():
            # Create a key for the dictionary
            key = f"{gender}_{tested}_{equipment}"

            # Filter the DataFrame for the current combination
            df_filtered = sorted_top_lifters[
                (sorted_top_lifters['Sex'] == gender) &
                (sorted_top_lifters['Tested'] == tested) &
                (sorted_top_lifters['Equipment'] == equipment)
                ]

            # Only add to dictionary if the filtered DataFrame is not empty
            if not df_filtered.empty:
                dfs[key] = df_filtered

# Male & not tested, equipment=Raw
male_not_tested_raw = dfs['M_False_Raw']

# Male & not tested, equipment=Wraps
male_not_tested_wraps = dfs['M_False_Wraps']

# Male & not tested, equipment=Single-ply
male_not_tested_single_ply = dfs['M_False_Single-ply']

# Male & not tested, equipment=Multi-ply
male_not_tested_multi_ply = dfs['M_False_Multi-ply']

# Female & not tested, equipment=Raw
female_not_tested_raw = dfs['F_False_Raw']

# Female & not tested, equipment=Wraps
female_not_tested_wraps = dfs['F_False_Wraps']

# Female & not tested, equipment=Single-ply
female_not_tested_single_ply = dfs['F_False_Single-ply']

# Female & not tested, equipment=Multi-ply
female_not_tested_multi_ply = dfs['F_False_Multi-ply']

# Male & tested, equipment=Raw
male_tested_raw = dfs['M_True_Raw']

# Female & tested, equipment=Raw
female_tested_raw = dfs['F_True_Raw']
