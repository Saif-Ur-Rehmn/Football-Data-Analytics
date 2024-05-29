import matplotlib.pyplot as plt
import pandas as pd
import json
from FCPython import createPitch

# Size of the pitch in yards
pitchLengthX = 120
pitchWidthY = 80

home_team_required = "Argentina"
player_analysed = 'Lionel Andrés Messi Cuccittini'

# Match details
matches = {
    3869151: "Australia",
    3869321: "Netherlands",
    3869685: "France",
    3857264: "Poland",
    3857289: "Mexico",
    3869519: "Coratia",
    3857300: "Saudi Arabia"
}
match_ids = [3869151, 3869321, 3869685, 3857264, 3857289, 3869519, 3857300]
color_country = {3869151: 'xkcd:sun yellow', 3869321: 'xkcd:orange', 3869685: 'xkcd:blue', 
                 3857264: 'xkcd:red', 3857289: 'xkcd:frog green', 3869519: 'xkcd:vermillion', 
                 3857300: 'xkcd:dark grass green'}

pass_count = 0

# Create the figure and axis
(fig, ax) = createPitch(pitchLengthX, pitchWidthY, 'yards', 'gray')

for match_id_required in match_ids:
    file_name = str(match_id_required) + '.json'
    with open('Statsbomb/data/events/' + file_name, encoding='utf-8') as data_file:
        data = json.load(data_file)
        
    # Get the nested structure into a dataframe
    df = pd.json_normalize(data, sep="_").assign(match_id=file_name[:-5])

    # Find the passes
    passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

    # Plotting all passes
    for i, thepass in passes.iterrows():
        if thepass['player_name'] == player_analysed:
            pass_count += 1
            
            x = thepass['location'][0]
            y = thepass['location'][1]
            passCircle = plt.Circle((x, pitchWidthY - y), .25, color=color_country[match_id_required])      
            passCircle.set_alpha(.125)   
            ax.add_patch(passCircle)
            dx = thepass['pass_end_location'][0] - x
            dy = thepass['pass_end_location'][1] - y
            passArrow = plt.Arrow(x, pitchWidthY - y, dx, -dy, width=3, color=color_country[match_id_required])
            passArrow.set_alpha(0.125)
            ax.add_patch(passArrow)

    # Filter key passes
    key_passes = passes[passes['pass_goal_assist'].notnull() | passes['pass_shot_assist'].notnull()]

    # Plotting key passes
    for i, thepass in key_passes.iterrows():
        if thepass['player_name'] == player_analysed:
            x = thepass['location'][0]
            y = thepass['location'][1]
            passCircle = plt.Circle((x, pitchWidthY - y), 0.25, color=color_country[match_id_required])      
            passCircle.set_alpha(1)
            ax.add_patch(passCircle)
            dx = thepass['pass_end_location'][0] - x
            dy = thepass['pass_end_location'][1] - y
            passArrow = plt.Arrow(x, pitchWidthY - y, dx, -dy, width=3, color=color_country[match_id_required])
            passArrow.set_alpha(1)
            ax.add_patch(passArrow)

# Calculate and print metrics
total_passes = passes.shape[0]
completed_passes = passes[passes['pass_outcome_name'].isnull()].shape[0]
pass_completion_rate = completed_passes / total_passes * 100
key_passes_count = key_passes.shape[0]


# Adding the legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=match_name,
                              markerfacecolor=color_country[match_id], markersize=10) for match_id, match_name in matches.items()]

plt.legend(handles=legend_elements, loc='lower left')

plt.text(10, 75, 'Attempted passes by Messi')
fig.set_size_inches(10, 7)
fig.savefig('Output/passes.pdf', dpi=100) 
print("Total passes attempted by Messi:", pass_count)
print("Total passes: ", total_passes)
print("Completed passes: ", completed_passes)
print("Key passes type: ", type(key_passes))
print("Key passes count:", key_passes_count)
print("Pass completion rate: ", pass_completion_rate)
plt.show()
