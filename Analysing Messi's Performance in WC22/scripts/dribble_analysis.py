import pandas as pd
import json

# Size of the pitch in yards
pitchLengthX = 120
pitchWidthY = 80

player_analysed = 'Lionel Andrés Messi Cuccittini'

match_ids = [3869151, 3869321, 3869685, 3857264, 3857289, 3869519, 3857300]


dribble_count = 0
successful_dribble_count = 0


for match_id_required in match_ids:
    file_name = str(match_id_required) + '.json'
    with open('Statsbomb/data/events/' + file_name, encoding='utf-8') as data_file:
        data = json.load(data_file)
    # Get the nested structure into a dataframe
    df = pd.json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    
    # Find the dribbles
    dribbles = df.loc[df['type_name'] == 'Dribble'].set_index('id')

    # Calculating dribbles
    for i, dribble in dribbles.iterrows():
        if dribble['player_name'] == player_analysed:
            dribble_count += 1
            x = dribble['location'][0]
            y = dribble['location'][1]

            if 'dribble_end_location' in dribble and isinstance(dribble['dribble_end_location'], list):
                end_x = dribble['dribble_end_location'][0]
                end_y = dribble['dribble_end_location'][1]
                dx = end_x - x
                dy = end_y - y
            else:
                end_x = x
                end_y = y
                dx = 0
                dy = 0

            success = dribble['dribble_outcome_name'] == 'Complete' if 'dribble_outcome_name' in dribble else True
            if success:
                successful_dribble_count += 1
             
dribble_success_rate = successful_dribble_count / dribble_count * 100 if dribble_count > 0 else 0



print("Total dribbles attempted by Messi:", dribble_count)
print("Successful dribbles:", successful_dribble_count)
print("Dribble success rate:", dribble_success_rate)
