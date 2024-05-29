import matplotlib.pyplot as plt
import pandas as pd
import json
from FCPython import createPitch

# Size of the pitch in yards
pitchLengthX = 120
pitchWidthY = 80

#player to be analysed
player_analysed = 'Lionel Andrés Messi Cuccittini'

#match ids for all matches played by Argentina
match_ids = [3869151, 3869321, 3869685, 3857264, 3857289, 3869519, 3857300]

matches = {
    3869151: "Australia",
    3869321: "Netherlands",
    3869685: "France",
    3857264: "Poland",
    3857289: "Mexico",
    3869519: "Coratia",
    3857300: "Saudi Arabia"
}


#color coding for opponent teams
color_country = {3869151: 'xkcd:sun yellow', 3869321: 'xkcd:orange', 3869685: 'xkcd:blue', 
                 3857264: 'xkcd:red', 3857289: 'xkcd:frog green', 3869519: 'xkcd:vermillion', 
                 3857300: 'xkcd:dark grass green'}

#initiating xg_count, goal_count and shot_count vairables for aalysing Messi's shots
xg_count = 0
shot_count = 0
goal_count = 0


# Create the figure and axis
(fig, ax) = createPitch(pitchLengthX, pitchWidthY, 'yards', 'gray')

# Load in the data and plot the shots
for match_id_required in match_ids:
    file_name = str(match_id_required) + '.json'
    with open('Statsbomb/data/events/' + file_name, encoding='utf-8') as data_file:
        data = json.load(data_file)

    # get the nested structure into a dataframe
    df = pd.json_normalize(data, sep="_").assign(match_id=file_name[:-5])

    # A dataframe of shots
    shots = df.loc[df['type_name'] == 'Shot'].set_index('id')

    # Plot the shots
    for i, shot in shots.iterrows():
        x = shot['location'][0]
        y = shot['location'][1]

        goal = shot['shot_outcome_name'] == 'Goal'
        team_name = shot['team_name']
        shot_player = shot['player_name']
        
        #period defines the period of the game..1st period is 1st half, 2nd period is 2nd half, 3rd period is 1st half of extra time and so on
        if (shot_player == player_analysed and shot['period'] < 5):
            
            xg_count += shot['shot_statsbomb_xg']
            shot_count += 1

            circleSize = 2
            # circleSize = np.sqrt(shot['shot_statsbomb_xg']) * 12

            if goal:
                shotCircle = plt.Circle((x, pitchWidthY - y), circleSize, color=color_country.get(match_id_required))
                plt.text((x + 1), pitchWidthY - y + 1, shot['shot_statsbomb_xg'])
                goal_count+=1
            else:
                shotCircle = plt.Circle((x, pitchWidthY - y), circleSize, color=color_country.get(match_id_required))
                shotCircle.set_alpha(.2)

            ax.add_patch(shotCircle)

# Adding the legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=match_name,
                              markerfacecolor=color_country[match_id], markersize=10) for match_id, match_name in matches.items()]

plt.legend(handles=legend_elements, loc='lower left')


plt.text(80, 75, 'Shots by Messi')
fig.set_size_inches(10, 7)
fig.savefig('Output/shots.pdf', dpi=100)
plt.show()

print('total xg accumulated= ', xg_count)
print('number of shots by Messi', shot_count)
print ('number of goals scored by Messi: ', goal_count)
