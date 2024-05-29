plt.show()
        
    # Get the nested structure into a dataframe
    df = pd.json_normalize(data, sep="_").assign(match_id=file_name[:-5])
    
    # Find the dribbles
    dribbles = df.loc[df['type_name'] == 'Dribble'].set_index('id')

    # Plotting dribbles
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
                dx = 0
                dy = 0

            success = dribble['dribble_outcome_name'] == 'Complete' if 'dribble_outcome_name' in dribble else True
            if success:
                successful_dribble_count += 1
                dribbleCircle = plt.Circle((x, pitchWidthY - y), 0.25, color='green', alpha=1)
            else:
                dribbleCircle = plt.Circle((x, pitchWidthY - y), 0.25, color='red', alpha=0.2)

            ax.add_patch(dribbleCircle)
            
            # Draw the arrow for the dribble
            dribbleArrow = plt.Arrow(x, pitchWidthY - y, dx, -dy, width=3, color='blue' if success else 'red')
            dribbleArrow.set_alpha(1 if success else 0.2)
            ax.add_patch(dribbleArrow)

dribble_success_rate = successful_dribble_count / dribble_count * 100 if dribble_count > 0 else 0

plt.text(80, 75, 'Dribbles by Messi')
fig.set_size_inches(10, 7)
fig.savefig('Output/dribbles_corrected.pdf', dpi=100) 

print("Total dribbles attempted by Messi:", dribble_count)
print("Successful dribbles:", successful_dribble_count)
print("Dribble success rate:", dribble_success_rate)
plt.show()
