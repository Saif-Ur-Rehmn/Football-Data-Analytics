# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 01:33:29 2024

@author: saif1
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 01:16:11 2024

@author: saif1
"""
import pandas as pd

# Load the CSV files
capology_df = pd.read_csv('capology.csv')  # Ensure these files are in the same directory
marketvalue_df = pd.read_csv('marketvalue.csv')

# Merging the two dataframes on the 'Player' column
merged_df = pd.merge(capology_df, marketvalue_df, on='Player')

# Exclude players who do not have a per_week_salary or whose per_week_salary is NaN
merged_df = merged_df.dropna(subset=['per-week-salary'])

# Filter the dataset to find Danny Ings
danny_ings = merged_df[merged_df['Player'] == 'Danny Ings']

# Extract Danny Ings' market value and salary
danny_ings_market_value = danny_ings['Market Value'].values[0]
danny_ings_salary = danny_ings['per-week-salary'].values[0]

# Calculate Danny Ings' fair market salary (FMS)
danny_ings_fms = 19.4 * (danny_ings_market_value ** 0.42)

# Calculate the ratio of actual salary to FMS
danny_ings_ratio = danny_ings_salary / (danny_ings_fms * 1000)

print(f"Danny Ings' actual salary is {danny_ings_ratio:.2f} times his Fair Market Salary.")
