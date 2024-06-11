# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 04:30:26 2024

@author: saif1
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV files
capology_df = pd.read_csv('capology.csv')
marketvalue_df = pd.read_csv('marketvalue.csv')

# Merging the two dataframes on the 'Player' column
merged_df = pd.merge(capology_df, marketvalue_df, on='Player')

# Exclude players who do not have a per_week_salary or whose per_week_salary is NaN
merged_df = merged_df.dropna(subset=['per-week-salary'])

# Calculate the fair market salary (FMS) for each player
merged_df['Fair Market Salary'] = 19.4 * (merged_df['Market Value'] ** 0.42)

# Convert the data to numpy arrays to ensure compatibility with matplotlib
market_value = merged_df['Market Value'].values
per_week_salary = merged_df['per-week-salary'].values
fair_market_salary = merged_df['Fair Market Salary'].values * 1000
overpaid_threshold = fair_market_salary * 2
underpaid_threshold = fair_market_salary * 0.5

# Determine the players in overpaid and underpaid categories
overpaid_players = merged_df[merged_df['per-week-salary'] > overpaid_threshold]
underpaid_players = merged_df[merged_df['per-week-salary'] < underpaid_threshold]

# Plotting the graph with the background portion colored and selected annotations
plt.figure(figsize=(14, 8))
plt.scatter(market_value, per_week_salary, alpha=0.7, label='Actual Salary')
plt.scatter(market_value, fair_market_salary, alpha=0.7, label='Fair Market Salary')

plt.yscale('log')
plt.xscale('log')
plt.title('Market Value vs. Player Weekly Salary with Fair Market Salary')
plt.ylabel('Weekly Salary in GBP')
plt.xlabel('Market Value in Million GBP')
plt.grid(True, which="both", ls="--")

# Creating a meshgrid for the fill_between shading
x = np.logspace(np.log10(market_value.min()), np.log10(market_value.max()), 500)
fair_market_salary_log = 19.4 * (x ** 0.42) * 1000
overpaid_threshold_log = fair_market_salary_log * 2
underpaid_threshold_log = fair_market_salary_log * 0.5

# Shading the areas
plt.fill_between(x, overpaid_threshold_log, per_week_salary.max(), where=(x >= market_value.min()), color='red', alpha=0.3, label='Overpaid Area')
plt.fill_between(x, per_week_salary.min(), underpaid_threshold_log, where=(x >= market_value.min()), color='green', alpha=0.3, label='Underpaid Area')

# Annotating the points with player names only for overpaid and underpaid players
for i, row in overpaid_players.iterrows():
    plt.annotate(row['Player'], (row['Market Value'], row['per-week-salary']), fontsize=8, alpha=0.75)

for i, row in underpaid_players.iterrows():
    plt.annotate(row['Player'], (row['Market Value'], row['per-week-salary']), fontsize=8, alpha=0.75)

plt.legend()
# Save the plot as a PNG file
plt.savefig('market_value_vs_player_salary_with_fms_log_scale_selected_colored.png')

# Display the plot
plt.show()
