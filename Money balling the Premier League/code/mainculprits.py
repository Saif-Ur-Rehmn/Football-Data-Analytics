# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 04:30:26 2024

@author: saif1
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Compute the median ratio for each club
median_ratios = merged_df.groupby('Club_x')['Salary to FMS Ratio'].median().sort_values()

# Plotting the bar graph
plt.figure(figsize=(14, 8))
median_ratios.plot(kind='bar')
plt.axhline(1, color='red', linestyle='--', linewidth=1)
plt.title('Median Ratio of Player Salary to Market Value-Implied Salary by Club')
plt.ylabel('Median Salary to Market Value-Implied Salary Ratio')
plt.xlabel('Club')
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', linewidth=0.7)  # Adding horizontal grid lines
plt.tight_layout()

# Adding text annotations
plt.text(0.95, 0.97, 'Lower value for money', horizontalalignment='right', verticalalignment='top', transform=plt.gca().transAxes, color='red', fontsize=12)
plt.text(0.05, 0.97, 'Higher value for money', horizontalalignment='left', verticalalignment='top', transform=plt.gca().transAxes, color='green', fontsize=12)

# Save the plot as a PNG file
plt.savefig('median_salary_to_fms_ratio_by_club.png')

# Display the plot
plt.show()
