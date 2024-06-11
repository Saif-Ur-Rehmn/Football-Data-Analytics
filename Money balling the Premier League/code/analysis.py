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

# Convert the data to numpy arrays to ensure compatibility with matplotlib
market_value = merged_df['Market Value'].values
per_week_salary = merged_df['per-week-salary'].values
fair_market_salary = merged_df['Fair Market Salary'].values * 1000
overpaid_threshold = fair_market_salary * 2
underpaid_threshold = fair_market_salary * 0.5

# Determine the players in overpaid and underpaid categories
overpaid_players = merged_df[merged_df['per-week-salary'] > overpaid_threshold]
underpaid_players = merged_df[merged_df['per-week-salary'] < underpaid_threshold]

# Determine the players earning more than 250% and less than 35% of their fair market salary
overpaid_players_extreme = merged_df[merged_df['per-week-salary'] > 2.5 * fair_market_salary]
underpaid_players_extreme = merged_df[merged_df['per-week-salary'] < 0.35 * fair_market_salary]

# Plotting the graph with the background portion colored and selected annotations
plt.figure(figsize=(14, 8))
plt.scatter(market_value, per_week_salary, alpha=0.7, label='Actual Salary')

#Plotting fair market salary reference
plt.plot(market_value, fair_market_salary, '--', color='black', alpha=0.7, label='Fair Market Salary')



plt.yscale('log')
plt.xscale('log')
plt.title('Market Value vs. Player Weekly Salary with Fair Market Salary')
plt.ylabel('Weekly Salary in euros (capology.com) ')
plt.xlabel('Market Value in million euros (transfermarkt.com)')
# plt.grid(True, which="both", ls="--")   - Uncomment this to see grid

# Creating a meshgrid for the fill_between shading
x = np.logspace(np.log10(market_value.min()), np.log10(market_value.max()), 500)
fair_market_salary_log = 19.4 * (x ** 0.42) * 1000
overpaid_threshold_log = fair_market_salary_log * 2
underpaid_threshold_log = fair_market_salary_log * 0.5

# Shading the areas
plt.fill_between(x, overpaid_threshold_log, per_week_salary.max(), where=(x >= market_value.min()), color='red', alpha=0.2, label='Overpaid Area')
plt.fill_between(x, per_week_salary.min(), underpaid_threshold_log, where=(x >= market_value.min()), color='green', alpha=0.2, label='Underpaid Area')

# Annotating the points with player names only for overpaid and underpaid players beyond the specified thresholds
# and ensuring not to annotate players with close salaries

def annotate_players(player_df, color):
    annotated_positions = []
    for i, row in player_df.iterrows():
        close_to_existing = False
        for pos in annotated_positions:
            if abs(np.log10(row['per-week-salary']) - np.log10(pos[1])) < 0.05:
                close_to_existing = True
                break
        if not close_to_existing:
            plt.annotate(row['Player'], (row['Market Value'], row['per-week-salary']), fontsize=8, color=color, alpha=0.9)
            annotated_positions.append((row['Market Value'], row['per-week-salary']))

annotate_players(overpaid_players_extreme, 'black')
annotate_players(underpaid_players_extreme, 'black')

plt.legend()

plt.savefig('moneyball-fms-epl.png')
# Display the plot
plt.show()
