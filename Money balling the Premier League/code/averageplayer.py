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

# Calculate the fair market salary (FMS) for each player
merged_df['Fair Market Salary'] = 19.4 * (merged_df['Market Value'] ** 0.42)

# Calculate the ratio of actual salary to fair market salary
merged_df['Salary to FMS Ratio'] = merged_df['per-week-salary'] / (merged_df['Fair Market Salary'] * 1000)

# Filter the dataset to include only Manchester United players
manutd_df = merged_df[merged_df['Club_x'] == 'Manchester United']

# Compute the average ratio of actual salary to fair market salary for Manchester United players
average_ratio_manutd = manutd_df['Salary to FMS Ratio'].mean()

# Determine the percentage by which this average ratio exceeds 1
percentage_exceed = (average_ratio_manutd - 1) * 100

print(f"The average player in Manchester United's squad earns {percentage_exceed:.2f}% of their FMS.")
